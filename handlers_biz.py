__author__ = 'yuxizhou'

import tornado.web
import tornado.gen
from handlers import BaseHandler
from bson.objectid import ObjectId


class HomeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        user_id = self.get_current_user()
        if user_id:
            user = yield self.mongodb.user.find_one({'_id': ObjectId(user_id)})
            self.render('home.html', user=user)
        else:
            self.render('home.html', user=None)


class ReserveHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        user_id = self.get_current_user()
        user = yield self.mongodb.user.find_one({'_id': ObjectId(user_id)})

        self.render('reserve.html', user=user)


class ReserveMHandler(BaseHandler):
    @tornado.gen.coroutine
    def post(self):
        time = self.get_argument('time')
        area = self.get_argument('area')
        custom_area = self.get_argument('custom-area')
        phone = self.get_argument('phone')
        wx_name = self.get_argument('wx-name')

        future = self.mongodb.reservewx.insert({
            'time': time,
            'area': area,
            'custom_area': custom_area,
            'phone': phone,
            'wx_name': wx_name,
        })
        rid = yield future

        if rid:
            self.render('reserve_success.html')
        else:
            self.render('reserve_fail.html')
