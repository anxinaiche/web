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
