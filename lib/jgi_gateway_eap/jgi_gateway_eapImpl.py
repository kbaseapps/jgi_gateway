# -*- coding: utf-8 -*-
#BEGIN_HEADER
"""
JGI Gateway Service
"""

import os
import json
import sys
import time
import calendar
import re
import utils
# from pymongo import MongoClient
# from bson.json_util import dumps
from bson import json_util
from .staging_jobs_manager import StagingJobsManager
from .jgi_gateway_eapServerContext import ServerContext

#END_HEADER


class jgi_gateway_eap:
    '''
    Module Name:
    jgi_gateway_eap

    Module Description:
    A KBase module: jgi_gateway_eap
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.2.0"
    GIT_URL = "ssh://git@github.com/eapearson/jgi_gateway"
    GIT_COMMIT_HASH = "36c365bfd83f2d7839934bc6a2caf1fbf6b312bd"

    #BEGIN_CLASS_HEADER


# class ServerContext(object):
#     'Provides functions only the server can'
#     def __init__(self, uwsgi_avail):
#         self.uwsgi_available = uwsgi_avail
        
#     def send_message(self, msg):
#         if self.uwsgi_available:
#             uwsgi.mule_msg(msg)
#         else:
#             print('warning: uwsgi not available')

#     def is_uwsgi_available(self):
#         return self.uwsgi_available

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        """
        default constructor
        """

        # Note - config errors are not caught here, but when the
        # config would be used.
        # TODO: it is cleaner to do it here, but not sure how well
        # it plays with module lifecycle.
        self.context = ServerContext()

        self.config = utils.validate_config(config)
       
        self.staging_jobs_manager = StagingJobsManager(self.config)

        self.context.send_message('start-job-monitoring')

        #END_CONSTRUCTOR
        pass


    def search(self, ctx, parameter):
        """
        The search function takes a search structure and returns a list of
        documents.
        :param parameter: instance of type "SearchInput" (search searches the
           JGI service for matches against the query, which may be a string
           or an object mapping string->string query - Other parameters
           @optional filter @optional limit @optional page @optional
           include_private) -> structure: parameter "query" of type
           "SearchQuery" -> mapping from String to String, parameter "filter"
           of type "SearchFilter" (SearchFilter The jgi back end takes a map
           of either string, integer, or array of integer. I don't think the
           type compiler supports union types, so unspecified it is.) ->
           mapping from String to unspecified object, parameter "sort" of
           list of type "SortSpec" -> structure: parameter "field" of String,
           parameter "descending" of Long, parameter "limit" of Long,
           parameter "page" of Long, parameter "include_private" of type
           "bool" (a bool defined as int)
        :returns: multiple set - (1) parameter "result" of type
           "SearchResult" -> structure: parameter "search_result" of type
           "SearchQueryResult" (SearchQueryResult The top level search object
           returned from the query. Note that this structure closely
           parallels that returned by the jgi search service. The only
           functional difference is that some field names which were prefixed
           by underscore are known by their unprefixed selfs. hits  - a list
           of the actual search result documents and statsitics returned;;
           note that this represents the window of search results defined by
           the limit input property. total - the total number of items
           matched by the search; not the same as the items actually
           returned;) -> structure: parameter "hits" of list of type
           "SearchResultItem" (SearchResult Represents a single search result
           item) -> structure: parameter "source" of type "SearchDocument"
           (SearchDocument The source document for the search; it is both the
           data obtained by the search as well as the source of the index. It
           is the entire metadata JAMO record.) -> unspecified object,
           parameter "index" of String, parameter "score" of String,
           parameter "id" of String, parameter "total" of Long, (2) parameter
           "error" of type "Error" -> structure: parameter "message" of
           String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object, (3) parameter "stats" of
           type "CallStats" (Call performance measurement) -> structure:
           parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, error, stats
        #BEGIN search

        # BASIC config
        # error = utils.validateCallConfig(self);
        # if error:
        #     return [None, error, None]


        # INPUT
        call_start = time.clock()

        query, error = utils.validateSearchParameter(parameter, ctx)
        if error:
            return [None, error, None]

        # PREPARE REQUEST
        responsejson, error, stats = utils.sendRequest('query', query, {
            'method': 'post',
            'connection_timeout': self.config['jgi']['connection-timeout'],
            'url': self.config['jgi']['base-url'],
            'user': self.config['jgi']['user'],
            'password': self.config['jgi']['password'],
        })

        if responsejson:
            new_hits = []

            for hit in responsejson['hits']:
                new_hits.append({
                    'source': hit['_source'],
                    'index': hit['_index'],
                    'score': hit['_score'],
                    'id': hit['_id']
                })
            result = {
                'hits': new_hits,
                'total': responsejson['total']
            }
        else:
            result = None

        return [result, error, stats]

        # We need to transform the result into a form that is acceptable to
        # KIDL.


        #END search

        # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method search return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method search return value ' +
        #                      'error is not type dict as required.')
        # if not isinstance(stats, dict):
        #     raise ValueError('Method search return value ' +
        #                      'stats is not type dict as required.')
        # # return the results
        # return [result, error, stats]

    def stage(self, ctx, parameter):
        """
        :param parameter: instance of type "StageInput" -> structure:
           parameter "file" of type "StageRequest" (STAGE) -> structure:
           parameter "id" of String, parameter "filename" of String,
           parameter "username" of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingResult" (StagingResult returns a map entry for each id
           submitted in the stage request. The map key is the _id property
           returned in a SearchResult item (not described here but probably
           should be), the value is a string describing the result of the
           staging request. At time of writing, the value is always "staging"
           since the request to the jgi gateway jgi service and the call to
           stage in the jgi gateway kbase service are in different
           processes.) -> structure: parameter "job_id" of String, (2)
           parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object, (3) parameter
           "stats" of type "CallStats" (Call performance measurement) ->
           structure: parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, error, stats
        #BEGIN stage

        # error = utils.validateCallConfig(self);
        # if error:
        #     return [None, error, None]

        # INPUT
        request, error = utils.validateFetchParameter(parameter, ctx)
        if error:
            return [None, error, None]

        # Create the job record in advance of the actual request... good idea?
        record_id = self.staging_jobs_manager.add_job(parameter['file']['username'], parameter['file']['id'], parameter['file']['filename'])

        responsejson, error, stats = utils.sendRequest('fetch', request,  {
            'method': 'post',
            'connection_timeout': self.config['jgi']['connection-timeout'],
            'url': self.config['jgi']['base-url'],
            'user': self.config['jgi']['user'],
            'password': self.config['jgi']['password'],
        })

        if responsejson:
            #
            # Note that the response returns a single job id, regardless
            # of the number of ids in the copy request.
            #
            job_id = responsejson['id']
    
            # Update the job record to indicate that it has been submitted.
            # The monitor will update the status from the jgi service
            # itself.
            self.staging_jobs_manager.job_submitted(record_id, job_id)

            print('putting start message in monitor queue...')
            self.context.send_message('start-job-monitoring')

            result = {'job_id': job_id}
        # elif error TODO: handle error here
        else:
            result = None

        return [result, None, stats]

        # NOTE: we are already returned here, the code below is dead.

        #END stage

        # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method stage return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method stage return value ' +
        #                      'error is not type dict as required.')
        # if not isinstance(stats, dict):
        #     raise ValueError('Method stage return value ' +
        #                      'stats is not type dict as required.')
        # # return the results
        # return [result, error, stats]

    def stage_status(self, ctx, parameter):
        """
        Fetch the current status of the given staging fetch request as 
        identified by its job id
        :param parameter: instance of type "StagingStatusInput" -> structure:
           parameter "job_id" of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingStatusResult" -> structure: parameter "message" of String,
           (2) parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object, (3) parameter
           "stats" of type "CallStats" (Call performance measurement) ->
           structure: parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, error, stats
        #BEGIN stage_status

        # error = utils.validateCallConfig(self);
        # if error:
        #     return [None, error, None]


        # INPUT
        request, error = utils.validateStageStatusParameter(parameter, ctx)
        if error:
            return [None, error, None]

        response, error, stats = utils.sendRequest('status', request,  {
            'method': 'get',
            'connection_timeout': self.config['jgi']['connection-timeout'],
            'url': self.config['jgi']['base-url'],
            'user': self.config['jgi']['user'],
            'password': self.config['jgi']['password'],
            'type': 'text'
        })

        return [response, error, stats]

        # NOTE: we are already returned here, the code below is dead.
        #END stage_status

        # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method stage_status return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method stage_status return value ' +
        #                      'error is not type dict as required.')
        # if not isinstance(stats, dict):
        #     raise ValueError('Method stage_status return value ' +
        #                      'stats is not type dict as required.')
        # # return the results
        # return [result, error, stats]

    def staging_jobs(self, ctx, parameter):
        """
        Fetch all file staging jobs for the current user
        :param parameter: instance of type "StagingJobsInput" -> structure:
           parameter "filter" of type "StagingJobsFilter" -> structure:
           parameter "created_from" of type "timestamp", parameter
           "created_to" of type "timestamp", parameter "updated_from" of type
           "timestamp", parameter "updated_to" of type "timestamp", parameter
           "status" of String, parameter "jamo_id" of String, parameter
           "job_ids" of list of String, parameter "filename" of String,
           parameter "range" of type "StagingJobsRange" -> structure:
           parameter "start" of Long, parameter "limit" of Long, parameter
           "sort" of list of type "SortSpec" -> structure: parameter "field"
           of String, parameter "descending" of Long
        :returns: multiple set - (1) parameter "result" of type
           "StagingJobsResult" -> structure: parameter "staging_jobs" of list
           of type "StagingJob" -> structure: parameter "jamo_id" of String,
           parameter "filename" of String, parameter "username" of String,
           parameter "job_id" of String, parameter "status_code" of String,
           parameter "status_raw" of String, parameter "created" of type
           "timestamp", parameter "updated" of type "timestamp", parameter
           "total_matched" of Long, parameter "total_jobs" of Long, (2)
           parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object, (3) parameter
           "stats" of type "CallStats" (Call performance measurement) ->
           structure: parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, error, stats
        #BEGIN staging_jobs
        # error = utils.validateCallConfig(self);
        # if error:
        #     return [None, error, None]


        # INPUT
        # error = utils.validateCallConfig(self);
        # if error:
        #     return [None, error, None]

        # INPUT
        request, error = utils.validate_staging_jobs_parameter(parameter, ctx)
        if error:
            return [None, error, None]

        response = self.staging_jobs_manager.staging_jobs_for_user(request)

        return [response, None, None]
        #END staging_jobs

        # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method staging_jobs return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method staging_jobs return value ' +
        #                      'error is not type dict as required.')
        # if not isinstance(stats, dict):
        #     raise ValueError('Method staging_jobs return value ' +
        #                      'stats is not type dict as required.')
        # # return the results
        # return [result, error, stats]

    def staging_jobs_summary(self, ctx, parameter):
        """
        Fetch the # of transfers in each state
        :param parameter: instance of type "StagingJobsSummaryInput" ->
           structure: parameter "username" of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingJobsSummaryResult" -> structure: parameter "state" of
           mapping from String to type "StagingJobsSummary" -> structure:
           parameter "label" of String, parameter "count" of Long, (2)
           parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object, (3) parameter
           "stats" of type "CallStats" (Call performance measurement) ->
           structure: parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, error, stats
        #BEGIN staging_jobs_summary
        request, error = utils.validate_staging_jobs_summary_parameter(parameter, ctx)
        if error:
            return [None, error, None]

        response = self.staging_jobs_manager.get_jobs_summary_for_user(request)

        return [response, None, None]
        #END staging_jobs_summary

        # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method staging_jobs_summary return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method staging_jobs_summary return value ' +
        #                      'error is not type dict as required.')
        # if not isinstance(stats, dict):
        #     raise ValueError('Method staging_jobs_summary return value ' +
        #                      'stats is not type dict as required.')
        # # return the results
        # return [result, error, stats]
    def status(self, ctx):
        #BEGIN_STATUS

        result = {
            'state': 'OK',
            'message': 'The system is operating normally',
            'version': self.VERSION,
            'git_url': self.GIT_URL,
            'git_commit_hash': self.GIT_COMMIT_HASH
        }

        return [result, None, None]
        #END_STATUS
        # return [returnVal]
