# coding=gbk
'''
Created on Mar 15, 2014

@author: Administrator
'''
import math

#calculate user similarity
def userSimilarity(train): 
    # build inverse table for item_users
    itemUsers = dict()
    for user, items in train.items():
        for i in items.keys():
            if i not in itemUsers:  # 《=》 .keys():
                itemUsers[i] = set()  #!!!
            itemUsers[i].add(user)
    # calculate co-rated between users
    N = dict()
    C = dict()
    for items, users in itemUsers.items():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1
            for v in users:
                C.setdefault(u, {})
                C[u].setdefault(v, 0)
                if u == v:
                    continue
                C[u][v] += 1/math.log(1+len(users)) #UserCF-IIF惩罚了用户u和用户v共同兴趣列表中热门物品的影响
    # calculate final similarity matrix w
    W = dict()
    for u, relatedUsers in C.items():
        W.setdefault(u, {})
        for v, cuv in relatedUsers.items():
            if u == v:
                continue
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
#     for u in train.keys():
#         for v in train.keys():
#             W[u][v] = C[u][v]/math.sqrt(N[u]*N[v])#c,v not related make key error
    return W

