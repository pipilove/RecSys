'''
Created on Mar 16, 2014

@author: pipi
'''
import math


#calculate the recall rating        
def recall(train,test,getRecommend,n = 10): #getRecommend from different CF method
    hit = 0
    allTest = 0
    for user in train.keys():
        tuItems = test[user]
        rank = getRecommend(user, train, n)
        for item,user in rank:
            if item in tuItems:
                hit += 1
        allTest += len(tuItems)
    return hit/(allTest*1.0)    #reduce float calculation
#calculate the precision rating
def precision(train,test,getRecommend,n = 10):
    hit = 0
    allRec = 0
    for user in train.keys():
        tuItems = test[user]
        rank = getRecommend(user,train,n)
        for item,user in rank:
            if item in tuItems:
                hit += 1
        allRec += n #<=>len(rank)
    return hit/(allRec*1.0)
#calculate the precision&recall rating simultaneously
def precisionRecall(train,test,getRecommend,n = 10):
    hit = 0
    allTest = 0
    allRec = 0
    for user,items in test.items():
        rank= getRecommend(user,train,n)
        rankDict = dict(rank)
        hit += len((rankDict.keys() & items.keys())) #for python3.3!!!
        allTest += len(items)
        allRec += n
    return [hit/(allTest*1.0),hit/(allRec*1.0)] #return list[recall,precision]

#calculate the coverage rating
def coverage(train,getRecommend,n = 10):
    allItems = set()
    recommendItems = set()
    for user,items in train.items():
        for item in items.keys():
            allItems.add(item)
        rank = getRecommend(user,train,n)
        for item,user in rank:
            recommendItems.add(item)
    return (len(recommendItems))/(len(allItems)*1.0)
        
#calculate the popularity rating
def popularity(train,getRecommend,n = 10):
    itemPopularity = dict()
    for user,items in train.items():
        for item in items.keys():
            itemPopularity.setdefault(item,0)
            itemPopularity[item] += 1
    ret = 0
    retLen = 0
    for user in train.keys():
        rank = getRecommend(user,train,n)
        for item,user in rank:
            ret += math.log(1+itemPopularity[item])
            retLen += 1
    return ret/(retLen*1.0)           
        
        
#print evaluating result
def printEvaluate(train,test,getRecommend):
    n = 10
    coveragerate = coverage(train,getRecommend,n)
    precisionRate = precision(train,test,getRecommend,n)
    recallRate = recall(train,test,getRecommend,n)
#     (precisionRate,recallRate) = precisionRecall(train,LanguageAnalysis,getRecommend)
    popularityRate = popularity(train,getRecommend,n)
    print('recall = ',recallRate)
    print('precision = ',precisionRate)
    print('coverage = ',coveragerate)
    print('popularity = ',popularityRate)  
    
    