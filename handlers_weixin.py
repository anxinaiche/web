# coding=utf-8
__author__ = 'yuxizhou'

import tornado.web
import tornado.gen
from handlers import BaseHandler


class WXHandler(BaseHandler):
    def get(self):
        echo_str = self.get_argument("echostr", None, True)
        self.set_header("content-type", "text/html")
        self.write(echo_str)
        self.finish()


class WXOAuthHandler(BaseHandler):
    """
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx703b3491b593a587&redirect_uri=http%3A%2F%2F121.199.5.143%2Foauth_response&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect
    """
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

        self.redirect('/wx/orders')


class WXReserveHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        info = {
            'openid': self.get_secure_cookie('user'),
            'nickname': self.get_secure_cookie('nickname'),
            'headimgurl': self.get_secure_cookie('headimgurl'),
        }

        brands = yield self.item_list(self.mongodb.brand)
        group_brands = {}
        for b in brands:
            if b.get('pinyin_init', 'w') in group_brands:
                group_brands[b.get('pinyin_init', 'w')].append(b)
            else:
                group_brands[b.get('pinyin_init', 'w')] = [b]

        self.render('mobile/ratchet/m_ratchet_reserve.html', info=info, brands=group_brands)

    @tornado.gen.coroutine
    def post(self):
        time = self.get_argument('time')
        area = self.get_argument('area')
        custom_area = self.get_argument('custom-area', '')
        phone = self.get_argument('phone')
        wx_name = self.get_argument('wx-name')
        wx_openid = self.get_argument('wx-openid')

        future = self.mongodb.reservewx.insert({
            'time': time,
            'area': area,
            'custom_area': custom_area,
            'phone': phone,
            'wx_name': wx_name,
            'wx_openid': wx_openid,
        })
        rid = yield future

        if rid:
            self.render('mobile/ratchet/m_ratchet_success.html')
        else:
            self.render('mobile/ratchet/wx_reserve_fail.html')


class WXMyHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        info = {
            'openid': self.get_secure_cookie('user'),
            'nickname': self.get_secure_cookie('nickname'),
            'headimgurl': self.get_secure_cookie('headimgurl'),
        }
        self.render('mobile/ratchet/m_ratchet_my.html', info=info)


class WXHomeHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        self.render('mobile/ratchet/m_ratchet_home.html')


class WXOrdersHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        info = {
            'openid': self.get_secure_cookie('user'),
            'nickname': self.get_secure_cookie('nickname'),
            'headimgurl': self.get_secure_cookie('headimgurl'),
        }

        reserves = yield self.item_list_by(self.mongodb.reservewx, {
            'wx_openid': info['openid']
        })
        self.render('mobile/ratchet/m_ratchet_orders.html', info=info, reserves=reserves)


class WXTestHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        self.render('mobile/ratchet/m_ratchet_test.html')


class WXReportHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self, report_id):
        report = yield self.item_get(self.mongodb.report, report_id)
        self.render('mobile/ratchet/m_ratchet_report.html', report=report)