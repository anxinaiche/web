__author__ = 'yuxizhou'

import motor

client = motor.MotorClient()
db = client.test_database

from tornado.ioloop import IOLoop


def my_callback(result, error):
    print 'result', repr(result)
    IOLoop.instance().stop()

document = {'key': 'value'}
db.test_collection.insert(document, callback=my_callback)
IOLoop.instance().start()