#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'UserCF recommendation: For the give rating matrix, recommendation top-3 items for each user. Using 5 neighbors, Comparing the method of normalization and non-normalization'
__author__ = 'pika'
__mtime__ = '16-7-4'
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
import pandas as pd
from scipy import spatial

NUM_NEIGHBORS = 5
NUM_RECOMS = 3

ui_mat_df = pd.read_excel(r'./rating+matrix.xlsx', header=0).T.replace(to_replace=' ', value=np.NaN).astype(float)
# print(ui_mat_df.iloc[:8, :4])


def my_pearson(u, v):
    '''
    计算向量u和v的相似度并返回
    '''
    common_index = np.array([True if not np.isnan(ui) and not np.isnan(vi) else False for ui, vi in zip(u, v)])
    u = u[common_index]
    v = v[common_index]
    # print(u, v)
    sig_weight = min(u.size, 50) / 50  # significance weighting
    similar = (1 - spatial.distance.correlation(u, v)) * sig_weight if np.unique(u).size > 1 and np.unique(v).size > 1 else 0.0
    # similar = (1 - spatial.distance.cosine(u, v)) * sig_weight if np.unique(u).size > 1 and np.unique(v).size > 1 else 0.0
    return similar


# 计算所有用户间的相似度, 个性化权重
uu_similar_array = spatial.distance.squareform(spatial.distance.pdist(ui_mat_df.values, metric=my_pearson))
for i in range(len(uu_similar_array)):  # 只取最相近的NUM_NEIGHBORS个邻居，且去除负值
    uu_similar_array[i][uu_similar_array[i].argsort()[:-NUM_NEIGHBORS]] = 0
    uu_similar_array[i][uu_similar_array[i] < 0] = 0
# print(uu_similar_array[:3, ])

# data normalization: normalized user item rating matrix
user_rat_mean_series = ui_mat_df.mean(axis=1)  # 每个用户打分均值（不包含未打分）
# print(user_rat_mean_series)
norm_ui_df = ui_mat_df.sub(user_rat_mean_series, axis=0).fillna(0)
# print(norm_ui_df.iloc[:10, :4])

# normalization评分预测
ui_predict_array = user_rat_mean_series.reshape(-1, 1) + \
                   uu_similar_array.dot(norm_ui_df) / uu_similar_array.sum(axis=1).reshape(-1, 1)
np.set_printoptions(precision=1)
# print(ui_predict_array)

# 推荐
ui_predict_array[ui_mat_df.values > 0] = 0
# print(ui_predict_array)
ui_rec_df = pd.DataFrame(ui_predict_array.argsort(axis=1)[:, -1:-NUM_RECOMS - 1:-1], index=ui_mat_df.index)
print(ui_rec_df)

item_names_dict = dict(zip(list(range(len(ui_mat_df.columns))), ui_mat_df.columns))
for key in item_names_dict:
    ui_rec_df.replace(key, item_names_dict[key], inplace=True)
ui_rec_df.to_csv('./ui_rec.csv')
