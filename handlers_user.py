# coding=utf-8
__author__ = 'yuxizhou'

import tornado
import tornado.gen
from handlers import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        to = self.get_argument("next", "/reserve")
        self.render('login.html', user=None, msg=None, next=to)

    @tornado.gen.coroutine
    def post(self):
        try:
            email = self.get_argument('email')
            password = self.get_argument('password')
            to = self.get_argument("next", "/reserve")
            user = yield self.mongodb.user.find_one({'email': email, 'password': password})
            if user:
                self.set_secure_cookie('user', str(user['_id']))
                self.redirect(to)
            else:
                self.render('login.html', user=None, msg=u'密码错误')
        except Exception, e:
            print e
            self.set_status(400)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html', user=None, msg=None)

    @tornado.gen.coroutine
    def post(self):
        try:
            email = self.get_argument('email')
            password = self.get_argument('password')
            nick = self.get_argument('nick')

            if email == '' or password == '' or nick == '':
                self.render('register.html', user=None, msg=u'字段均不能为空')
                return

            # check if email is exists
            document = yield self.mongodb.user.find_one({'email': email})
            if document:
                self.render('register.html', user=None, msg=u'该邮箱已经注册')
                return

            # check
            document = yield self.mongodb.user.find_one({'nick': nick})
            if document:
                self.render('register.html', user=None, msg=u'该名号已存在')
                return

            future = self.mongodb.user.insert({
                'email': email,
                'password': password,
                'nick': nick
            })
            user_id = yield future
            self.set_secure_cookie('user', str(user_id))
            self.redirect('/reserve')
        except Exception, e:
            print e
            self.set_status(400)