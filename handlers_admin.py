__author__ = 'yuxizhou'

import tornado.web
import tornado.gen
from bson import ObjectId
import pymongo


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("admin")
        if user_id == 'leshou':
            return user_id
        else:
            return None

    @property
    def mongodb(self):
        return self.application.mongodb

    @tornado.gen.coroutine
    def item_list(self, db):
        cursor = db.find()
        result = []
        cursor.sort([('_id', pymongo.DESCENDING)])
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


class AdminHandler(BaseHandler):
    def get(self):
        self.render('admin/login.html')

    def post(self):
        u = self.get_argument('username')
        p = self.get_argument('password')

        if u == 'leshou' and p == 'leshou2014':
            self.set_secure_cookie('admin', u)
            self.redirect('/admin/home')
        else:
            self.render('admin/login.html')


class AdminHomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/home.html')


class AdminReservesHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        reserves = yield self.item_list(self.mongodb.reservewx)
        self.render('admin/reserves.html', reserves=reserves)


class AdminReservesDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.item_remove(self.mongodb.reservewx, item_id)
        self.redirect('/admin/reserves')


######################   brands   ###################

class AdminBrandsHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        items = yield self.item_list(self.mongodb.brand)
        self.render('admin/brands.html', brand=items)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        result = yield self.item_insert(self.mongodb.brand)
        self.redirect('/admin/brands')


class AdminBrandsNewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/brand_new.html', item=None)


class AdminBrandsDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.item_remove(self.mongodb.brand, item_id)
        self.redirect('/admin/brands')


class AdminBrandsEditHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        item = yield self.item_get(self.mongodb.brand, item_id)
        self.render('admin/brand_new.html', item=item)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, item_id):
        result = yield self.item_update(self.mongodb.brand, item_id)
        self.redirect('/admin/brands')


######################   dealers   ###################


class AdminDealersHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        category = self.get_argument('category', None)

        if category:
            items = yield self.item_list_by(self.mongodb.dealer, {
                'category': category
            })
        else:
            items = yield self.item_list(self.mongodb.dealer)

        brands = yield self.item_list(self.mongodb.brand)
        self.render('admin/dealers.html', items=items, brands=brands)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        result = yield self.item_insert(self.mongodb.dealer)
        self.redirect('/admin/dealers')


class AdminDealersNewHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        brands = yield self.item_list(self.mongodb.brand)
        self.render('admin/dealer_new.html', item=None, brands=brands)


class AdminDealersDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.item_remove(self.mongodb.dealer, item_id)
        self.redirect('/admin/dealers')


class AdminDealersEditHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        item = yield self.item_get(self.mongodb.dealer, item_id)
        brands = yield self.item_list(self.mongodb.brand)
        self.render('admin/dealer_new.html', item=item, brands=brands)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, item_id):
        result = yield self.item_update(self.mongodb.dealer, item_id)
        self.redirect('/admin/dealers')