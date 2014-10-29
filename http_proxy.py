__author__ = 'yuxizhou'

import tornado.httpclient
import tornado.gen
import json


class HttpProxy(object):
    def __init__(self):
        self.async_http_client = tornado.httpclient.AsyncHTTPClient()

    @tornado.gen.coroutine
    def get_wx_access_token(self, appid, secret, code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(appid, secret, code)

        request = tornado.httpclient.HTTPRequest(url=url, method='GET')
        resp = yield self.async_http_client.fetch(request)
        raise tornado.gen.Return(json.loads(resp.body))

    @tornado.gen.coroutine
    def get_wx_info(self, access_token, openid):
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, openid)

        request = tornado.httpclient.HTTPRequest(url=url, method='GET')
        resp = yield self.async_http_client.fetch(request)
        raise tornado.gen.Return(json.loads(resp.body))