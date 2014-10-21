import tornado
import tornado.gen


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return user_id

    @property
    def mongodb(self):
        return self.application.mongodb