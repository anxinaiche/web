import tornado


class BaseHandler(tornado.web.RequestHandler):
    pass


class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html')
