import math
import json
import time
import calendar
import re
import requests
from requests_futures.sessions import FuturesSession

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
    if impl.password is None:
        return {
            'message': ("the configuration parameter 'password' is not set; "
                        "cannot call service without it"),
            'type': 'context',
            'code': 'context-property-missing',
            'info': {
                'key': 'password'
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

# def validateConfig(impl):

def check_param(params, name, required, param_type):

    if name not in params:
        if required:
            error = {
                'message': 'the required parameter "' + name + '" was not provided',
                'type': 'input',
                'code': 'missing',
                'info': {
                    'key': name
                }
            }
            return [None, error]
        else:
            return [None, None]

    param_value = params[name]
    if not isinstance(param_value, param_type):
        error = {
            'message': ('the "' + name + '" parameter is expected to be a "' + param_type.__name__ + '" but is actually a "' + type(param_value).__name__),
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': name,
                'expected': param_type.__name__,
                # TODO translate to json type name
                'received': type(param_value).__name__
            }
        }
        return [None, error]
    return [param_value, None]


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

    sort_param, error = check_param(parameter, 'sort', True, list)
    if error is not None:
        return None, error

    sort = []
    for index, sort_spec in enumerate(sort_param):
        if not isinstance(sort_spec, dict):
            error = {
                'message': 'the "sort" spec within a sort must be a dict',
                'type': 'input',
                'code': 'wrong-type',
                'info': {
                    'key': ['sort', index],
                    'expected': 'list',
                    'received': type(sort_spec).__name__
                }
            }
            return [None, error]
        
        field, error = check_param(sort_spec, 'field', True, basestring)
        if error is not None:
            return [None, error]

        descending, error = check_param(sort_spec, 'descending', True, int)
        if error is not None:
            return [None, error]

        if descending == 1:
            direction = 'desc'
        else:
            direction = 'asc'

        sort.append(dict([(field, direction)]))

    param['sort'] = sort

    # filter
    # Optional search filter, which is a dictionary with fields as keys
    # and a simple string, integer, or list of integers as value.
    # A special yet optional "operator"  field may contain AND, OR, or NOT
    if 'filter' in parameter and parameter['filter'] is not None:
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
    if 'fields' in parameter and parameter['fields'] is not None:
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


    if 'limit' in parameter and parameter['limit'] is not None:
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

    # The page size comes in 1-based
    # The requested page cannot result in any item beyond 10,000.
    # Therefore the max page is the 
    max_page = math.floor(10000 / param['size'])

    if 'page' in parameter and parameter['page'] is not None:
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
    if 'include_private' in parameter and parameter['include_private'] is not None:
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
            'code': 'gateway-error',
            'info': {
                'status': resp.status_code,
                # TODO: convert tojson
                'body': resp.text,
                'query_sent': data
            }
        }
        return [None, error, stats]
    elif resp.status_code == 503:
        error = {
            'message': 'jgi search service reports that it is unavailable',
            'type': 'upstream-service',
            'code': 'service-unavailable',
            'info': {
                'status': resp.status_code,
                # TODO: convert tojson
                'body': resp.text,
                'query_sent': data
            }
        }
        return [None, error, stats]
    else:
        error = {
            'message': 'the jgi search service experienced an unknown error',
            'type': 'upstream-service',
            'code': 'unknown-error',
            'info': {
                'status': resp.status_code,
                # TODO: convert tojson
                'body': resp.text,
                'query_sent': data
            }
        }
        return [None, error, stats]

def sendFRequest(session, path, data, ctx):
    header = {'Content-Type': 'application/json'}
    timeout = ctx['connection_timeout']
    if (ctx['method'] == 'post'):
        return session.post(ctx['url'] + '/' + path, data=json.dumps(data),
                                auth=(ctx['user'], ctx['password']),
                                timeout=timeout,
                                headers=header)
    else:
        return session.get(ctx['url'] + '/' + path, params=data,
                                auth=(ctx['user'], ctx['password']),
                                timeout=timeout,
                                headers=header)

def processFRequest(request):
    try:
        resp = request.result()
    except requests.exceptions.Timeout as ex:
        error = {
            'message': 'timeout exceeded sending request to jgi search service',
            'type': 'network',
            'code': 'connection-timeout',
            'info': {
                'exception_message': str(ex),
                # 'timeout': timeout
            }
        }
        return [None, error, None]
    except requests.exceptions.RequestException as ex:
        error = {
            'message': 'connection error sending request to jgi search service',
            'type': 'network',
            'code': 'connection-error',
            'info': {
                'exception_message': str(ex)
            }
        }
        return [None, error, None]

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
            return [None, error, None]

        return [responsejson, None, None]
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
        return [None, error, None]
    elif resp.status_code == 502:
        error = {
            'message': 'jgi search service unavailable due to gateway error',
            'type': 'upstream-service',
            'code': 'gateway-error'
        }
        return [None, error, None]
    elif resp.status_code == 503:
        error = {
            'message': 'jgi search service unavailable',
            'type': 'upstream-service',
            'code': 'service-unavailable'
        }
        return [None, error, None]
    else:
        error = {
            'message': 'the jgi search service experienced an unknown error',
            'type': 'upstream-service',
            'code': 'unknown-error',
            'info': {
                'text': resp.text
            }
        }
        return [None, error, None]

def validateFetchParameter(parameter, ctx):
    # ids
    # A list of string database entity ids. A file is associated with each
    # id, and a copy request will be issued for each on. Just the ids are
    # passed through here, the fanning out is on the jgi side.
    if 'file' not in parameter:
        error = {
            'message': "the 'file' parameter is required but missing",
            'type': 'input',
            'code': 'missing',
            'info': {
                'key': 'file'
            }
        }
        return [None, error]
    requested_file = parameter['file']

    if not isinstance(requested_file, dict):
        error = {
            'message': "the 'file' parameter must be an dict",
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': 'file'
            }
        }
        return [None, error]

    ids = []

    if 'id' not in requested_file:
        error = {
            'message': "the 'id' parameter is required but missing",
            'type': 'input',
            'code': 'missing',
            'info': {
                'key': ['file', 'id']
            }
        }
        return [None, error]

    if not isinstance(requested_file['id'], basestring):
        error = {
            'message': "an 'id' parameter item must be a string",
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': ['file', 'id']
            }
        }
        return [None, error]   

    if 'filename' not in requested_file:
        error = {
            'message': "the 'filename' parameter is required but missing",
            'type': 'input',
            'code': 'missing',
            'info': {
                'key': ['file', 'filename']
            }
        }
        return [None, error]     

    if not isinstance(requested_file['filename'], basestring):
        error = {
            'message': "a 'filename' parameter item must be a string",
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': ['file', 'filename']
            }
        }
        return [None, error]

    if 'username' not in requested_file:
        error = {
            'message': "the 'username' parameter is required but missing",
            'type': 'input',
            'code': 'missing',
            'info': {
                'key': ['file', 'username']
            }
        }
        return [None, error]     

    if not isinstance(requested_file['username'], basestring):
        error = {
            'message': "a 'username' parameter item must be a string",
            'type': 'input',
            'code': 'wrong-type',
            'info': {
                'key': ['file', 'username']
            }
        }
        return [None, error]

    if requested_file['username'] != ctx['user_id']:
        error = {
            'message': "the 'username' parameter must match the current authorized user",
            'type': 'input',
            'code': 'invalid',
            'info': {
                'key': 'username'
            }
        }
        return [None, error]
        
    ids.append({
        'id': requested_file['id'],
        'filename': requested_file['filename']
    })

    # NOTE: still using the old ids parameter for the call to jgi.
    return [{"files": ids,
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


    #  typedef structure {
    #     string username;
    #     timestamp created_from;
    #     timestamp created_to;
    #     timestamp updated_from;
    #     timestamp updated_to;
    #     string status;
    # } StagingJobsFilter;

    # typedef structure {
    #     StagingJobsFilter filter;
    # } StagingJobsInput;

def validate_staging_jobs_parameter(parameter, ctx):
    'validates the parameters for the staging_jobs method and return a normalized object'
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

    username, error = check_param(parameter, 'username', True, basestring)
    if error is not None:
        return None, error

    if username != ctx['user_id']:
        error = {
            'message': "the 'username' parameter must match the current authorized user",
            'type': 'input',
            'code': 'invalid',
            'info': {
                'key': 'username'
            }
        }
        return [None, error]

    search_filter, error = check_param(parameter, 'filter', True, dict)
    if error is not None:
        return None, error

    # TODO: Validate filter
    search_sort, error = check_param(parameter, 'sort', False, list)
    if error is not None:
        return None, error

    search_range, error = check_param(parameter, 'range', True, dict)
    if error is not None:
        return None, error

    return [{
        'username': username,
        'filter': search_filter,
        'range': search_range,
        'sort': search_sort
    }, None]

def validate_staging_jobs_summary_parameter(parameter, ctx):
    username, error = check_param(parameter, 'username', True, basestring)
    if error is not None:
        return None, error

    if username != ctx['user_id']:
        error = {
            'message': "the 'username' parameter must match the current authorized user",
            'type': 'input',
            'code': 'invalid',
            'info': {
                'key': 'username'
            }
        }
        return [None, error]

    return [{
        'username': username
    }, None]

def make_job(username, jamo_id, filename):
    return {
        'username': username,
        'jamo_id': jamo_id,
        'filename': filename,
        'job_id': None,
        'created': calendar.timegm(time.gmtime()),
        'updated': None,
        'status_code': 'sent',
        'status_raw': 'sent'
    }

def validate_config(config):
     # Import and validate the jgi host
    if 'jgi-base-url' not in config:
        raise(ValueError('"jgi-base-url" configuration property not provided'))
    # The host must be secure, and be reasonably valid:
    # https://a.b
    if (not re.match("^https://.+?\\..+$", config['jgi-base-url'])):
        raise(ValueError('"jgi-base-url" configuration property not a valid url base'))

    jgi_search_base_url = config['jgi-base-url']


    # Import and validate the jgi token
    if 'jgi-token' not in config:
        raise(ValueError('"jgi-token" configuration property not provided'))

    token = config['jgi-token'].split(':')
    if (len(token) != 2):
        raise(ValueError('"jgi-token" configuration property is invalid'))

    (user, password) = token

    # Given a string which can split, the worst we can have is an empty
    # part, since we are ensured to get at least a 0-length string
    if ((len(user) == 0) or (len(password) == 0)):
        raise(ValueError('"jgi-token" configuration property is invalid'))

    # Import and validate the connection timeout
    if 'jgi-connection-timeout' not in config:
        raise(ValueError('"jgi-connection-timeout" configuration property not provided'))
    try:
        connection_timeout = int(config['jgi-connection-timeout'])
    except ValueError as ex:
        raise(ValueError('"jgi-connection-timeout" configuration property is not a float: ' + str(ex)))
    if not (config['jgi-connection-timeout'] > 0):
        raise(ValueError('"jgi-connection-timeout" configuration property must be > 0'))

    connection_timeout = float(connection_timeout) /float(1000)
    print('connection timeout %f sec' % (connection_timeout) )

    # Import and validate the mongo db settings
    if 'mongo-host' not in config:
        raise(ValueError('"mongo-host" configuration property not provided')) 
    mongo_host = config['mongo-host']

    if 'mongo-port' not in config:
        raise(ValueError('"mongo-port" configuration property not provided')) 
    mongo_port = int(config['mongo-port'])

    if 'mongo-db' not in config:
        raise(ValueError('"mongo-db" configuration property not provided'))
    mongo_db = config['mongo-db']

    if 'mongo-user' not in config:
        raise(ValueError('"mongo-user" configuration property not provided'))
    mongo_user = config['mongo-user']

    if 'mongo-pwd' not in config:
        raise(ValueError('"mongo-pwd" configuration property not provided'))
    mongo_pwd = config['mongo-pwd']

    return {
        'mongo': {
            'host': mongo_host,
            'port': mongo_port,
            'db': mongo_db,
            'user': mongo_user,
            'password': mongo_pwd
        }, 
        'jgi': {
            'connection-timeout': connection_timeout,
            'base-url': jgi_search_base_url,
            'user': user,
            'password': password
        }
    }