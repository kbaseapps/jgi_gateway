# -*- coding: utf-8 -*-
import os  # noqa: F401
import time
import unittest
from configparser import ConfigParser  # py3
from os import environ

from installed_clients.WorkspaceClient import Workspace as workspaceService
from jgi_gateway.authclient import KBaseAuth as _KBaseAuth
from jgi_gateway.jgi_gatewayImpl import jgi_gateway
from jgi_gateway.jgi_gatewayServer import MethodContext


class jgi_gatewayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        if not isinstance(token, str):
            raise ValueError
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('jgi_gateway'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'jgi_gateway',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})

        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        # context = ServerContext()
        cls.serviceImpl = jgi_gateway(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        print('starting to build local mongoDB')
        os.system("sudo service mongodb start")
        os.system("mongod --version")
        os.system("cat /var/log/mongodb/mongodb.log "
                  "| grep 'waiting for connections on port 27017'")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = 'test_jgi_gateway_' + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    # These tests cover the simple cases of the control parameters.
    def test_search_simple(self):
        # Test default result size of 10 for the given user and a wildcard
        # that should give us everything.
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        query = {'query': {'_all': '*'}, 'sort': sort}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        self.assertEqual(len(ret['hits']), 10)

        # Test an explicit limit of 20, still for wildcard
        query = {'query': {'_all': '*'}, 'sort': sort, 'limit': 20}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        self.assertEqual(len(ret['hits']), 20)

        # Test the same query, this time fetching the second page of hits
        query = {'query': {'_all': '*'}, 'sort': sort, 'limit': 20, 'page': 1}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        self.assertEqual(len(ret['hits']), 20)

    # Input values good and at the edges
    # For now just test that error is None and result is not None.
    def test_search_input_validation(self):
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        tests = [
            # query
            [{'query': {'_all': '*'}, 'sort': sort}, 'bog simple search'],
            # filter
            [{'query': {'_all': '*'}, 'sort': sort, 'filter': {'file_type': 'fastq'}}, 'with one file type'],
            [{'query': {'_all': '*'}, 'sort': sort, 'filter': {'file_type': 'fastq | fasta'}}, 'with two file types'],            
            [{'query': {'_all': '*'}, 'sort': sort, 'filter': None}, 'with filter null'],
            # fields
            [{'query': {'_all': '*'}, 'sort': sort, 'fields': None}, 'with fields null'],
            [{'query': {'_all': '*'}, 'sort': sort, 'fields': ['file_type']}, 'with fields set to one valid field'],
            # limit
            [{'query': {'_all': '*'}, 'sort': sort, 'limit': None}, 'with limit null'],
            [{'query': {'_all': '*'}, 'sort': sort, 'limit': 1}, 'with limit set to lower limit: 1'],
            [{'query': {'_all': '*'}, 'sort': sort, 'limit': 1000}, 'with limit set to upper limit: 1,000'],
            # page
            [{'query': {'_all': '*'}, 'sort': sort, 'page': None}, 'with page null'],
            [{'query': {'_all': '*'}, 'sort': sort, 'page': 1}, 'with page at lower limit: 1'],
            [{'query': {'_all': '*'}, 'sort': sort, 'page': 1000}, 'with page at upper limit: 1,000'],
            # include_private
            [{'query': {'_all': '*'}, 'sort': sort, 'include_private': None}, 'with include private null'],
            [{'query': {'_all': '*'}, 'sort': sort, 'include_private': 0}, 'with include_private at lower bound: 0'],
            [{'query': {'_all': '*'}, 'sort': sort, 'include_private': 1}, 'with include_private at upper bound: 1']
        ]
        for query, msg in tests:
            ret, err, status = self.getImpl().search(self.getContext(), query)
            # if err:
            #     print('test search input validation')
            #     print(err)
            self.assertIsNotNone(ret, 'return is not none: ' + msg)
            self.assertIsNone(err, 'err is none: ' + msg)
            self.assertIsNotNone(status, 'status is not none: ' + msg)

    def test_page_at_limit(self):
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        # Test the same query, this time fetching the second page of hits
        query = {'query': {'_all': '*'}, 'sort': sort, 'limit': 20, 'page': 1}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret, err)
        self.assertIn('hits', ret)
        self.assertEqual(len(ret['hits']), 20)            

    # Stats
    def test_search_timing_stats(self):
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        tests = [
            # query
            [{'query': {'_all': '*'}, 'sort': sort}],
        ]
        for query, in tests:
            ret, err, status = self.getImpl().search(self.getContext(), query)
            self.assertIsNotNone(status)

            self.assertIn('request_elapsed_time', status)
            req_elapsed = status['request_elapsed_time']
            self.assertIsInstance(req_elapsed, int)

    # Trigger input validation errors
    def test_search_input_validation_errors(self):
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        tests = [
            [{'sort': sort}, 'missing', 'query'],
            [{'query': 'i am wrong', 'sort': sort}, 'wrong-type', 'query'],
            [{'query': {'_all': '*'}, 'sort': sort, 'filter': 1}, 'wrong-type', 'filter'],
            [{'query': {'_all': '*'}, 'sort': sort, 'fields': 'x'}, 'wrong-type', 'fields'],
            [{'query': {'_all': '*'}, 'sort': sort, 'limit': 'x'}, 'wrong-type', 'limit'],
            [{'query': {'_all': '*'}, 'sort': sort, 'limit': 0}, 'invalid', 'limit'],
            [{'query': {'_all': '*'}, 'sort': sort, 'limit': 1001}, 'invalid', 'limit'],
            [{'query': {'_all': '*'}, 'sort': sort, 'page': 'x'}, 'wrong-type', 'page'],
            [{'query': {'_all': '*'}, 'sort': sort, 'page': 0}, 'invalid', 'page'],
            [{'query': {'_all': '*'}, 'sort': sort, 'page': 1001}, 'invalid', 'page'],
            [{'query': {'_all': '*'}, 'sort': sort, 'include_private': 'x'}, 'wrong-type', 'include_private'],
            [{'query': {'_all': '*'}, 'sort': sort, 'include_private': -1}, 'invalid', 'include_private'],
            [{'query': {'_all': '*'}, 'sort': sort, 'include_private': 2}, 'invalid', 'include_private']
        ]
        for query, error_code, error_key in tests:
            ret, err, status = self.getImpl().search(self.getContext(), query)
            self.assertIsNone(ret)
            self.assertIsNone(status)
            self.assertIsInstance(err, dict)
            self.assertEqual(err['type'], 'input')
            self.assertEqual(err['code'], error_code)
            self.assertEqual(err['info']['key'], error_key)

    # Test control parameters at, just under, just over the limits.
    # Test the return structure using the simplest query and all default
    # control parameters.
    def test_search_return_structure(self):
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        query = {'query': {'_all': '*'}, 'sort': sort}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        hits = ret['hits']
        self.assertIsInstance(hits, list)
        self.assertEqual(len(hits), 10)
        a_hit = hits[0]
        self.assertIsInstance(a_hit, dict)
        self.assertIn('total', ret)
        total = ret['total']
        self.assertIsInstance(total, int)
        for key in ['source', 'index', 'score', 'id']:
            self.assertIn(key, a_hit)
        source = a_hit['source']
        self.assertIsInstance(source, dict)
        index = a_hit['index']
        self.assertIsInstance(index, str)
        # Note that score is None when sorting.
        # Hmm, maybe we do want to be able to turn sorting off?
        score = a_hit['score']
        # self.assertIsInstance(score, float)
        self.assertIsNone(score)
        hitid = a_hit['id']
        self.assertIsInstance(hitid, str)

    # Test the error structure.
    # Use a
    # def test_search_error_structure(self):
    #     query = {}

    # Test staging
    def test_stage(self):
        # req = {'files': [{
        #         'id': '51d4fa27067c014cd6ed1a90', 
        #         'filename': 'file1'
        #     }, {
        #         'id': '51d4fa27067c014cd6ed1a96',
        #         'filename': 'file2'
        #     }]}
        username = self.getContext()['user_id']
        req = {
            'file': {
                'id': '51d4fa27067c014cd6ed1a90', 
                'filename': 'file1',
                'username': username
            }
        }
        ret, error, status = self.getImpl().stage(self.getContext(), req)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)
        self.assertIn('job_id', ret)
        job_id = ret['job_id']
        self.assertIsInstance(job_id, str)

    def test_stage_and_status(self):
        # req = {'files': [{
        #         'id': '5786eec57ded5e34bd91fa63',
        #         'filename': 'file3'
        #     }]}
        username = self.ctx['user_id']
        req = {
            'file': {
                'id': '5786eec57ded5e34bd91fa63',
                'filename': 'file3',
                'username': username
            }
        }
        ret, error, status = self.getImpl().stage(self.getContext(), req)
        # print(error)
        self.assertIsNotNone(ret)
        self.assertIsNone(error)
        self.assertIsInstance(ret, dict)
        self.assertIn('job_id', ret)
        job_id = ret['job_id']
        self.assertIsInstance(job_id, str)
        req = {'job_id': job_id}
        ret, error, status = self.getImpl().stage_status(self.getContext(), req)
        self.assertIsNotNone(ret)
        self.assertIsNone(error)
        self.assertIsInstance(ret, str)

    # Test staging validation errors

    # Trigger input validation errors
    def test_stage_input_validation(self):
        # tests = [
        #     [{}, 'missing', 'files'],
        #     [{'files': 'x'}, 'wrong-type', 'files'],
        #     [{'files': [{'x': 'x', 'filename': 'y'}]}, 'missing', ['files', 0, 'id'] ],
        #     [{'files': [{'id': 'x', 'x': 'y'}]}, 'missing', ['files', 0, 'filename'] ],
        #     [{'files': [{'id': 1, 'filename': 'y'}]}, 'wrong-type', ['files', 0, 'id'] ],
        #     [{'files': [{'id': 'x', 'filename': 1}]}, 'wrong-type', ['files', 0, 'filename'] ]
        # ]
        tests = [
            [{}, 'missing', 'file'],
            [{'file': 'x'}, 'wrong-type', 'file'],

            [{'file': {'x': 'x', 'filename': 'y', 'username': 'z'}}, 'missing', ['file', 'id'] ],
            [{'file': {'id': 'x', 'x': 'y', 'username': 'z'}}, 'missing', ['file', 'filename'] ],
            [{'file': {'id': 'x', 'filename': 'y', 'a': 'z'}}, 'missing', ['file', 'username'] ],

            [{'file': {'id': 1,   'filename': 'y', 'username': 'z'}}, 'wrong-type', ['file', 'id'] ],
            [{'file': {'id': 'x', 'filename': 1,   'username': 'z'}}, 'wrong-type', ['file', 'filename'] ],
            [{'file': {'id': 'x', 'filename': 'y', 'username': 1}},   'wrong-type', ['file', 'username'] ]
        ]
        for req, error_code, error_key in tests:
            ret, err, status = self.getImpl().stage(self.getContext(), req)
            #   ret, err, status = self.getImpl().stage(self.getContext(), param)
            self.assertIsNone(ret)
            self.assertIsNone(status)
            self.assertIsInstance(err, dict)
            self.assertEqual(err['type'], 'input')
            self.assertEqual(err['code'], error_code)
            self.assertEqual(err['info']['key'], error_key)

    def test_stage_status_input_validation(self):
        tests = [
            [{}, 'missing', 'job_id'],
            [{'job_id': 1}, 'wrong-type', 'job_id']
        ]
        for req, error_code, error_key in tests:
            ret, err, status = self.getImpl().stage_status(self.getContext(), req)
            #   ret, err, status = self.getImpl().stage(self.getContext(), param)
            self.assertIsNone(ret)
            self.assertIsNone(status)
            self.assertIsInstance(err, dict)
            self.assertEqual(err['type'], 'input')
            self.assertEqual(err['code'], error_code)
            self.assertEqual(err['info']['key'], error_key)

    def test_status(self):
        ret, err, status = self.getImpl().status(self.getContext())
        self.assertEqual(ret['state'], 'OK')

    # # These tests cover the simple cases of the control parameters.
    def test_search_timeout(self):
        # Test default result size of 10 for the given user and a wildcard
        # that should give us everything.
        impl = self.getImpl()
        original_timeout = impl.config['jgi']['connection-timeout']
        test_timeout = 0.0001
        impl.config['jgi']['connection-timeout'] = test_timeout
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        query = {'query': {'_all': '*'}, 'sort': sort}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNone(ret)
        self.assertIsNotNone(err)
        self.assertEqual(err['info']['timeout'], test_timeout)
        self.assertEqual(err['type'], 'network')
        self.assertEqual(err['code'], 'connection-timeout')
        impl.config['jgi']['connection-timeout'] = original_timeout

    # This test may need to be commented out sometimes; it is possible
    # that async network requests are tripping over each other, and we
    # are changing the implementation config, which may screw up
    # concurrent tests.
    def test_search_bad_host(self):
        # Test default result size of 10 for the given user and a wildcard
        # that should give us everything.
        impl = self.getImpl()
        original_url = impl.config['jgi']['base-url']
        bad_url = original_url + 'x'
        impl.config['jgi']['base-url'] = bad_url
        sort = [
            {
                'field': 'modified',
                'descending': 1
            }
        ]
        query = {'query': {'_all': '*'}, 'sort': sort}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNone(ret)
        self.assertIsNotNone(err)
        # self.assertEquals(err['info']['timeout'], test_timeout)
        self.assertEqual(err['type'], 'network')
        self.assertEqual(err['code'], 'connection-error')
        impl.config['jgi']['base-url'] = original_url

    def test_staging_jobs(self):
        # First stage a file.
        req1 = {'file': {
                'id': '51d4fa27067c014cd6ed1a90', 
                'filename': 'file1',
                'username': self.ctx['user_id']
            }}
        ret, error, status = self.getImpl().stage(self.getContext(), req1)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)
        self.assertIn('job_id', ret)
        job_id = ret['job_id']
        self.assertIsInstance(job_id, str)

        # Now fetch the staging job
        req2 = {
            'username': self.ctx['user_id'],
            'filter': {
                'job_ids': [job_id]
            },
            'range': {
                'start': 0,
                'limit': 1
            }
        }
        ret, error, status = self.getImpl().staging_jobs(self.getContext(), req2)
        self.assertIsNotNone(ret)
        self.assertIsNone(error)
        self.assertIsInstance(ret, dict)
        self.assertIn('jobs', ret)
        jobs = ret['jobs']
        self.assertIsInstance(jobs, list)
        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertIsInstance(job, dict) 
        self.assertIn('filename', job)
        filename = job['filename']
        self.assertEqual(filename, 'file1')

    @unittest.skip("Only eric can run this test ATM")
    def test_staging_jobs2(self):
        # TODO: set up various staging jobs...
        reqs = [
            {
                'params': {
                    'username': 'eapearson',
                    'filter': {
                        'job_ids': ['JOB_315']
                    },
                    'range': {
                        'start': 0,
                        'limit': 1
                    }
                },
                'expected': 1
            },
            {
                'params': {
                    'username': 'eapearson',
                    'filter': {
                        'job_statuses': ['completed']
                    },
                    'range': {
                        'start': 0,
                        'limit': 1
                    }
                },
                'expected': 1
            }
        ]

        for req in reqs:
            ret, error, status = self.getImpl().staging_jobs(self.getContext(), req['params'])
            self.assertIsNotNone(ret, error)
            self.assertIsNone(error)
            self.assertIsInstance(ret, dict)
            self.assertIn('jobs', ret)
            jobs = ret['jobs']
            self.assertIsInstance(jobs, list)
            self.assertEqual(len(jobs), req['expected'])

    def test_staging_jobs3(self):
        # First stage a file.
        req1a = {'file': {
                'id': '51d4fa27067c014cd6ed1a90', 
                'filename': 'file1a',
                'username': self.ctx['user_id']
            }
        }
        ret, error, status = self.getImpl().stage(self.getContext(), req1a)
        self.assertIsNotNone(ret, error)
        self.assertIsInstance(ret, dict)
        self.assertIn('job_id', ret)
        job_id_1a= ret['job_id']
        self.assertIsInstance(job_id_1a, str)

        req1b = {'file': {
                'id': '51d4fa27067c014cd6ed1a90', 
                'filename': 'file1b',
                'username': self.ctx['user_id']
            }
        }
        ret, error, status = self.getImpl().stage(self.getContext(), req1b)
        self.assertIsNotNone(ret, error)
        self.assertIsInstance(ret, dict)
        self.assertIn('job_id', ret)
        job_id_1b = ret['job_id']
        self.assertIsInstance(job_id_1b, str)

        # Now fetch the staging job
        req2 = {
            'username': self.ctx['user_id'],
            'filter': {
                'job_ids': [job_id_1a, job_id_1b]
            },
            'range': {
                'start': 0,
                'limit': 2
            }
        }
        ret, error, status = self.getImpl().staging_jobs(self.getContext(), req2)
        self.assertIsNotNone(ret, error)
        self.assertIsNone(error)
        self.assertIsInstance(ret, dict)
        self.assertIn('jobs', ret)
        jobs = ret['jobs']
        self.assertIsInstance(jobs, list)
        self.assertEqual(len(jobs), 2)
        job_1a = [x for x in jobs if x['job_id'] == job_id_1a]
        self.assertIsInstance(job_1a, list) 
        self.assertIs(len(job_1a), 1)
        self.assertIn('filename', job_1a[0])
        filename = job_1a[0]['filename']
        self.assertEqual(filename, 'file1a')        
        
    def test_staging_jobs_monitor_job_status_happy(self):
        # TODO: Arrange jobs in various states ... tricky!

        req = [
            ['JOB_8', 'completed'],
            ['JOB_XXX', 'notfound']
        ]
        for job_id, expected_status in req:
            ret, error = self.getImpl().staging_jobs_manager.get_job_status(job_id)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict)
            self.assertIn('job_id', ret)
            job_id = ret['job_id']
            self.assertIsInstance(job_id, str)
            self.assertIn('code', ret)
            status = ret['code']
            self.assertIsInstance(status, str)
            self.assertEqual(status, expected_status)
            
    def test_sync_active_jobs(self):
        # TODO: First stage a file.

        req = {}
        ret, error = self.getImpl().staging_jobs_manager.sync_active_jobs()
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, list)

        # self.assertIn('job_id', ret)
        # job_id = ret['job_id']
        # self.assertIsInstance(job_id, basestring)
        # self.assertIn('status', ret)
        # status = ret['code']
        # self.assertIsInstance(status, basestring)
        # self.assertIs(status, 'completed')        

    def test_staging_jobs_status_happy(self):
        # TODO: First stage a file.

        req = ['JOB_8', 'JOB_9', 'JOB_10', 'JOB_11']
        ret = self.getImpl().staging_jobs_manager.get_jobs_status(req)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, list)

    # def test_staging_jobs_status_sad(self):
    #     # TODO: First stage a file.

    #     req = ['JOB_XXX']
    #     ret = self.getImpl().staging_jobs_manager.get_jobs_status(req)
    #     print(ret)
    #     print(error)
    #     self.assertIsNotNone(ret)
    #     self.assertIsInstance(ret, list)
        

    def test_status_parsing_happy(self):
        reqs = [
            [
                'In_Queue',
                'queued'
            ],
            [
                'Transfer Complete. Transfered 1 files.',
                'completed'
            ],
            [
                'In Progress. Total files = 1. Copy complete = 0. Restore in progress = 0. Copy in progress = 1',
                'copying'
            ],
            [
                'In Progress. Total files = 1. Copy complete = 1. Restore in progress = 0. Copy in progress = 0',
                'completed'
            ],
            [
                'In Progress. Total files = 1. Copy complete = 0. Restore in progress = 1. Copy in progress = 0',
                'restoring'
            ],
            [
                'Error: No such Id',
                'notfound'
            ]
        ]
        # TODO: not found.
        # [
        #     'Transfer Complete. Transfered 0 files. Scp failed for files = \[u'(.*?)'\]',
        #     'error'
        # ]
        for message, expected_status in reqs:
            status, error = self.getImpl().staging_jobs_manager.translate_job_status(message)
            # if error != None:
            #     print(message)
            #     print(error)
            self.assertIsNotNone(status)
            self.assertIsInstance(status, str)
            self.assertEqual(status, expected_status)

    def test_status_parsing_sad(self):
        reqs = [
            [
                'abc',
                'queued'
            ]
        ]
        for message, expected_status in reqs:
            status, error = self.getImpl().staging_jobs_manager.translate_job_status(message)
            self.assertIsNotNone(error)
            self.assertIsInstance(error, str)

    # def test_monitoring_happy(self):
    #     print('monitoring happy story')
    #     instance = self.getImpl().staging_jobs_monitor
    #     self.assertEqual(instance.job_checks, 0)
    #     # monitor count should be 0
    #     instance.message_queue.put('start')
    #     time.sleep(5)
    #     self.assertEqual(instance.job_checks, 1)
    #     time.sleep(10)
    #     self.assertEqual(instance.job_checks, 2)
    #     print('monitoring happy?')
    #     print(instance.job_checks)
    #     # wait 15 seconds
    #     # count  should be 1

    def test_staging_jobs_summary(self):
        req = {
            'username': self.getContext()['user_id']
        }
        ret = self.getImpl().staging_jobs_manager.get_jobs_summary_for_user(req)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)

    def test_staging_jobs_summary_happy(self):
        params = {
            'username': self.getContext()['user_id'],
            'job_monitoring_ids': []
        }

        ret, error, status = self.getImpl().staging_jobs_summary(self.getContext(), params)

        self.assertIsNotNone(ret)
        self.assertIsNone(error)
        self.assertIsInstance(ret, dict)
        self.assertIn('states', ret)
        state = ret['states']
        self.assertIsInstance(state, dict)
