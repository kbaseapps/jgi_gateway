# -*- coding: utf-8 -*-
#BEGIN_HEADER
"""
JGI Gateway Service
"""

import os
import requests
import json
#END_HEADER


class jgi_gateway:
    '''
    Module Name:
    jgi_gateway

    Module Description:
    A KBase module: jgi_gateway
    '''

    # WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        """
        default constructor
        """

        self.user = None
        self.passwd = None
        if 'JGI_TOKEN' in os.environ:
            (user, passwd) = os.environ['JGI_TOKEN'].split(':')
            self.user = user
            self.passwd = passwd
        #END_CONSTRUCTOR

    def search_jgi(self, ctx, search_string):
        """
        The search_jgi function takes a search string and returns a list of
        documents.
        :param search_string: instance of String
        :returns: instance of type "SearchResults" -> structure: parameter
           "doc_data" of list of type "docdata" -> mapping from String to
           String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN search_jgi
        header = {'Content-Type': 'application/json'}
        query = json.dumps({"query": search_string})
        ret = requests.post('https://jgi-kbase.nersc.gov/query', data=query,
                            auth=(self.user, self.passwd),
                            headers=header)
        if ret.status_code == 200:
            output = ret.json()
        else:
            raise ValueError('Bad Response from JGI search service (%d)' %
                             ret.status_code)
        #END search_jgi

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method search_jgi return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def stage_objects(self, ctx, input):
        """
        :param input: instance of type "StageInput" -> structure: parameter
           "ids" of list of String
        :returns: instance of type "StagingResults" -> mapping from String to
           String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN stage_objects
        results = dict()
        for item in input:
            results[item] = 'SUBMITED'
        #END stage_objects

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method stage_objects return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
