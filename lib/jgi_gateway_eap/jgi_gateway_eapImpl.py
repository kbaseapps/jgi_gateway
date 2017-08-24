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
    GIT_COMMIT_HASH = "5cfa1f63228c57a5ca32bc19da6f8ee71ca574aa"

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
           JGI service for matches against the search_string Other parameters
           @optional limit @optional page) -> structure: parameter
           "search_string" of String, parameter "limit" of Long, parameter
           "page" of Long
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

        # Do it
        header = {'Content-Type': 'application/json'}
        if 'search_string' not in input:
            raise(ValueError("missing required parameter search_string"))
        query = {"query": input['search_string']}
        if 'limit' in input:
            query['size'] = input['limit']
        if 'page' in input:
            query['page'] = input['page']
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
            raise ValueError('Bad Response from JGI search service (%d)' %
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

        # Do it
        header = {'Content-Type': 'application/json'}
        request = {"ids": ','.join(input['ids']),
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
        # for id in input['ids']:
        #     result[id] = responsejson
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

        # header = {'Accept': 'application/json'}
        header = {}
        request = {"id": input['job_id']}
        # requestjson = json.dumps(request)
        print "Fetch request: " + requestjson
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
