__author__ = 'yuxizhou'

import json
import tornado.gen
from handlers import BaseHandler


class ApiDealersHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        c = self.get_argument('c', None)

        if c:
            result = yield self.item_list_by(self.mongodb.dealer, {
                'category': c
            })
        else:
            result = yield self.item_list(self.mongodb.dealer)

        d = []
        for r in result:
            d.append({
                'name': r['name'],
                'address': r['address']
            })

        self.write(json.dumps(d))
        self.finish()