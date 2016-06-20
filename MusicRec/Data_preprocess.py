#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '3/17/2015-017'
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
import datetime
import random

from numpy import array


def convert_raw_no(input_filename, output_filename):
    '''
    填补userid-timestamp-artid-artname-traid-traname.tsv文件中缺失的traid,重新对user_id, item_id编号
    :param filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    output_file = open(output_filename, 'w', encoding='utf-8')

    user_ids = list()

    item_name_list = list()
    item_id_list = list()
    new_item_id_list = list()
    new_item_id = 0

    art_name_list = list()
    art_id_list = list()
    new_art_id_list = list()
    new_art_id = 0

    start_time = datetime.datetime.now()

    for line_id, line in enumerate(input_file):
        if line_id % 100000 == 0:
            print('******** %d ********' % line_id)
            end_time = datetime.datetime.now()
            print(end_time - start_time)
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        # print(art_id_list)
        # print(new_art_id_list)
        # print(art_name_list)
        # print(art_id, art_name, item_id, item_name)

        if art_id != '':
            if art_id in art_id_list:
                art_id = new_art_id_list[art_id_list.index(art_id)]
            else:
                art_id_list.append(art_id)
                new_art_id_list.append(new_art_id)
                art_name_list.append(art_name)
                art_id = new_art_id
                new_art_id += 1
        else:
            if art_name in art_name_list:
                art_id = new_art_id_list[art_name_list.index(art_name)]
            else:
                art_name_list.append(art_name)
                art_id = new_art_id
                new_art_id += 1
                art_id_list.append(art_id)
                new_art_id_list.append(art_id)

        if user_id not in user_ids:
            user_ids.append(user_id)
        user_id = user_ids.index(user_id)

        if item_id != '':
            if item_id in item_id_list:
                item_id = new_item_id_list[item_id_list.index(item_id)]
            else:
                item_id_list.append(item_id)
                new_item_id_list.append(new_item_id)
                item_name_list.append(item_name)
                item_id = new_item_id
                new_item_id += 1
        else:
            if item_name in item_name_list:
                item_id = new_item_id_list[item_name_list.index(item_name)]
            else:
                item_name_list.append(item_name)
                item_id = new_item_id
                new_item_id += 1
                item_id_list.append(item_id)
                new_item_id_list.append(item_id)

        # line_str = [str(i) for i in [user_id, timestamp, art_id, art_name, item_id, item_name]]
        # output_file.write('\t'.join(line_str) + '\n')
        output_file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (user_id, timestamp, art_id, art_name, item_id, item_name))
    input_file.close()
    output_file.close()


def del_none(input_filename, output_filename):
    '''
    删除art_id或者item_id为空的行
    :param input_filename:
    :param output_filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    output_file = open(output_filename, 'w', encoding='utf-8')

    start_time = datetime.datetime.now()
    for line_id, line in enumerate(input_file):
        if line_id % 100000 == 0:
            print('******** %d ********' % line_id)
            # if line_id > 1000000: break
            print(datetime.datetime.now() - start_time)
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        if art_id == '' or item_id == '':
            continue
        output_file.write(line)
    input_file.close()
    output_file.close()


def sample_small_data(input_filename, output_filename):
    '''
    从大数据集中每隔10个数据采样1个数据组成小数据集
    :param input_filename:
    :param output_filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    output_file = open(output_filename, 'w', encoding='utf-8')

    start_time = datetime.datetime.now()
    for line_id, line in enumerate(input_file):
        # if line_id % 3 == 0:
        if line_id % 20 == 0:
            output_file.write(line)
    print(datetime.datetime.now() - start_time)
    input_file.close()
    output_file.close()


def convert_no(input_filename, output_filename):
    '''
    将user_id, art_id, item_id转换成简单形式
    :param input_filename:
    :param output_filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    output_file = open(output_filename, 'w', encoding='utf-8')

    user_id_list = list()
    new_user_id = 0
    art_id_list = list()
    new_art_id = 0
    item_id_list = list()
    new_item_id = 0

    start_time = datetime.datetime.now()
    for line_id, line in enumerate(input_file):
        if line_id % 500000 == 0:
            print('******** %d ********' % line_id)
            print(datetime.datetime.now() - start_time)

        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        # user_id = str(int(user_id.split('user_', 1)[1]) - 1)
        try:
            user_id = user_id_list.index(user_id)
        except:
            user_id_list.append(user_id)
            user_id = new_user_id
            new_user_id += 1

        try:
            art_id = art_id_list.index(art_id)
        except:
            art_id_list.append(art_id)
            art_id = new_art_id
            new_art_id += 1

        # if art_id not in art_id_list:
        # art_id_list.append(art_id)
        # art_id = art_id_list.index(art_id)

        try:
            item_id = item_id_list.index(item_id)
        except:
            item_id_list.append(item_id)
            item_id = new_item_id
            new_item_id += 1

        output_file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (user_id, timestamp, art_id, art_name, item_id, item_name))
    input_file.close()
    output_file.close()


def get_train_test(input_filename, train_filename, test_filename):
    '''
    分割原有数据集为trainning set和test set
    :param input_filename:
    :param train_filename:
    :param test_filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    train_file = open(train_filename, 'w', encoding='utf-8')
    test_file = open(test_filename, 'w', encoding='utf-8')
    # user_ids_dict = dict()
    # for line in input_file:
    # user_id = line.strip().split('\t', 1)[0]
    # user_ids_dict[user_id] += 1
    # input_file.seek(0)
    for line in input_file:
        if random.random() > 0.3:
            train_file.write(line)
        else:
            test_file.write(line)

    input_file.close()
    train_file.close()
    test_file.close()


if __name__ == '__main__':
    # raw_input_filename = r'\\tsclient\E\machine_learning\datasets\lastfm-dataset-1K\userid-timestamp-artid-artname-traid-traname2.tsv'
    # raw_input_filename = r'E:\machine_learning\datasets\lastfm-dataset-1K\userid-timestamp-artid-artname-traid-traname.tsv'
    # input_filename = r'E:\machine_learning\datasets\lastfm-dataset-1K\userid-timestamp-artid-artname-traid-traname2.tsv'

    small_dataset_filaname = r'.\datasets\lastfm-dataset-1K\small_dataset.tsv'
    convert_no_small_filename = r'.\datasets\lastfm-dataset-1K\convert_no_small_dataset20.tsv'
    train_filename = r'.\datasets\lastfm-dataset-1K\train_data.tsv'
    test_filename = r'.\datasets\lastfm-dataset-1K\test_data.tsv'

    # del_none(raw_input_filename, del_none_filename)
    # sample_small_data(del_none_filename, small_dataset_filaname)
    # convert_no(small_dataset_filaname, convert_no_small_filename)
    # get_item_infor(convert_no_small_filename)
    # get_train_test(convert_no_small_filename, train_filename, test_filename)


def get_item_infor(input_filename, item_infor_filename=r'..\..\datasets\lastfm-dataset-1K\item_infor.tsv'):
    '''
    获取item的信息：item_id, item_name, art_name, item_link并存入文件中
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    item_infor_file = open(item_infor_filename, 'w', encoding='utf-8')

    item_ids_set = set()
    start_time = datetime.datetime.now()
    for line_id, line in enumerate(input_file):
        if line_id % 100000 == 0:
            print('******** %d ********' % line_id)
            print(datetime.datetime.now() - start_time)
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        if item_id not in item_ids_set:
            item_ids_set.add(item_id)
            item_infor_file.write("%s\t%s\t%s\n" % (item_id, item_name, art_name))
    input_file.close()
    item_infor_file.close()


def data_preprocess0(input_filename, output_filename):
    '''
    填补userid-timestamp-artid-artname-traid-traname.tsv文件中缺失的traid,重新对user_id, item_id编号
    :param filename:
    :return:
    '''
    input_file = open(input_filename, encoding='utf-8')
    output_file = open(output_filename, 'w', encoding='utf-8')

    user_ids = list()

    item_name_id_dict = dict()
    new_item_id = 0

    new_art_id = 0
    art_name_id_dict = dict()

    for line_id, line in enumerate(input_file):
        if line_id % 100000 == 0:
            print('******** %d ********' % line_id)
        user_id, timestamp, art_id, art_name, item_id, item_name = array(line.strip().split('\t'))
        if art_name in art_name_id_dict.keys():
            if art_id != '':
                if art_name_id_dict[art_name].split('#')[0] == art_id:
                    art_id = art_name_id_dict[art_name].split('#')[1]
                else:
                    art_id = new_art_id
                    new_art_id += 1
            else:
                art_id = art_name_id_dict[art_name].split('#')[1]
        else:
            art_name_id_dict[art_name] = art_id + '#' + str(new_art_id)
            art_id = new_art_id
            new_art_id += 1

        if user_id not in user_ids:
            user_ids.append(user_id)
        user_id = user_ids.index(user_id)

        if item_name in item_name_id_dict.keys():
            if item_id != '':
                if item_name_id_dict[item_name].split('#')[0] == item_id:
                    item_id = item_name_id_dict[item_name].split('#')[1]
                else:
                    item_id = new_item_id
                    new_item_id += 1
            else:
                item_id = item_name_id_dict[item_name].split('#')[1]
        else:
            item_name_id_dict[item_name] = item_id + '#' + str(new_item_id)
            item_id = new_item_id
            new_item_id += 1

        # line_str = [str(i) for i in [user_id, timestamp, art_id, art_name, item_id, item_name]]
        # output_file.write('\t'.join(line_str) + '\n')
        output_file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (user_id, timestamp, art_id, art_name, item_id, item_name))
    input_file.close()
    output_file.close()
