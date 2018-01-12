import pymongo
import time
from . import utils
import sched
import re
import calendar
import threading
import json 
from bson import json_util
from bson import ObjectId
from requests_futures.sessions import FuturesSession
import urllib

class StagingJobsManager:
    def __init__(self, config):
        self.config = config
        self.jgi_search_base_url = config['jgi']['base-url']
        self.user = config['jgi']['user']
        self.password = config['jgi']['password']
        self.connection_timeout = config['jgi']['connection-timeout']

        self.mongo_host = config['mongo']['host']

        self.mongo_port = int(config['mongo']['port'])

        self.mongo_db = config['mongo']['db']

        self.mongo_user = config['mongo']['user']

        self.mongo_pwd = config['mongo']['password']

        self.mongo = pymongo.MongoClient(self.mongo_host, self.mongo_port)

        self.db = self.mongo[self.mongo_db]
        self.db.authenticate(self.mongo_user, urllib.quote_plus(self.mongo_pwd))

        self.regexes = {
            'queued': re.compile(r'^In_Queue$'),
            'completed': re.compile(r'^Transfer Complete\. Transfered ([\d]+) files\.$'),
            'progress': re.compile(r'^In Progress\. Total files = ([\d]+)\. Copy complete = ([\d]+)\. Restore in progress = ([\d]+)\. Copy in progress = ([\d]+)$'),
            'error': re.compile(r"^Transfer Complete. Transfered ([\d]+) files. Scp failed for files = \[u'(.*?)'\]$"),
            'notfound': re.compile(r"^Error: No such Id$")
        }

    def translate_job_status(self, status):
        m = re.search(self.regexes['queued'], status)
        if m:
            return 'queued', None

        m = re.search(self.regexes['completed'], status)
        if m:
            return 'completed', None

        m = re.search(self.regexes['error'], status)
        if m:
            return 'error', None

        m = re.search(self.regexes['notfound'], status)
        if m:
            return 'notfound', None

        m = re.search(self.regexes['progress'], status)
        if m == None:
            return None, 'Unrecognized job status message'

        total, completed, restoring, copying = m.groups()
        if total != '1':
            return None, 'Strange, progress message but no files reported'
        if completed == '1':
            return 'completed', None
        if restoring == '1':
            return 'restoring', None
        if copying == '1':
            return 'copying', None
        
        return None, 'Strange, progress message with a file but no files in state reported'

    def staging_jobs_for_user(self, req):
        'For a give request spec, return the staging jobs for the given user'
        collection = self.db.staging_jobs

        # Filter

        # Username is always used, and is not part of the filter condition.
        find_filter = {
            'username': req['username']
        }

        # Supported filters:

        # By job id or filename

        # By status
        if 'job_statuses' in req['filter']:
            find_filter['status_code'] = {'$in': req['filter']['job_statuses']}            

        # By job id
        if 'job_ids' in req['filter']:
            find_filter['job_id'] = {'$in': req['filter']['job_ids']}

        # Skip and Limit == range
        skip = None
        limit = None
        if req['range'] is not None:
            if 'start' in req['range']:
                skip = req['range']['start']
            if 'limit' in req['range']:
                limit = req['range']['limit']


        # Default sort.
        if req['sort'] is None:
            find_sort = [
                ('created', pymongo.DESCENDING)
            ]
        else:
            find_sort = []
            for sort_spec in req['sort']:
                if sort_spec['descending']:
                    print('sort descending')
                    direction = pymongo.DESCENDING
                else:
                    print('sort ascending')
                    direction = pymongo.ASCENDING
                find_sort.append((sort_spec['field'], direction))

        jobs = collection.find(spec=find_filter, skip=skip, limit=limit, sort=find_sort)
        jobs_json = []
        for job in jobs:
            job_json = json.loads(json_util.dumps(job))
            # we use the document object id as the primary id for the job record
            job_monitoring_id = job_json['_id']['$oid']
            job_json['job_monitoring_id'] = job_monitoring_id
            jobs_json.append(job_json)

        total_matched = collection.find(spec=find_filter).count()

        total_available = collection.find(spec={'username': req['username']}).count()

        return {
            'jobs': jobs_json,
            'total_matched': total_matched,
            'total_available': total_available
        }

    def get_jobs_summary_for_user(self, req):
        'For a give request spec, return the summary of staging jobs in each state for the given user'
        collection = self.db.staging_jobs

        # Filter

        # Username is always used, and is not part of the filter condition.
        match_stage = {
            'username': req['username']
        }

        group_stage = {
            '_id': '$status_code',
            'count': {'$sum': 1}
        }

        pipeline_expression = [
            {'$match': match_stage},
            {'$group': group_stage}
        ]

        cursor = collection.aggregate(pipeline_expression, cursor={})

        result = {}
        for doc in cursor:
            result[doc['_id']] = doc['count']

        states = ['sent', 'submitted', 'queued', 'restoring', 'copying', 'completed', 'error']
        state_summary = {}
        for state_name in states:
            if state_name in result:
                state = result[state_name]
            else:
                state = 0
            state_summary[state_name] = state

        return state_summary

    def get_jobs_summary_for_ids(self, req):
        'For a give request spec, return the summary of staging jobs in each state for the given user'
        collection = self.db.staging_jobs

        # Filter

        # Username is always used, and is not part of the filter condition.
        match_stage = {
            'username': req['username'],
            'jamo_id': {'$in': req['job_monitoring_ids']}
        }

        group_stage = {
            '_id': {'jamo_id': '$jamo_id', 'status_code': '$status_code'},
            'count': {'$sum': 1}
        }

        pipeline_expression = [
            {'$match': match_stage},
            {'$group': group_stage}
        ]

        cursor = collection.aggregate(pipeline_expression, cursor={})

        result = {}
        for doc in cursor:
            result[doc['_id']] = doc['count']

        # states = ['sent', 'submitted', 'queued', 'restoring', 'copying', 'completed', 'error']
        ids_summary = {}
        for job_monitoring_id in req['job_monitoring_ids']:
            ids_summary[job_monitoring_id] = {}

        for doc in result:
            job_monitoring_id = doc['_id']['status_code']
            state_name = doc['_id']['status_code']
            ids_summary[job_monitoring_id][state_name] = doc['count']
            
        return ids_summary      

    def add_job(self, username, jamo_id, filename):
        'add a job to the jobs database'
        collection = self.db.staging_jobs
        record_id = str(collection.insert(utils.make_job(username, jamo_id, filename)))
        return record_id

    def remove_job(self, req):
        'remove a job from the jobs database'
        collection = self.db.staging_jobs

        result = collection.find_and_modify(query={'username': req['username'], '_id': ObjectId(req['job_monitoring_id'])}, remove=True)
        json_result = {'job_monitoring_id': json.loads(json_util.dumps(result))}
        return [json_result, None]
    

    def job_submitted(self, record_id, job_id):
        'set the state for this job to "submitted"'
        collection = self.db.staging_jobs
        collection.update(
            {'_id': ObjectId(record_id)},
            {'$set': {
                'updated': calendar.timegm(time.gmtime()), 
                'job_id': job_id, 
                'status_code': 'submitted', 
                'status_raw': 'submitted'
                }   
            })

    def get_job_status(self, job_id):
        request = {'id': job_id}
        ctx = {
            'method': 'get',
            'connection_timeout': self.connection_timeout,
            'url': self.jgi_search_base_url,
            'user': self.user,
            'password': self.password,
            'type': 'text'
        }
        response, error, stats = utils.sendRequest('status', request, ctx)
        if error != None:
            return [None, error]

        translated, error = self.translate_job_status(response)
        if error != None:
            return [None, {
                'message': 'Invalid job status message',
                'job_status_message': response,
                'reported_error': error
            }]

        return [{
            'job_id': job_id,
            'code': translated, 
            'raw': response
        }, None]

    def update_job_status(self, job_monitoring_id, status_code, status_raw):
        self.db.staging_jobs.update(
                {'_id': ObjectId(job_monitoring_id)},
                {'$set': {
                    'updated': calendar.timegm(time.gmtime()), 
                    'status_code': status_code, 
                    'status_raw': status_raw
                    }
                })


    def get_jobs_status(self, job_ids): 

        # get a futures session
        session = FuturesSession(max_workers=3)

        ctx = {
            'method': 'get',
            'connection_timeout': self.connection_timeout,
            'url': self.jgi_search_base_url,
            'user': self.user,
            'password': self.password,
            'type': 'text'
        }

        # create N requests for N job ids

        # loop through then and get the results. although each item blocks,
        # the io is continuing in the background. The loop really then 
        # just ensures that each future completes before continuing
        # past the loop.
        # This implies that this entire method blocks, which is ok
        # since we are running the monitor in its own thread 

        job_status_requests = map(lambda job_id: [job_id, utils.sendFRequest(session, 'status', {'id': job_id}, ctx)], job_ids)

        result = []
        for job_id, request in job_status_requests:
            response, error, stats = utils.processFRequest(request)
            if error != None:
                result.append([None, {
                    'job_id': job_id,
                    'error': error
                }])
            else:
                status_code, error = self.translate_job_status(response)
                if error == None:
                    result.append([{
                        'job_id': job_id,
                        'code': status_code,
                        'raw': response
                    }, None])
                else:
                    result.append([None, {
                        'job_id': job_id,
                        'error': error,
                        'job_status_message': response
                    }])

        return result

    def sync_active_jobs(self):
        pending_jobs_filter = {
            'status_code': {'$in': ['queued',  'submitted', 'restoring', 'copying']}
        }
        jobs_to_update = []
        jobs_awaiting_update = {}
        for job in self.db.staging_jobs.find(pending_jobs_filter):
            jobs_to_update.append(job['job_id'])
            jobs_awaiting_update[job['job_id']] = job

        for result, error in self.get_jobs_status(jobs_to_update):
            if result != None:
                awaiting_job = jobs_awaiting_update[result['job_id']]
                # only update the status if it changed. This keeps the update
                # date meaningful.
                if awaiting_job['status_code'] != result['code']:
                    self.update_job_status(str(awaiting_job['_id']), result['code'], result['raw'])
            else:
                print('ERROR getting job stats')
                print(error)
        
        return jobs_to_update, None
