'''
Created on Mar 16, 2014

@author: Administrator
'''
from operator import itemgetter

from ItemCF.Calculator import itemSimilarity


def recommend(train,user,W,k = 10):#item j similar to k = 10(optimal) items
    rank = dict()
    nu = train[user]    #all items that user likes
    for i,rui in nu.items():
        for j,wj in sorted(W[i].items(),key = itemgetter(1),reverse = True)[0:k]:
            if j in nu.keys():
                continue
            rank.setdefault(j,0)
            rank[j] += wj*rui
    return rank #return rank{item : rank rate}
        
def getRecommend(user,train,n = 10,k = 10):    
    W = itemSimilarity(train)    
    rank = recommend(train,user,W,k)
    topN = sorted(rank.items(),key = itemgetter(1),reverse = True)[0:n]
    return topN #topN[(item,rank rate),...]

