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