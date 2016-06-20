#coding=gbk
'''
Created on Mar 22, 2014

@author: pipi
'''
from numpy import nonzero
from SVD.Calculator import pearsSim, standEst


#recommend topN
def recommend(dataMat,user,N = 3,simMeasure = pearsSim,estMethod = standEst):
    unRatedItems = nonzero(dataMat[user,:].A == 0)[1]
    if len(unRatedItems) == 0:
        return 'you rated everything ... '
    itemScore = list()
    
    for item in unRatedItems:
        estimatedScore = estMethod(dataMat,user,item,simMeasure)
#         print '(item,estimatedScore):',(item,estimatedScore)
        itemScore.append( (item,estimatedScore) )
    
    topN = sorted(itemScore,key = lambda jj:jj[1],reverse = True)[:N]
    return topN
    
