# -*- coding: utf-8 -*-
#BEGIN_HEADER
"""
JGI Gateway Service
"""

import os
import requests
import json
import sys
import time
import re
import math
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
    GIT_COMMIT_HASH = "aa94fa16e4695bff10a53d3537f1c62192d70359"

    #BEGIN_CLASS_HEADER
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
        self.config = config
        self.user = None
        self.passwd = None

        # Import and validate the jgi host
        if 'jgi-search-base-url' not in config:
            raise(ValueError('"jgi-search-base-url" configuration property not provided'))
        # The host must be secure, and be reasonably valid:
        # https://a.b
        if (not re.match("^https://.+?\\..+$", config['jgi-search-base-url'])):
            raise(ValueError('"jgi-host" configuration property not a valid url base'))

        self.jgi_search_base_url = config['jgi-search-base-url']

        print("Using jgi base url: %s" % (self.jgi_search_base_url))


        # Import and validate the jgi token
        if 'jgi-token' not in config:
            raise(ValueError('"jgi-token" configuration property not provided'))

        token = config['jgi-token'].split(':')
        if (len(token) != 2):
            raise(ValueError('"jgi-token" configuration property is invalid'))

        (user, passwd) = token

        # Given a string which can split, the worst we can have is an empty
        # part, since we are ensured to get at least a 0-length string
        if ((len(user) == 0) or (len(passwd) == 0)):
            raise(ValueError('"jgi-token" configuration property is invalid'))

        self.user = user
        self.passwd = passwd

        # Import and validate the connection timeout
        if 'connection-timeout' not in config:
            raise(ValueError('"connection-timeout" configuration property not provided'))
        try:
            connection_timeout = int(config['connection-timeout'])
        except ValueError as ex:
            raise(ValueError('"connection-timeout" configuration property is not a float: ' + str(ex)))
        if not (config['connection-timeout'] > 0):
            raise(ValueError('"connection-timeout" configuration property must be > 0'))

        self.connection_timeout = float(connection_timeout) /float(1000)
        print('connection timeout %f sec' % (self.connection_timeout) )

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
           mapping from String to unspecified object, parameter "limit" of
           Long, parameter "page" of Long, parameter "include_private" of
           type "bool" (a bool defined as int)
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

        # INPUT
        call_start = time.clock()
        # query
        # A required property, this provides the, well, search to conduct
        # over the jgi search service space.
        # Note that the sender may simply send '*' to fetch all results.
        #
        if 'query' not in parameter:
            error = {
                'message': 'the required parameter "query" was not provided',
                'type': 'input',
                'code': 'missing',
                'info': {
                    'key': 'query'
                }
            }
            return [None, error, None]

        if not isinstance(parameter['query'], dict):
            error = {
                'message': ('the "query" parameter must be a an object '
                            'mapping fields to search strings'),
                'type': 'input',
                'code': 'wrong-type',
                'info': {
                    'key': 'query',
                    'expected': 'object',
                    # TODO translate to json type name
                    'received': type(parameter['query']).__name__
                }
            }
            return [None, error, None]
        query = {
            'query': parameter['query']
        }
        # filter
        # Optional search filter, which is a dictionary with fields as keys
        # and a simple string, integer, or list of integers as value.
        # A special yet optional "operator"  field may contain AND, OR, or NOT
        if 'filter' in parameter and parameter['filter'] != None:
            if not isinstance(parameter['filter'], dict):
                error = {
                    'message': ('the "filter" parameter must be an object '
                                'mapping fields to filter values'),
                    'type': 'input',
                    'code': 'wrong-type',
                    'info': {
                        'key': 'filter',
                        'expected': 'object',
                        # TODO translate to json type name
                        'received': type(parameter['filter']).__name__
                    }
                }
                return [None, error, None]
            query['filter'] = parameter['filter']

        # fields
        # Optional list of files to in return in the results.
        # It is an array of strings, each string being the dot
        # separated path to the result property, starting at _source.
        # The top level fields (sister fields to _source) area
        # always returned.
        if 'fields' in parameter and parameter['fields'] != None:
            # could, but am not, checking the type of the list...
            if not isinstance(parameter['fields'], list):
                error = {
                    'message': 'the "fields" parameter must be a list of strings',
                    'type': 'input',
                    'code': 'wrong-type',
                    'info': {
                        'key': 'fields',
                        'expected': 'list',
                        'received': type(parameter['fields']).__name__
                    }
                }
                return [None, error, None]
            query['fields'] = parameter['fields']


        if 'limit' in parameter and parameter['limit'] != None:
            if not isinstance(parameter['limit'], int):
                error = {
                    'message': 'the "limit" parameter must be an integer',
                    'type': 'input',
                    'code': 'wrong-type',
                    'info': {
                        'key': 'limit',
                        'expeced': 'integer',
                        'received': type(parameter['limit']).__name__
                    }
                }
                return [None, error, None]
            # theoretical limit is 10000, but getting anywhere close just times
            # out.
            if parameter['limit'] < 1 or parameter['limit'] > 1000:
                error = {
                    'message': ('the "limit" parameter must be an '
                                'integer between 1 and 1000'),
                    'type': 'input',
                    'code': 'invalid',
                    'info': {
                        'key': 'limit'
                    }
                }
                return [None, error, None]
            query['size'] = parameter['limit']
        else:
            query['size'] = 10

        max_page = math.ceil(10000 / query['size'])

        if 'page' in parameter and parameter['page'] != None:
            if not isinstance(parameter['page'], int):
                error = {
                    'messagse': 'the "page" parameter must be an integer',
                    'type': 'input',
                    'code': 'wrong-type',
                    'info': {
                        'key': 'page',
                        'expected': 'integer',
                        'received': type(parameter['page']).__name__
                    }
                }
                return [None, error, None]
            if parameter['page'] < 1 or parameter['page'] > max_page:
                error = {
                    'message': ('the "page" parameter must be an integer '
                                'between 1 and %d with a page size of %d' % (max_page, query['size'])),
                    'type': 'input',
                    'code': 'invalid',
                    'info': {
                        'key': 'page',
                        'valueProvided': parameter['page']
                    }
                }
                return [None, error, None]
            # we use 1 based page numbering, the jgi api is 0 based.
            query['page'] = parameter['page'] - 1
        else:
            query['page'] = 0

        # include_private A flag (kbase style boolean, 1, 0) indicating whether
        # to request private data be searched. It causes this by including the
        # username in the request to jgi. The kbase username is matched against
        # the jgi user database, which includes a kbase username field. If the
        # username is found, that account is used to determine which private
        # data is searched.
        #
        if 'include_private' in parameter and parameter['include_private'] != None:
            include_private = parameter['include_private']
            if not isinstance(include_private, int):
                error = {
                    'message': ("the 'include_private' parameter must be an "
                                " integer"),
                    'type': 'input',
                    'code': 'wrong-type',
                    'info': {
                        'key': 'include_private'
                    }
                }
                return [None, error, None]
            if include_private not in [1, 0]:
                error = {
                    'message': ("the 'include_private' parameter must be an "
                                "integer 1 or 0"),
                    'type': 'input',
                    'code': 'invalid',
                    'info': {
                        'key': 'include_private'
                    }
                }
                return [None, error, None]
            if (include_private == 1):
                query['userid'] = ctx['user_id']

        # PREPARE REQUEST

        header = {'Content-Type': 'application/json'}

        queryjson = json.dumps(query)

        # Ensure that the configuration is correct; the constructor
        # does not enforce this.
        if self.user is None:
            error = {
                'message': ("the configuration parameter 'user' is not set; "
                            "cannot call service without it"),
                'type': 'context',
                'code': 'context-property-missing',
                'info': {
                    'key': 'user'
                }
            }
            return [None, error, None]
        if self.passwd is None:
            error = {
                'message': ("the configuration parameter 'passwd' is not set; "
                            "cannot call service without it"),
                'type': 'context',
                'code': 'context-property-missing',
                'info': {
                    'key': 'passwd'
                }
            }
            return [None, error, None]
        if self.jgi_search_base_url is None:
            error = {
                'message': ("the configuration parameter 'jgi_search_base_url' is not set; "
                            "cannot call service without it"),
                'type': 'context',
                'code': 'context-property-missing',
                'info': {
                    'key': 'jgi_search_base_url'
                }
            }
            return [None, error, None]
        req_start = time.clock()
        pre_elapsed = int(round((req_start - call_start) * 1000))
        timeout = self.connection_timeout
        try:
            resp = requests.post(self.jgi_search_base_url + '/query', data=queryjson,
                                 auth=(self.user, self.passwd),
                                 timeout=timeout,
                                 headers=header)
        except requests.exceptions.Timeout as ex:
            req_end = time.clock()
            req_elapsed = int(round((req_end - req_start) * 1000))
            stats = {
                'pre_elapsed': pre_elapsed,
                'request_elapsed_time': req_elapsed,
                'post_elapsed': None,
                'query_sent': query
            }
            error = {
                'message': 'timeout exceeded sending query to jgi search service',
                'type': 'network',
                'code': 'connection-timeout',
                'info': {
                    'exception_message': str(ex),
                    'timeout': timeout
                }
            }
            return [None, error, stats]
        except requests.exceptions.RequestException as ex:
            req_end = time.clock()
            req_elapsed = int(round((req_end - req_start) * 1000))
            stats = {
                'pre_elapsed': pre_elapsed,
                'request_elapsed_time': req_elapsed,
                'post_elapsed': None,
                'query_sent': query
            }
            error = {
                'message': 'connection error sending query to jgi search service',
                'type': 'network',
                'code': 'connection-error',
                'info': {
                    'exception_message': str(ex)
                }
            }
            return [None, error, stats]

        req_end = time.clock()
        req_elapsed = int(round((req_end - req_start) * 1000))
        stats = {
            'pre_elapsed': pre_elapsed,
            'request_elapsed_time': req_elapsed,
            'post_elapsed': None,
            'query_sent': query
        }

        if resp.status_code == 200:
            post_end = time.clock()
            post_elapsed = int(round((post_end - req_end) * 1000))
            total_elapsed = int(round((post_end - call_start) * 1000))
            stats['post_elapsed'] = post_elapsed
            stats['total_elapsed'] = total_elapsed
            try:
                responsejson = json.loads(resp.text)
            except Exception as e:
                error = {
                    'message': 'error decoding json response',
                    'type': 'exception',
                    'code': 'json-decoding',
                    'info': {
                        'exception_message': str(e),
                        'query_sent': query
                    }
                }
                return [None, error, stats]
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
            return [result, None, stats]
        elif resp.status_code == 500:
            error = {
                'message': 'the jgi search service experienced an internal error',
                'type': 'upstream-service',
                'code': 'internal-error',
                'info': {
                    'status': resp.status_code,
                    # TODO: convert tojson
                    'body': resp.text,
                    'query_sent': query
                }
            }
            return [None, error, stats]
        elif resp.status_code == 502:
            error = {
                'message': 'jgi search service unavailable due to gateway error',
                'type': 'upstream-service',
                'code': 'gateway-error'
            }
            return [None, error, stats]
        elif resp.status_code == 503:
            error = {
                'message': 'jgi search service unavailable',
                'type': 'upstream-service',
                'code': 'service-unavailable'
            }
            return [None, error, stats]
        else:
            error = {
                'message': 'the jgi search service experienced an unknown error',
                'type': 'upstream-service',
                'code': 'unknown-error'
            }
            return [None, error, stats]

        # resp.raise_for_status()


        # We need to transform the result into a form that is acceptable to
        # KIDL.


        #END search

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method search return value ' +
                             'error is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method search return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, error, stats]

    def stage(self, ctx, parameter):
        """
        :param parameter: instance of type "StageInput" (STAGE) -> structure:
           parameter "ids" of list of String
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

        # INPUT

        # ids
        # A list of string database entity ids. A file is associated with each
        # id, and a copy request will be issued for each on. Just the ids are
        # passed through here, the fanning out is on the jgi side.
        if 'ids' not in parameter:
            error = {
                'message': "the 'ids' parameter is required but missing",
                'type': 'input',
                'code': 'missing',
                'info': {
                    'key': 'ids'
                }
            }
            return [None, error, None]
        ids = parameter['ids']
        if not isinstance(ids, list):
            error = {
                'message': "the 'ids' parameter must be an list",
                'type': 'input',
                'code': 'wrong-type',
                'info': {
                    'key': 'ids'
                }
            }
            return [None, error, None]

        # PREPARE REQUEST

        # Do it
        header = {'Content-Type': 'application/json'}

        request = {"ids": ','.join(ids),
                   "path": "/data/%s" % (ctx['user_id'])}

        requestjson = json.dumps(request)

        call_start = time.clock()
        timeout = self.connection_timeout
        try:
            resp = requests.post(self.jgi_search_base_url + '/fetch',
                                 data=requestjson,
                                 auth=(self.user, self.passwd),
                                 timeout=timeout,
                                 headers=header)
        except requests.exceptions.Timeout as ex:
            call_end = time.clock()
            elapsed_time = int(round((call_end - call_start) * 1000))
            stats = {
                'request_elapsed_time': elapsed_time
            }
            error = {
                'message': 'error sending fetech request to jgi search service',
                'type': 'network',
                'code': 'connection-timeout',
                'info': {
                    'exception_message': str(ex),
                    'timeout': timeout
                }
            }
            return [None, error, stats]
        except requests.exceptions.RequestException as ex:
            call_end = time.clock()
            elapsed_time = int(round((call_end - call_start) * 1000))
            stats = {
                'request_elapsed_time': elapsed_time
            }
            error = {
                'message': 'connection error sending fetch request to jgi search service',
                'type': 'network',
                'code': 'connection-error',
                'info': {
                    'exception_message': str(ex)
                }
            }
            return [None, error, stats]

        call_end = time.clock()
        stats = {
            'request_elapsed_time': int(round((call_end - call_start) * 1000))
        }

        # TODO: Just bail or return error object?
        if resp.status_code != 200:
            error = {
                'message': 'error processing query',
                'type': 'upstream',
                'code': 'http-error',
                'info': {
                    'response_code': resp.status_code,
                    'response_text': resp.text
                }
            }
            return [None, error, stats]

        # resp.raise_for_status()
        try:
            responsejson = json.loads(resp.text)
        except Exception as e:
            error = {
                'message': 'error decoding json response',
                'type': 'exception',
                'code': 'json-decoding',
                'info': {
                    'exception_message': str(e)
                }
            }
            return [None, error, stats]

        # TODO Add some logging

        #
        # Note that the response returns a single job id, regardless
        # of the number of ids in the copy request.
        #
        job_id = responsejson['id']

        result = {'job_id': job_id}

        return [result, None, stats]

        # NOTE: we are already returne d here, the code below is dead.

        #END stage

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method stage return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method stage return value ' +
                             'error is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method stage return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, error, stats]

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
        # INPUT

        # id
        # The job id is required in order to specify for which job we
        # want the status
        if 'job_id' not in parameter:
            error = {
                'message': "the 'job_id' parameter is required but missing",
                'type': 'input',
                'code': 'missing',
                'info': {
                    'key': 'job_id'
                }
            }
            return [None, error, None]
        if not isinstance(parameter['job_id'], basestring):
            error = {
                'message': "the 'job_id' parameter must be a string",
                'type': 'input',
                'code': 'wrong-type',
                'info': {
                    'key': 'job_id'
                }
            }
            return [None, error, None]
        job_id = parameter['job_id']

        request = {
            'id': job_id
        }

        # PREPARE REQUEST

        # TODO: when the api is fixed, and this request returns a json object,
        # the request header will need to be updated.
        # header = {'Accept': 'application/json'}
        header = {'Accept': 'text/html'}

        call_start = time.clock()
        timeout = self.connection_timeout
        try:
            resp = requests.get(self.jgi_search_base_url + '/status', params=request,
                                auth=(self.user, self.passwd),
                                timeout=timeout,
                                headers=header)
        except requests.exceptions.Timeout as ex:
            call_end = time.clock()
            elapsed_time = int(round((call_end - call_start) * 1000))
            stats = {
                'request_elapsed_time': elapsed_time
            }
            error = {
                'message': 'error sending status request to jgi search service',
                'type': 'network',
                'code': 'connection-timeout',
                'info': {
                    'exception_message': str(ex),
                    'timeout': timeout
                }
            }
            return [None, error, stats]
        except requests.exceptions.RequestException as ex:
            call_end = time.clock()
            elapsed_time = int(round((call_end - call_start) * 1000))
            stats = {
                'request_elapsed_time': elapsed_time
            }
            error = {
                'message': 'connection error sending status request to jgi search service',
                'type': 'network',
                'code': 'connection-error',
                'info': {
                    'exception_message': str(ex)
                }
            }
            return [None, error, stats]

        call_end = time.clock()
        stats = {
            'request_elapsed_time': int(round((call_end - call_start) * 1000))
        }

        if resp.status_code != 200:
            error = {
                'message': 'error processing query',
                'type': 'upstream',
                'code': 'http-error',
                'info': {
                    'response_code': resp.status_code,
                    'response_text': resp.text
                }
            }
            return [None, error, stats]

        # TODO: we hope to get json back but just string for now
        # responsejson = json.loads(resp.text)
        # TODO Add some logging
        result = {
            'message': resp.text
        }

        return [result, None, stats]

        # NOTE: we are already returned here, the code below is dead.
        #END stage_status

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method stage_status return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method stage_status return value ' +
                             'error is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method stage_status return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, error, stats]
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
        return [returnVal]
