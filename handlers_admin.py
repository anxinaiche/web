__author__ = 'yuxizhou'

import tornado.web
import tornado.gen
from handlers import BaseHandler


class AdminHandler(BaseHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("admin")
        if user_id == 'leshou':
            return user_id
        else:
            return None


class AdminHandler(AdminHandler):
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


class AdminHomeHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/home.html')


class AdminReservesHandler(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        reserves = yield self.item_list(self.mongodb.reservewx)
        self.render('admin/reserves.html', reserves=reserves)


class AdminReservesDeleteHandler(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.item_remove(self.mongodb.reservewx, item_id)
        self.redirect('/admin/reserves')


######################   brands   ###################

class AdminBrandsHandler(AdminHandler):
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


class AdminBrandsNewHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/brand_new.html', item=None)


class AdminBrandsDeleteHandler(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.item_remove(self.mongodb.brand, item_id)
        self.redirect('/admin/brands')


class AdminBrandsEditHandler(AdminHandler):
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


class AdminDealersHandler(AdminHandler):
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


class AdminDealersNewHandler(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        brands = yield self.item_list(self.mongodb.brand)
        self.render('admin/dealer_new.html', item=None, brands=brands)


class AdminDealersDeleteHandler(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, item_id):
        result = yield self.item_remove(self.mongodb.dealer, item_id)
        self.redirect('/admin/dealers')


class AdminDealersEditHandler(AdminHandler):
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