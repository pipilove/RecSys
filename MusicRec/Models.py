#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '3/19/2015-019'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""


class User:
    '''
    implement of user property
    '''

    def __init__(self, user_id, user_name=None, passwd=None, gender=None, age=None, country=None, items_dict=None):
        self.user_id = user_id
        self.user_name = user_name
        self.passwd = passwd
        self.gender = gender
        self.age = age
        self.country = country
        if items_dict == None:
            self.items_dict = dict()
        else:
            self.items_dict = items_dict
            # self.item_ids = None

    def add_item(self, item, timestamp, preference):
        if item.item_id not in self.items_dict.keys():
            self.items_dict[item.item_id] = (timestamp, preference)
        else:
            self.items_dict[item.item_id] = (timestamp, preference + self.items_dict[item.item_id][1])

    def update_item(self, preference):
        pass


class Item:
    '''
    implement of item property
    '''

    def __init__(self, item_id, item_name, art_id=None, art_name=None, item_link=None, item_tag=None):
        self.item_id = item_id
        self.item_name = item_name
        self.art_id = art_id
        self.art_name = art_name
        self.item_link = item_link
        self.item_tag = item_tag

    def update_item(self):
        pass


class Art:
    '''
    implement of art
    '''

    def __init__(self, art_id, art_name):
        self.art_id = art_id
        self.art_name = art_name

