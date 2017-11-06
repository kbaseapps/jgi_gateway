import math
import json
import time
import requests

def validateCallConfig(impl):
    if impl.user is None:
        return {
            'message': ("the configuration parameter 'user' is not set; "
                        "cannot call service without it"),
            'type': 'context',
            'code': 'context-property-missing',
            'info': {
                'key': 'user'
            }
        }
    if impl.passwd is None:
        return {
            'message': ("the configuration parameter 'passwd' is not set; "
                        "cannot call service without it"),
            'type': 'context',
            'code': 'context-property-missing',
            'info': {
                'key': 'passwd'
            }
        }
    if impl.jgi_search_base_url is None:
        return {
            'message': ("the configuration parameter 'jgi_search_base_url' is not set; "
                        "cannot call service without it"),
            'type': 'context',
            'code': 'context-property-missing',
            'info': {
                'key': 'jgi_search_base_url'
            }
        }
    return None

def validateSearchParameter(parameter, ctx):
    param = dict()
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
        return [None, error]

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
        return [None, error]
    param['query'] = parameter['query']

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
            return [None, error]
        param['filter'] = parameter['filter']

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
            return [None, error]
        param['fields'] = parameter['fields']


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
            return [None, error]
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
            return [None, error]
        param['size'] = parameter['limit']
    else:
        param['size'] = 10

    max_page = math.ceil(10000 / param['size'])

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
            return [None, error]
        if parameter['page'] < 1 or parameter['page'] > max_page:
            error = {
                'message': ('the "page" parameter must be an integer '
                            'between 1 and %d with a page size of %d' % (max_page, param['size'])),
                'type': 'input',
                'code': 'invalid',
                'info': {
                    'key': 'page',
                    'valueProvided': parameter['page']
                }
            }
            return [None, error]
        # we use 1 based page numbering, the jgi api is 0 based.
        param['page'] = parameter['page'] - 1
    else:
        param['page'] = 0

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
            return [None, error]
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
            return [None, error]
        if (include_private == 1):
            param['userid'] = ctx['user_id']

    return [param, None]


def sendRequest(path, data, ctx):
    header = {'Content-Type': 'application/json'}

    req_start = time.clock()
    timeout = ctx['connection_timeout']
    try:
        if (ctx['method'] == 'post'):
            resp = requests.post(ctx['url'] + '/' + path, data=json.dumps(data),
                                 auth=(ctx['user'], ctx['password']),
                                 timeout=timeout,
                                 headers=header)
        else:
            resp = requests.get(ctx['url'] + '/' + path, params=data,
                                 auth=(ctx['user'], ctx['password']),
                                 timeout=timeout,
                                 headers=header)
    except requests.exceptions.Timeout as ex:
        req_end = time.clock()
        req_elapsed = int(round((req_end - req_start) * 1000))
        stats = {
            'request_elapsed_time': req_elapsed,
            'query_sent': data
        }
        error = {
            'message': 'timeout exceeded sending request to jgi search service',
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
            'request_elapsed_time': req_elapsed,
            'query_sent': data
        }
        error = {
            'message': 'connection error sending request to jgi search service',
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
        'request_elapsed_time': req_elapsed,
        'query_sent': data
    }


    if resp.status_code == 200:
        try:
            if (resp.headers['Content-Type'] == 'application/json'):
                responsejson = json.loads(resp.text)
            else:
                responsejson = {'message': resp.text}
        except Exception as e:
            error = {
                'message': 'error decoding json response',
                'type': 'exception',
                'code': 'json-decoding',
                'info': {
                    'exception_message': str(e),
                    'query_sent': data
                }
            }
            return [None, error, stats]

        return [responsejson, None, stats]
    elif resp.status_code == 500:
        error = {
            'message': 'the jgi search service experienced an internal error',
            'type': 'upstream-service',
            'code': 'internal-error',
            'info': {
                'status': resp.status_code,
                # TODO: convert tojson
                'body': resp.text,
                'query_sent': data
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
            'code': 'unknown-error',
            'info': {
                'text': resp.text
            }
        }
        return [None, error, stats]

def validateFetchParameter(parameter, ctx):
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
        return [None, error]
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
        return [None, error]

    return [{"ids": ','.join(ids),
             "path": "/data/%s" % (ctx['user_id'])}, None]


def validateStageStatusParameter(parameter, ctx):
    if not isinstance(parameter, dict):
        error = {
            'message': "the parameter must be a dict",
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': 'parameter'
            }
        }
        return [None, error]

    if 'job_id' not in parameter:
        error = {
            'message': "the 'job_id' parameter is required but missing",
            'type': 'input',
            'code': 'missing',
            'info': {
                'key': 'job_id'
            }
        }
        return [None, error]

    if not isinstance(parameter['job_id'], basestring):
        error = {
            'message': "the 'job_id' parameter must be a string",
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': 'job_id'
            }
        }
        return [None, error]
    job_id = parameter['job_id']

    return [{
        'id': job_id
    }, None]
