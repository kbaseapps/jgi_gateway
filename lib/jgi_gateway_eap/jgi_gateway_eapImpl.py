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
import utils
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

        # BASIC config
        error = utils.validateCallConfig(self);
        if error:
            return [None, error, None]


        # INPUT
        call_start = time.clock()

        query, error = utils.validateSearchParameter(parameter, ctx)
        if error:
            return [None, error, None]

        # PREPARE REQUEST
        responsejson, error, stats = utils.sendRequest('query', query, {
            'method': 'post',
            'connection_timeout': self.connection_timeout,
            'url': self.jgi_search_base_url,
            'user': self.user,
            'password': self.passwd
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

        error = utils.validateCallConfig(self);
        if error:
            return [None, error, None]

        # INPUT
        request, error = utils.validateFetchParameter(parameter, ctx)
        if error:
            return [None, error, None]

        responsejson, error, stats = utils.sendRequest('fetch', request,  {
            'method': 'post',
            'connection_timeout': self.connection_timeout,
            'url': self.jgi_search_base_url,
            'user': self.user,
            'password': self.passwd
        })

        if responsejson:
            #
            # Note that the response returns a single job id, regardless
            # of the number of ids in the copy request.
            #
            job_id = responsejson['id']

            result = {'job_id': job_id}
        else:
            result = None

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

        error = utils.validateCallConfig(self);
        if error:
            return [None, error, None]


        # INPUT
        request, error = utils.validateStageStatusParameter(parameter, ctx)
        if error:
            return [None, error, None]

        response, error, stats = utils.sendRequest('status', request,  {
            'method': 'get',
            'connection_timeout': self.connection_timeout,
            'url': self.jgi_search_base_url,
            'user': self.user,
            'password': self.passwd,
            'type': 'text'
        })

        return [response, error, stats]

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
