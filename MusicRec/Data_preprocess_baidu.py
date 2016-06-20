#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '3/9/2015-009'
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
from os import listdir
from os.path import join
import re


def get_music_ids(DIR):
    '''
    找到包含所有音乐名的集合
    :param DIR:
    :return:
    '''
    filenames = listdir(DIR)
    # print(filenames)
    music_ids = set()
    for filename in filenames:
        music_ids = music_ids.union(set([line.strip() for line in open(join(DIR, filename))]))
    # print(music_ids.__len__())  #4w
    return music_ids


def get_music_tag(DIR):
    '''
    从DIT中找到每个music所有对应的tags，并写入文件music_tag_filename中
    :param music_tag_filename:
    :return:
    '''
    filenames = listdir(DIR)
    music_tag = dict()
    for music_id in get_music_ids(DIR):
        music_tag.setdefault(music_id, [])
        for filename in filenames:
            if music_id in [line.strip() for line in open(join(DIR, filename))]:
                music_tag[music_id].append(filename.split('.')[0])
    return music_tag
    # print(list(music_tag.keys()).__len__())   #4w+


def write_music_tag(music_tag, music_tag_filename):
    '''
    将music_tag每个music_id:tags写入文件music_tag_filename中
    :param music_tag:
    :param music_tag_filename:
    :return:
    '''
    music_tag_file = open(music_tag_filename, 'w')
    for music_id in music_tag.keys():
        tags = re.sub("\[|\]|\s*'", '', str(music_tag[music_id]))  # list中,后面是有空格的
        # print(tags)
        music_tag_file.write("%s:%s\n" % (music_id, tags))
    music_tag_file.close()


def load_music_tag(music_tag_filename):
    '''
    从文件music_tag_filename中载入music_name和其相应的tags
    :param music_tag_filename:
    :return:
    '''
    music_tag_file = open(music_tag_filename)
    music_tag = dict()
    for line in music_tag_file:
        music_id = line.split(':')[0]
        music_tag.setdefault(music_id, [])
        music_tag[music_id] = line.strip().split(':')[1].split(',')
        # print(music_tag[music_id])
    return music_tag


def get_all_tags(music_tag):
    '''
    返回music的所有tags的集合
    :param music_tag:
    :return:
    '''
    all_tags = set()
    for tags in music_tag.values():
        all_tags.update(tags)
    # print(all_tags.__len__()) #106
    return list(all_tags)


def add_music_tag(lrc_filename_dir, all_tags, music_tag):
    '''
    从歌词lrc中挖掘music对应的tags
    :return:
    '''
    lrc_filenames = [join(lrc_filename_dir, lrc_filename) for lrc_filename in listdir(lrc_filename_dir)]
    # print(lrc_filenames)
    for lrc_filename in lrc_filenames:
        music_id = lrc_filename.split('\\')[-1].split('.')[0]
        for tag in all_tags:
            if tag in open(lrc_filename, encoding='UTF-8', errors='ignore').readlines() and not tag in music_tag[
                music_id]:
                music_tag[music_id].append(tag)
    print(music_tag)
    return music_tag


def write_tag_name(TAG_DIR, TAG_FILENAME='./tag_names.txt'):
    '''
    读取所有tag的名字，并写入文件中
    :param TAG_DIR:
    :param TAG_FILENAME:
    :return:
    '''
    tag_names = [tag.split('.')[0] for tag in listdir(TAG_DIR)]
    tag_file = open(TAG_FILENAME, 'w')
    for tag_name in tag_names:
        tag_file.write(tag_name + ' ')
    tag_file.close()


if __name__ == '__main__':
    TAG_DIR = 'E:\machine_learning\datasets\百度音乐集\\tag'
    music_tag_filename = 'E:\machine_learning\datasets\百度音乐集\music_tag.txt'
    # TAG_DIR = 'E:\machine_learning\datasets\百度音乐集\\tag_test'
    # music_tag_file_name = 'E:\machine_learning\datasets\百度音乐集\music_tag1.txt'

    # music_tag = get_music_tag(TAG_DIR)
    # write_music_tag(music_tag, music_tag_filename)

    music_tag = load_music_tag(music_tag_filename)
    all_tags = get_all_tags(music_tag)
    lrc_filename_dir = 'E:\machine_learning\datasets\百度音乐集\lrc'
    # add_music_tag(lrc_filename_dir, all_tags, music_tag)


    # music_ids = get_music_ids(TAG_DIR)

