import logging

import werkzeug.serving

from app import app

# we are behind a proxy. log the ip of the end-user, not the proxy.
# this will also work without the proxy
werkzeug.serving.WSGIRequestHandler.address_string = lambda self: self.headers.get('x-real-ip', self.client_address[0])

# log to a file (access.log), not stderr
logging.basicConfig(filename='access.log', level=logging.DEBUG, format='%(message)s')

if __name__ == '__main__':
    app.run()
