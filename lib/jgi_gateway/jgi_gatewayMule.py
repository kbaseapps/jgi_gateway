import threading
from os import environ

import uwsgi
from configparser import ConfigParser

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    my_dir = path.dirname(path.dirname(path.abspath(__file__)))
    print('my dir')
    print(my_dir)
    sys.path.append(my_dir)
from jgi_gateway.staging_jobs_manager import StagingJobsManager
from jgi_gateway import utils

DEPLOY = 'KB_DEPLOYMENT_CONFIG'
SERVICE = 'KB_SERVICE_NAME'
AUTH = 'auth-service-url'


def get_config_file():
    return environ.get(DEPLOY, None)


def get_service_name():
    return environ.get(SERVICE, None) 


def get_config():
    if not get_config_file():
        return None
    retconfig = {}
    config = ConfigParser()
    config.read(get_config_file())
    for nameval in config.items(get_service_name() or 'jgi_gateway'):
        retconfig[nameval[0]] = nameval[1]
    return retconfig


app_config = utils.validate_config(get_config())


class Looper:
    def __init__(self, config):
        self.in_loop = False
        self.interval = 10
        self.job_checks = 0
        self.jobs_manager = StagingJobsManager(config)

    def start_job_check_loop(self):
        if self.in_loop:
            return
        self.in_loop = True
        self.job_check_loop()

    def job_check_loop(self):
        jobs, error = self.jobs_manager.sync_active_jobs()
        if jobs:
            threading.Timer(self.interval, self.job_check_loop).start()
        else:
            self.in_loop = False


def mule_loop():
    looper = Looper(app_config)
    while True:
        message = uwsgi.mule_get_msg()
        if message == b'start-job-monitoring':
            looper.start_job_check_loop()
        else:
            print('unknown message:')
            print(message)

# this_thread = threading.Thread(target=mule_loop)
# this_thread.daemon = True
# this_thread.start()


if __name__ == '__main__':
    # threading.Thread(target=mule_loop, deamon=True).start()
    mule_loop()
