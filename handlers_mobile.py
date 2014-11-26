__author__ = 'yuxizhou'

import tornado.web
import tornado.gen
from handlers import BaseHandler


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
            self.render('mobile/wx_reserve_success.html')
        else:
            self.render('mobile/wx_reserve_fail.html')


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


class WXHistoryHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        self.render('mobile/ratchet/m_ratchet_history.html')