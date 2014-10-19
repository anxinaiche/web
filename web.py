__author__ = 'yuxizhou'

import os
import signal
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from handlers import *

define('production', default=False, type=bool)
define('port', default=8880, type=int)


def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    http_server.stop()

    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 3

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()

    stop_loop()
    
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/login", LoginHandler),
            (r"/register", RegisterHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
            login_url='/',
            debug=not options.production
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    global http_server
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()