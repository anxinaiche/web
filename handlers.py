# coding=utf-8
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

    @property
    def proxy(self):
        return self.application.http_proxy


class WXHandler(BaseHandler):
    '''
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx703b3491b593a587&redirect_uri=http%3A%2F%2F121.199.5.143%2Foauth_response&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect
    '''
    def get(self):
        echo_str = self.get_argument("echostr", None, True)
        self.set_header("content-type", "text/html")
        self.write(echo_str)
        self.finish()


class WXOAuthHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument('code')
        resp = yield self.proxy.get_wx_access_token('wx703b3491b593a587', '32fb3722ad1feb96029f2c6ce6ce82b3', code)

        access_token = resp['access_token']
        openid = resp['openid']
        resp = yield self.proxy.get_wx_info(access_token, openid)

        # resp = {
        #     'openid': 'dfksdhfslkdjf',
        #     'nickname': u'老于',
        #     'headimgurl': ''
        # }

        self.render('wx_reserve.html', info=resp)