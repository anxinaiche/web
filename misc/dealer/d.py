# coding=utf-8
__author__ = 'yuxizhou'

from pymongo import MongoClient

client = MongoClient()
db = client.web


with open('baoma', 'r') as fp:
    dealer = []
    for l in fp:
        line = l.strip()
        if line:
            if len(dealer) == 0:
                dealer.append(line)
            elif len(dealer) == 1:
                dealer.append(line)
                db.dealer.insert({
                    'name': dealer[0],
                    'category': '宝马',
                    'address': dealer[1]
                })
        else:
            dealer = []


# db.dealer.insert()