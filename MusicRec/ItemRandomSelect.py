#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '3/20/2015-020'
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
from numpy import random
from numpy.ma import add


def randomSelect(item_list):
    '''
    随机选择带权重的list中的某个item,并返回其下标（item_list权重和可以不为1）
    :param item_list:
    :return:
    '''
    accu_item_list = add.accumulate(item_list)
    # print(type(accu_item_list))
    random_select = random.random() * accu_item_list[-1]
    for accu_item_id, accu_item in enumerate(accu_item_list):
        if accu_item > random_select:
            return accu_item_id


def cal_ratio(item_list):
    '''
    计算每个item在item_list中的比重
    :param item_list:
    :return:
    '''
    all_sum = sum(item_list)
    for i in item_list:
        print(i / all_sum)


if __name__ == '__main__':
    item_list = [0.1, 0.4, 0.6, 0.8, 0.3]
    cal_ratio(item_list)

    item_list_all = []
    item_list_cnt = []
    for i in range(100000):
        selected_item_id = randomSelect(item_list)
        item_list_all.append(selected_item_id)
    for i in range(len(item_list)):
        item_list_cnt.append(item_list_all.count(i))
    cal_ratio(item_list_cnt)
