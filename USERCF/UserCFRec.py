# coding=gbk
'''
Created on Mar 12, 2014
 
@author: Administrator
'''
from operator import itemgetter
from USERCF.Calculator import userSimilarity


# UserCF recommendation
def recommend(user, W, train,k = 80):
    rank = dict()
    interactedItems = train[user]
    for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:k]:
            for i, rvi in train[v].items():  # rui = 1.0
                if i in interactedItems:
                    continue
                if i not in rank.keys():
                    rank.setdefault(i,0)
                rank[i] += wuv * rvi
    #print('type(rank) is ',type(rank))
    return rank     #return a dict(item:wuv)

#get the recommend table
def getRecommend(user,train,n = 10,k = 80): #k the no of recommend items
    W = userSimilarity(train)
    rank = recommend(user,W,train,k)
    topN = sorted(rank.items(),key = itemgetter(1),reverse = True)[0:n]
    #print('type(topN) is ',type(topN))
    return topN #return a tuple list[(item,user)...]
#     topN = dict(topN)
#     return topN #return a dict[item:user,...]

