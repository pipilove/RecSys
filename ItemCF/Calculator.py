# coding=gbk
'''
Created on Mar 16, 2014

@author: Administrator
'''
import math


def itemSimilarity(train):
    #calculate co-rated users between items
    C = dict()
    N = dict()
    for user,items in train.items():
        for i in items.keys():
            C.setdefault(i,{})
            N.setdefault(i,0)
            N[i] += 1
            for j in items.keys():
                if i == j:
                    continue
                C[i].setdefault(j,0)
                C[i][j] += 1/(math.log(1+len(items))*1.0)#ItemCF-IUF no of users who like i & j 
    #calculate final similarity matrix W
    W = dict()
    for i,relatedItems in C.items():
        W.setdefault(i,{})
        for j,cij in relatedItems.items():
            W[i].setdefault(j,0)
            W[i][j] += cij/math.sqrt(N[i]*N[j])
    #Normalization 归一化    !!!     ItemCF-Norm
#     for i,items in W.items(): 
#         for j in items.keys():
#             W[i][j] /= max(items.values())    #<=>!!!
    for i,items in W.items():
        items = {j:wij/max(items.values()) for j,wij in items.items()}
    return W    #return W{itemi:{itemj : wij}}

