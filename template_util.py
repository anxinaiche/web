# coding=utf-8
__author__ = 'yuxizhou'
from datetime import datetime, timedelta


def weekday(day):
    d = datetime.today() + timedelta(days=day)
    result = d.strftime('%m月%d日 ')

    week = d.weekday()
    if week == 0:
        result += '周日'
    elif week == 1:
        result += '周一'
    elif week == 2:
        result += '周二'
    elif week == 3:
        result += '周三'
    elif week == 4:
        result += '周四'
    elif week == 5:
        result += '周五'
    elif week == 6:
        result += '周六'

    return result


def get_or_none(item, name):
    if item and (name in item):
        return item[name]
    else:
        return ""