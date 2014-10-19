import tornado


class BaseHandler(tornado.web.RequestHandler):
    pass


class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html')


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')
