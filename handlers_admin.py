__author__ = 'yuxizhou'

import tornado.web
import tornado.gen
from bson import ObjectId


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


class Admin4sHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/4s.html')


class AdminBrandsHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        cursor = self.mongodb.brand.find()
        brand = []
        for item in (yield cursor.to_list(length=None)):
            brand.append(item)

        self.render('admin/brands.html', brand=brand)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        brand = self.get_argument('brand')

        for b in brand.split(' '):
            if b:
                self.mongodb.brand.insert({
                    'name': b
                })
        self.redirect('/admin/brands')


class AdminBrandsNewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/brand_new.html')


class AdminBrandsDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.mongodb.brand.remove({
            '_id': ObjectId(item_id)
        })
        self.redirect('/admin/brands')


class AdminBrandsEditHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        item = yield self.mongodb.brand.find_one({
            '_id': ObjectId(item_id)
        })
        self.render('admin/brand_edit.html', item=item)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, item_id):
        brand = self.get_argument('brand')

        result = yield self.mongodb.brand.update({
            '_id': ObjectId(item_id)
        }, {
            'name': brand
        })

        self.redirect('/admin/brands')
