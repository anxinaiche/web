# coding=utf-8
import tornado
import tornado.gen
import pymongo
from bson import ObjectId


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

    @tornado.gen.coroutine
    def item_list(self, db):
        cursor = db.find()
        result = []
        cursor.sort([('_id', pymongo.ASCENDING)])
        for item in (yield cursor.to_list(length=None)):
            result.append(item)

        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def item_list_by(self, db, by):
        cursor = db.find(by)
        result = []
        for item in (yield cursor.to_list(length=None)):
            result.append(item)

        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def item_remove(self, db, item_id):
        result = yield db.remove({
            '_id': ObjectId(item_id)
        })

        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def item_get(self, db, item_id):
        item = yield db.find_one({
            '_id': ObjectId(item_id)
        })

        raise tornado.gen.Return(item)

    @tornado.gen.coroutine
    def item_update(self, db, item_id):
        content = {}
        for key in self.request.arguments.keys():
            content[key] = self.get_argument(key)

        result = yield db.update({
            '_id': ObjectId(item_id)
        }, content)

        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def item_insert(self, db):
        content = {}
        for key in self.request.arguments.keys():
            content[key] = self.get_argument(key)

        result = yield db.insert(content)

        raise tornado.gen.Return(result)

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
        # code = self.get_argument('code')
        # resp = yield self.proxy.get_wx_access_token('wx703b3491b593a587', '32fb3722ad1feb96029f2c6ce6ce82b3', code)
        #
        # access_token = resp['access_token']
        # openid = resp['openid']
        # resp = yield self.proxy.get_wx_info(access_token, openid)

        resp = {
            'openid': 'dfksdhfslkdjf',
            'nickname': u'老于',
            'headimgurl': 'http://qtwebmobile.b0.upaiyun.com/qtfm.png'
        }

        # weixin login success
        self.set_secure_cookie('user', resp['openid'])
        self.set_secure_cookie('nickname', resp['nickname'])
        self.set_secure_cookie('headimgurl', resp['headimgurl'])

        self.redirect('/wx/home')


class DateHandler(BaseHandler):
    def get(self):
        self.render('mobile/datepicker.html')