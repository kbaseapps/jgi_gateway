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
    VERSION = "0.0.1"
    GIT_URL = "ssh://git@github.com/eapearson/jgi_gateway"
    GIT_COMMIT_HASH = "a487581ef96cba3a6d3dd2c83bb19aed69eb6eb8"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        """
        default constructor
        """

        # print "DEBUG - config:"
        # print json.dumps(config)

        self.config = config
        self.user = None
        self.passwd = None
        if 'jgi-token' in config:
            (user, passwd) = config['jgi-token'].split(':')
            self.user = user
            self.passwd = passwd
        self.jgi_host = 'https://jgi-kbase.nersc.gov'
        if 'jgi-host' in config:
            self.jgi_host = config['jgi-host']
        print "Using %s for queries" % (self.jgi_host)
        #END_CONSTRUCTOR
        pass


    def search_jgi(self, ctx, input):
        """
        The search_jgi function takes a search string and returns a list of
        documents.
        :param input: instance of type "SearchInput" (search_jgi searches the
           JGI service for matches against the query, which may be a string
           or an object mapping string->string Other parameters @optional
           limit @optional page) -> structure: parameter "query" of type
           "SearchQuery" -> mapping from String to String, parameter "filter"
           of type "SearchFilter" (SearchFilter The jgi back end takes a map
           of either string, integer, or array of integer. I don't think the
           type compiler supports union typs, so unspecified it is.) ->
           mapping from String to unspecified object, parameter "limit" of
           Long, parameter "page" of Long, parameter "include_private" of
           type "bool" (a bool defined as int)
        :returns: multiple set - (1) parameter "result" of type
           "SearchResult" -> structure: parameter "search_result" of type
           "SearchQueryResult" (typedef mapping<string, string> docdata;) ->
           list of unspecified object, (2) parameter "stats" of type
           "CallStats" (Call performance measurement) -> structure: parameter
           "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, stats
        #BEGIN search_jgi
        
        # Return structures
        stats = dict()
        result = dict()

        # INPUT

        # query
        # A required property, this provides the, well, search to conduct
        # over the jgi search service space. 
        # Note that the sender may simply send '*' to fetch all results.
        #
        if 'query' not in input:
            raise(ValueError("missing required parameter query"))
        query = {"query": input['query']}

        # filter
        # Optional search filter, which is a dictionary with fields as keys
        # and a simple string, integer, or list of integers as value.
        # A special yet optional "operator"  field may contain AND, OR, or NOT
        if 'filter' in input:
            query['filter'] = input['filter']

        if 'limit' in input:
            query['size'] = input['limit']

        if 'page' in input:
            query['page'] = input['page']

        # include_private 
        # A flag (kbase style boolean, 1, 0) indicating whether to request private
        # data be searched. It causes this by including the username in the request
        # to jgi. The kbase username is matched against the jgi user database, which
        # includes a kbase username field. If the username is found, that account is used
        # to determine which private data is searched.
        #
        if 'include_private' in input:
            include_private = input['include_private']
            if not isinstance(include_private, int) or include_private not in [1,0]:
                raise(ValueError("the 'include_private' parameter must be an integer 1 or 0"))
            if include_private:
                query['userid'] = ctx['user_id']

        # PREPARE REQUEST

        # Do it
        header = {'Content-Type': 'application/json'}

        queryjson = json.dumps(query)

        call_start = time.clock()
        ret = requests.post(self.jgi_host + '/query', data=queryjson,
                            auth=(self.user, self.passwd),
                            headers=header)
        call_end = time.clock()
        elapsed_time = int(round((call_end - call_start) * 1000))
        stats['request_elapsed_time'] = elapsed_time;

        if ret.status_code == 200:
            result['search_result'] = ret.json()            
        else:
            raise ValueError('Error Response from JGI search service (%d)' %
                             ret.status_code)

        #END search_jgi

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search_jgi return value ' +
                             'result is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method search_jgi return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, stats]

    def stage_objects(self, ctx, input):
        """
        :param input: instance of type "StageInput" -> structure: parameter
           "ids" of list of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingResult" (StagingResult returns a map entry for each id
           submitted in the stage_objects request. The map key is the _id
           property returned in a SearchResult item (not described here but
           probably should be), the value is a string describing the result
           of the staging request. At time of writing, the value is always
           "staging" since the request to the jgi gateway jgi service and the
           call to stage_objects in the jgi gateway kbase service are in
           different processes.) -> structure: parameter "job_id" of String,
           (2) parameter "stats" of type "CallStats" (Call performance
           measurement) -> structure: parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, stats
        #BEGIN stage_objects

        # Return structures
        stats = dict()
        result = dict()

        # INPUT

        # ids
        # A list of string database entity ids. A file is associated with each
        # id, and a copy request will be issued for each on. Just the ids are 
        # passed through here, the fanning out is on the jgi side.
        if 'ids' not in input:
            raise(ValueError("the 'ids' parameter is required "))
        ids = input['ids']
        if not isinstance(ids, list):
            raise(ValueError("the 'ids' parameter must be a list"))

        # PREPARE REQUEST

        # Do it
        header = {'Content-Type': 'application/json'}

        request = {"ids": ','.join(ids),
                   "path": "/data/%s" % (ctx['user_id'])}
        requestjson = json.dumps(request)

        call_start = time.clock()
        resp = requests.post(self.jgi_host + '/fetch', data=requestjson,
                                auth=(self.user, self.passwd),
                                headers=header)
        call_end = time.clock()
        elapsed_time = int(round((call_end - call_start) * 1000))
        stats['request_elapsed_time'] = elapsed_time
                            
        # TODO: Just bail or return error object?
        resp.raise_for_status()
        # TODO: handle parsing errors
        responsejson = json.loads(resp.text)
        # TODO Add some logging

        #
        # Note that the response returns a single job id, regardless
        # of the number of ids in the copy request.
        #
        job_id = responsejson['id']
        result['job_id'] = job_id

        #END stage_objects

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method stage_objects return value ' +
                             'result is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method stage_objects return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, stats]

    def stage_status(self, ctx, input):
        """
        Fetch the current status of the given staging fetch request as 
        identified by its job id
        :param input: instance of type "StagingStatusInput" -> structure:
           parameter "job_id" of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingStatusResult" -> structure: parameter "message" of String,
           (2) parameter "stats" of type "CallStats" (Call performance
           measurement) -> structure: parameter "request_elapsed_time" of Long
        """
        # ctx is the context object
        # return variables are: result, stats
        #BEGIN stage_status

        # Result structs
        stats = dict()
        result = dict()

        # INPUT

        # id
        # The job id is required in order to specify for which job we want the status
        #
        if 'job_id' not in input:
            raise(ValueError('the "job_id" is required'))
        job_id = input['job_id']
        if not isinstance(job_id, basestring):
            raise(ValueError('the "job_id" must be a string'))

        request = {"id": job_id}

        # PREPARE REQUEST

        # TODO: when the api is fixed, and this request returns a json object,
        # the request header will need to be updated.
        # header = {'Accept': 'application/json'}
        header = {'Accept': 'text/html'}

        # requestjson = json.dumps(request)
        # print "Fetch request: " + requestjson
        call_start = time.clock()
        resp = requests.get(self.jgi_host + '/status', params=request,
                            auth=(self.user, self.passwd),
                            headers=header)
        call_end = time.clock()
        stats['request_elapsed_time'] = int(round((call_end - call_start) * 1000))
        # TODO: Just bail or return error object?
        resp.raise_for_status()
        #print "jgi gateway staging status request status: %d" % (resp.status_code)
        #print resp.text
        # TODO: we hope to get json back but just string for now
        # responsejson = json.loads(resp.text)
        #    # TODO Add some logging

        result['message'] = resp.text

        #END stage_status

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method stage_status return value ' +
                             'result is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method stage_status return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, stats]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
