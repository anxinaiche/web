__author__ = 'yuxizhou'

import os
import signal
import time
import motor
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from http_proxy import HttpProxy
from handlers import *
from handlers_user import *
from handlers_web import *
from handlers_weixin import *
from handlers_admin import *
from handerls_api import *

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
            (r"/", ComingSoonHandler),
            # (r"/", HomeHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/register", RegisterHandler),
            (r"/reserve", ReserveHandler),
            (r"/intro", IntroHandler),

            # weixin site
            (r"/wx", WXHandler),
            (r"/oauth_response", WXOAuthHandler),
            (r"/wx/reserve", WXReserveHandler),
            (r"/wx/my", WXMyHandler),
            (r"/wx/home", WXHomeHandler),
            (r"/wx/orders", WXOrdersHandler),
            (r"/wx/test", WXTestHandler),
            (r"/wx/report/(.*)", WXReportHandler),

            # admin site
            (r"/admin", AdminHandler),
            (r"/admin/home", AdminHomeHandler),

            (r"/admin/reserves", AdminReservesHandler),
            (r"/admin/reserves/(.*)/delete", AdminReservesDeleteHandler),

            (r"/admin/dealers", AdminDealersHandler),
            (r"/admin/dealers/new", AdminDealersNewHandler),
            (r"/admin/dealers/(.*)/edit", AdminDealersEditHandler),
            (r"/admin/dealers/(.*)/delete", AdminDealersDeleteHandler),
            (r"/admin/dealers/(.*)", AdminDealersEditHandler),

            (r"/admin/brands", AdminBrandsHandler),
            (r"/admin/brands/new", AdminBrandsNewHandler),
            (r"/admin/brands/(.*)/edit", AdminBrandsEditHandler),
            (r"/admin/brands/(.*)/delete", AdminBrandsDeleteHandler),
            (r"/admin/brands/(.*)", AdminBrandsEditHandler),

            # api
            (r"/api/v1/dealers", ApiDealersHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
            login_url='/login',
            debug=not options.production
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.mongodb = motor.MotorClient().web

        self.http_proxy = HttpProxy()


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