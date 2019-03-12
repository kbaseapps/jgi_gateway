# -*- coding: utf-8 -*-
try:
    import uwsgi
    uwsgi_available = True
except ImportError:
    uwsgi_available = False


class ServerContext(object):
    'Provides functions only the server can'
    def __init__(self):
        self.uwsgi_available = uwsgi_available
        
    def send_message(self, msg):
        if self.uwsgi_available:
            uwsgi.mule_msg(msg)
        else:
            print('warning: uwsgi not available')

    def is_uwsgi_available(self):
        return self.uwsgi_available
