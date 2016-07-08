#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Cause Effect'
__author__ = '皮'
__mtime__ = '6/29/2016-029'
__email__ = 'pipisorry@126.com'
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
import numpy as np
from scipy import spatial

# m = np.array([[0, 1, 0], [0, 1, 1], [0, 1, 0], [1, 0, 1]]).transpose()

# item-user矩阵
m = np.array([[0, 1, 0, 1, 0],
              [0, 1, 1, 0, 0],
              [0, 1, 0, 1, 0],
              [1, 0, 1, 0, 1],
              [1, 0, 1, 1, 0],
              [0, 1, 0, 0, 1],
              [0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [1, 1, 0, 1, 0],
              [0, 1, 0, 1, 1]]).transpose()


def causal_effect(m):
    effect = lambda u, v: u.dot(v) / sum(u) - (1 - u).dot(v) / sum(1 - u)
    return spatial.distance.squareform(spatial.distance.pdist(m, metric=effect))


def p_x(m):
    '''
    计算每个item的p(y)
    '''
    return m.sum(axis=1) / len(m[0])


p_x = p_x(m)
print(p_x)
lift_array = causal_effect(m)
print(lift_array)
