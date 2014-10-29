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


class WXHandler(BaseHandler):
    def get(self):
        echo_str = self.get_argument("echostr", None, True)
        self.set_header("content-type", "text/html")
        self.write(echo_str)
        self.finish()
