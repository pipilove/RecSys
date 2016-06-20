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
from collections import defaultdict
import datetime
import linecache
from time import sleep

from numpy import loadtxt, append
from numpy import random
import numpy

from scipy import spatial
from numpy import argsort, array, zeros, savetxt
from numpy import dot
from scipy.io import mmwrite, mmread
from scipy.sparse import csr_matrix, vstack
from scipy.sparse.linalg.eigen.lobpcg.lobpcg import pause

from RecSys.MusicRec.Models import User, Item


def get_info_class_list(filename):
    '''
    将用户和歌曲信息读入相应的class中，所有class存在users_list、items_list中
    :param filename:
    :return:
    '''
    file = open(filename, encoding='utf-8')
    users_list = list()
    items_list = list()
    user_ids = list()
    item_ids = list()

    start_time = datetime.datetime.now()
    for line_id, line in enumerate(file):
        if line_id % 100000 == 0:
            print('******** %d ********' % line_id)
            print(datetime.datetime.now() - start_time)
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        if item_id not in item_ids:
            item_ids.append(item_id)
            item_class = Item(item_id=item_id, item_name=item_name, art_id=art_id)
            items_list.append(item_class)
        if user_id not in user_ids:
            user_ids.append(user_id)
            user_class = User(user_id=user_id)
            user_class.add_item(item_class, timestamp, preference=1)
            users_list.append(user_class)
        else:
            users_list[user_ids.index(user_id)].add_item(item_class, timestamp, preference=1)  # 已存在就不会添加
    file.close()
    # print(users_list, len(users_list), items_list, len(items_list))
    return users_list, items_list


def write_info_class_list(users_list, items_list, users_output_filename, items_output_filename):
    '''
    将user和item的class list写入文件
    :param users_list:
    :param items_list:
    :param users_output_filename:
    :param items_output_filename:
    :return:
    '''
    users_output_file = open(users_output_filename, 'w')
    for user_class in users_list:
        users_output_file.write("%s %s" % (user_class.user_id))
    users_output_file.close()


def get_user_item_mat0(users_list, items_list):
    '''
    构建user_item_mat
    :param users_list:
    :param items_list:
    :return:
    '''
    start_time = datetime.datetime.now()
    user_item_mat = zeros([len(users_list), len(items_list)])  # print(user_item_mat.shape)

    for user_class in users_list:
        for item_id in user_class.items_dict.keys():
            user_item_mat[user_class.user_id, item_id] = user_class.items_dict[item_id][1]  # 时间相关调整到后期再考虑

    print(datetime.datetime.now() - start_time)
    return user_item_mat


def get_convert_no_small_dataset_max_item_id(input_filename):
    '''
    计算item最大的id
    :param input_filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    max_item_id = 20000

    start_time = datetime.datetime.now()
    for line_id, line in enumerate(input_file):
        if line_id % 500000 == 0:
            print('******** %d ********' % line_id)
            print(datetime.datetime.now() - start_time)
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        item_id = int(item_id)
        if item_id > max_item_id:
            max_item_id = item_id
    input_file.close()
    return max_item_id


def get_raw_user_item_mat(users_num, items_num, input_filename):
    '''
    构建初始user_item_mat
    :param input_filename:
    :return:
    '''
    start_time = datetime.datetime.now()
    raw_user_item_mat = zeros([users_num, items_num])  # print(user_item_mat.shape)

    input_file = open(input_filename, encoding='utf-8')
    for line in input_file:
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        raw_user_item_mat[int(user_id)][int(item_id)] += 1
    input_file.close()
    print("raw_user_item_mat gotten ,lasting time:", datetime.datetime.now() - start_time)
    return raw_user_item_mat


def get_user_item_mat(user_item_mat_filename):
    '''
    从文件中读取user_item
    :return:
    '''
    lines = linecache.getlines(user_item_mat_filename)
    for line in lines:
        pass


def regularize_user_item_mat(raw_user_item_mat, ratio=1):
    '''
    从初始user_item_mat构建user_item_mat
    :param raw_user_item_mat:
    :return:
    '''
    weight = [-4, 1, 2, 3, 4] * ratio
    user_item_mat = raw_user_item_mat
    for row_id in range(len(user_item_mat)):
        for col_id in range(len(user_item_mat[0])):
            ui = user_item_mat[row_id][col_id]
            if user_item_mat[row_id][col_id] == 0 or user_item_mat[row_id][col_id] == 1 or user_item_mat[row_id][
                col_id] == 2:
                continue
            elif user_item_mat[row_id][col_id] < 0:
                user_item_mat[row_id][col_id] = weight[0]
            # elif user_item_mat[row_id][col_id] < 3:
            # user_item_mat[row_id][col_id] = 0
            # elif user_item_mat[row_id][col_id] < 2:
            # user_item_mat[row_id][col_id] = weight[1]
            elif user_item_mat[row_id][col_id] < 4:
                user_item_mat[row_id][col_id] = weight[2]
            elif user_item_mat[row_id][col_id] < 8:
                user_item_mat[row_id][col_id] = weight[3]
            else:
                user_item_mat[row_id][col_id] = weight[4]
    return user_item_mat


def cal_similar(user_item_mat, new_user_flag=True):
    '''
    计算相关度
    :return:
    '''
    # 构建item_item相似度矩阵
    item_item_mat = dot(user_item_mat.transpose(), user_item_mat)
    # item_item_mat = spatial.distance.squareform(spatial.distance.pdist(user_item_mat.transpose(), metric='cosine'))

    # 构建user_user相似度矩阵
    if new_user_flag:
        user_user_mat = None  # 之后加入新用户重新计算
    else:
        user_user_mat = dot(user_item_mat, user_item_mat.transpose())
        # user_user_mat = spatial.distance.squareform(spatial.distance.pdist(user_item_mat, metric='cosin'))

    return item_item_mat, user_user_mat


def cal_similar_sparse(user_item_sparse_mat, new_user_flag=True):
    '''
    计算相关度
    :return:
    '''
    # 构建item_item相似度矩阵
    item_item_mat = user_item_sparse_mat.transpose().dot(user_item_sparse_mat)
    # item_item_mat = spatial.distance.squareform(spatial.distance.pdist(user_item_mat.transpose(), metric='cosine'))

    # 构建user_user相似度矩阵
    if new_user_flag:
        user_user_mat = None  # 之后加入新用户重新计算
    else:
        user_user_mat = user_item_sparse_mat.dot(user_item_sparse_mat.transpose())
        # user_user_mat = spatial.distance.squareform(spatial.distance.pdist(user_item_mat, metric='cosin'))

    return item_item_mat, user_user_mat


def get_item_item_sparse_dict(item_item_sparse_mat_filename):
    '''
    从item_item_sparse_mat文件中读取数据到item_item_dict
    :return:
    '''
    item_item_dict = dict()
    lines = linecache.getlines(item_item_sparse_mat_filename)[2:-1]
    for line in lines:
        item_id1, item_id2, weight = line.strip().split()
        item_item_dict[int(item_id1), int(item_id2)] = int(weight)
    return item_item_dict


def get_item_item_similar(item_item_sparse_dict, item_id1, item_id2):
    '''
    在item_item_sparse_dict中查找item_id1和item_id2的相似度
    :param item_id1:
    :param item_id2:
    :return:
    '''
    try:
        return item_item_sparse_dict[(item_id1, item_id2)]
    except:
        try:
            return item_item_sparse_dict[(item_id2, item_id1)]
        except:
            return 0


def recommend_one(user_item_mat):
    '''
    对某个用户推荐歌曲
    :param user_item_mat:
    :return:
    '''


def recommend_all(user_item_mat):
    item_item_mat, user_user_mat = cal_similar(user_item_mat)


def user_based_rec_sparse(user_class, user_item_sparse_mat, top_n=50):
    '''
    对用户user_class推荐item
    :param item_item_mat:
    :param user_user_mat:
    :return:
'''
    new_user_item_mat = zeros([1, user_item_sparse_mat.shape[1]])  # 二维数组
    for item_id in user_class.items_dict.keys():
        new_user_item_mat[0][item_id] = user_class.items_dict[item_id][1]
    # print("new_user_item_vec", new_user_item_mat[0])
    new_user_item_mat = regularize_user_item_mat(new_user_item_mat)
    new_user_item_sparse_mat = csr_matrix(new_user_item_mat)
    new_user_item_sparse_vec = new_user_item_sparse_mat[0]  # 实际还是一个稀疏矩阵
    # print("new_user_item_sparse_vec", new_user_item_sparse_vec)

    users_similar = zeros([user_item_sparse_mat.shape[0]])
    rows, cols = user_item_sparse_mat.nonzero()
    rows = set(rows)
    # print(rows, "****")
    for row in rows:
        # print(new_user_item_sparse_vec.dot(user_item_sparse_mat[row].transpose())[0, 0], "....")
        users_similar[row] = new_user_item_sparse_vec.dot(user_item_sparse_mat[row].transpose())[0, 0]
    # print("users_similar", users_similar)
    user_item_sparse_mat = vstack([user_item_sparse_mat, new_user_item_sparse_mat])
    sorted_users_similar_indexs = argsort(-users_similar)[:top_n * 10]
    # print("sorted_users_similar_indexs", sorted_users_similar_indexs)

    rec_item_dict = dict()
    for old_user_item_sparse_vec in user_item_sparse_mat[sorted_users_similar_indexs]:
        rec_item_dict.update(get_rec_list_sparse(new_user_item_sparse_vec, old_user_item_sparse_vec))
        if len(rec_item_dict) >= top_n:
            break
    return rec_item_dict


def get_rec_list_sparse(new_user_item_sparse_vec, old_user_item_sparse_vec, threshold=1):
    rec_item_dict = dict()
    for row, col in old_user_item_sparse_vec.nonzero():
        ui = old_user_item_sparse_vec[row, col]
        if ui > threshold and new_user_item_sparse_vec[row, col] == 0:
            rec_item_dict[col] = ui
    return rec_item_dict


def user_based_rec(user_class, user_item_mat, top_n=50):
    '''
    对用户user_class推荐item
    :param item_item_mat:
    :param user_user_mat:
    :return:
'''
    new_user_item_mat = zeros([1, user_item_mat.shape[1]])  # 二维数组
    for item_id in user_class.items_dict.keys():
        new_user_item_mat[0][item_id] = user_class.items_dict[item_id][1]
    # print("new_user_item_vec", new_user_item_mat[0])
    new_user_item_mat = regularize_user_item_mat(new_user_item_mat)
    new_user_item_vec = new_user_item_mat[0]
    # print("new_user_item_vec", new_user_item_vec)

    users_similar = array([dot(new_user_item_vec, old_user_item_vec) for old_user_item_vec in user_item_mat])
    # print("users_similar", users_similar)
    user_item_mat = append(user_item_mat, new_user_item_mat, axis=0)
    sorted_users_similar_indexs = argsort(-users_similar)[:top_n * 10]
    # print("sorted_users_similar_indexs", sorted_users_similar_indexs)

    rec_item_dict = dict()
    for old_user_item_vec in user_item_mat[sorted_users_similar_indexs]:
        rec_item_dict.update(get_rec_list(new_user_item_vec, old_user_item_vec))
        # for rec_item_key, rec_item_value in get_rec_list(new_user_item_vec, old_user_item_vec).items():
        # try:
        # rec_item_dict[rec_item_key] += rec_item_value
        # except:
        # rec_item_dict[rec_item_key] = rec_item_value
        # print(rec_item_dict)
        if len(rec_item_dict) >= top_n:
            break
    return rec_item_dict


def get_rec_list(new_user_item_vec, old_user_item_vec, threshold=1):
    '''
    根据old_user_item_vec得到一个推荐列表推荐给user_new
    :param new_user_item_vec:
    :param old_user_item_vec:
    :return:
    '''
    rec_item_dict = dict()
    for index, (new_ui, ui) in enumerate(zip(new_user_item_vec, old_user_item_vec)):
        if new_ui == 0 and ui > threshold:
            rec_item_dict[index] = ui
    return rec_item_dict


def get_rec_list0(new_user_item_vec, old_user_item_vec):
    '''
    根据old_user_item_vec得到一个推荐列表推荐给user_new
    :param new_user_item_vec:
    :param old_user_item_vec:
    :return:
    '''
    rec_item_array = zeros([new_user_item_vec.shape[0]])  # 一维数组
    for index, ui in enumerate(new_user_item_vec):
        if ui == 0:
            rec_item_array[index] = old_user_item_vec[index]
    return rec_item_array


def get_new_user_item_dict(new_user):
    '''
    从新用户class中获取用户喜欢的item的dict，其中dict[item_id]=3代表user喜欢item_id的程度为3
    :param new_user:
    :return:
    '''
    new_user_item_dict = dict()
    for item_id, user_item_infor in new_user.items_dict.items():
        if user_item_infor[1] != 0:
            new_user_item_dict[item_id] = user_item_infor[1]
    return new_user_item_dict


def get_final_rec_item_list(new_user_item_dict, rec_item_dict, item_item_sparse_dict, top_n=10):
    '''
    计算new_user_item_dict和rec_item_dict各个item之间的相关度，排序选出最后的推荐列表
    :return:
    '''
    final_rec_item_dict = defaultdict(int)
    for rec_item_id, rec_item_weight in rec_item_dict.items():
        for new_user_item_id, new_user_item_weight in new_user_item_dict.items():
            final_rec_item_dict[rec_item_id] += get_item_item_similar(item_item_sparse_dict, rec_item_id,
                                                                      new_user_item_id) * rec_item_weight * new_user_item_weight
    sorted_final_rec_item_tuples = sorted(final_rec_item_dict.items(), key=lambda i: i[1], reverse=True)[:top_n]
    print(sorted_final_rec_item_tuples)
    return [t[0] for t in sorted_final_rec_item_tuples if t[1] is not 0]


def item_based_rec(new_user_item_dict, item_item_sparse_dict, top_n=10):
    '''
    基于item的推荐
    :param new_user_item_dict:
    :param item_item_sparse_dict:
    :return:
    '''
    cmp_item_set = set()
    for i in item_item_sparse_dict.keys():
        if i[0] not in new_user_item_dict.keys():
            cmp_item_set.add(i[0])
        if i[1] not in new_user_item_dict.keys():
            cmp_item_set.add(i[1])
    final_item_based_rec_dict = defaultdict(int)
    for cmp_item_id in cmp_item_set:
        for new_user_item_id in new_user_item_dict:
            final_item_based_rec_dict[cmp_item_id] += get_item_item_similar(item_item_sparse_dict, cmp_item_id,
                                                                            new_user_item_id)
    final_item_based_rec_tuples = sorted(final_item_based_rec_dict.items(), key=lambda i: i[1], reverse=True)[:top_n]
    print(final_item_based_rec_tuples)
    return [t[0] for t in final_item_based_rec_tuples]


def get_top_items(user_item_mat, top_n=100, top_n_items_filename=r'..\..\datasets\lastfm-dataset-1K\top_n_items.tsv',
                  top_n_items_cnt_filename=r'..\..\datasets\lastfm-dataset-1K\top_n_items_cnt.tsv'):
    '''
    获得用户听的最多的topn个item
    :return:
    '''
    top_n_items_cnt = numpy.sum(user_item_mat, axis=0)
    savetxt(top_n_items_cnt_filename, [top_n_items_cnt], fmt="%d")
    top_n_items = argsort(-top_n_items_cnt)[0:top_n]
    savetxt(top_n_items_filename, [top_n_items], fmt="%d")


if __name__ == '__main__':
    s = datetime.datetime.now()
    convert_no_small_filename = r'.\datasets\lastfm-dataset-1K\convert_no_small_dataset20.tsv'
    train_filename = r'.\datasets\lastfm-dataset-1K\train_data.tsv'
    raw_user_item_mat_filename = r'.\datasets\lastfm-dataset-1K\raw_user_item_mat.npy'
    user_item_mat_filename = r'.\datasets\lastfm-dataset-1K\user_item_mat3.npy'
    user_item_sparse_mat_filename = r'.\datasets\lastfm-dataset-1K\user_item_sparse_mat3.mtx'
    item_item_csr_mat_filename = r'.\datasets\lastfm-dataset-1K\item_item_csr_mat3.mtx'

    # 计算raw_user_item_mat并写入文档
    # max_item_id = get_convert_no_small_dataset_max_item_id(convert_no_small_filename)#284409
    # max_item_id = 284409_m
    # raw_user_item_mat = get_raw_user_item_mat(users_num=987, items_num=max_item_id + 1, input_filename=convert_no_small_filename)
    # savetxt(raw_user_item_mat_filename, raw_user_item_mat, fmt="%d")
    # print("raw_user_item_mat written finished !!! ")

    # 计算user_item_mat并写入文档
    # raw_user_item_mat = loadtxt(raw_user_item_mat_filename, dtype=int)
    # user_item_mat = regularize_user_item_mat(raw_user_item_mat)
    # savetxt(user_item_mat_filename, user_item_mat, fmt="%d")
    # print("user_item_mat written finished !!! ")

    # 转换user_item_sparse_mat并存入文档
    # user_item_mat = loadtxt(user_item_mat_filename, dtype=int)  # user_item_mat1 loading last 0:07:29.984140
    # user_item_sparse_mat = csr_matrix(user_item_mat)
    # mmwrite(user_item_sparse_mat_filename, user_item_sparse_mat)
    # print("user_item_sparse_mat written finished !!! ")

    # 计算item_item_sparse_mat并存入文档
    user_item_sparse_mat = mmread(user_item_sparse_mat_filename)
    user_item_sparse_mat = csr_matrix(user_item_sparse_mat)
    # item_item_sparse_mat, _ = cal_similar_sparse(user_item_sparse_mat)
    # mmwrite(item_item_csr_mat_filename, item_item_sparse_mat)
    # print("item_item_sparse_mat written finished !!! ")
    print("user_item_sparse_mat read done!", datetime.datetime.now() - s)

    item_item_sparse_dict = get_item_item_sparse_dict(item_item_csr_mat_filename)
    print("item_item_sparse_dict read done!", datetime.datetime.now() - s)

    random.seed(1)

    # raw_user_item_mat = random.randint(0, 6, (4, 5))
    # user_item_mat = regularize_user_item_mat(raw_user_item_mat)
    # print(user_item_mat)

    user_id = 1000
    items_dict = dict()
    for i in range(10):
        items_dict[random.randint(0, 200000)] = (None, 1)
        items_dict[random.randint(0, 200000)] = (None, 1)
    new_user = User(user_id=user_id, items_dict=items_dict)

    new_user_item_dict = get_new_user_item_dict(new_user)
    # print("new_user_item_dict", new_user_item_dict)

    # item_based && user_based recommendation
    # rec_item_dict = user_based_rec(new_user, user_item_mat)
    rec_item_dict = user_based_rec_sparse(new_user, user_item_sparse_mat)
    print("rec_item_dict done!", datetime.datetime.now() - s)
    # print("rec_item_dict : ", rec_item_dict)
    final_rec_list = get_final_rec_item_list(new_user_item_dict, rec_item_dict, item_item_sparse_dict)


    # just item_based recommendation
    # final_item_based_rec_list = item_based_rec(new_user_item_dict, item_item_sparse_dict)

    print(datetime.datetime.now() - s)

