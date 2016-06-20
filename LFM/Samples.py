'''
Created on Mar 19, 2014

@author: pipi
'''
import random


#positive&negative sample selection
def randomSelectSamples(items,itemsPool,ratio = 10):    #for one user
    negLen = len(items)*ratio   #length of negative samples
    ret = dict()
    for i in items.keys():
        ret[i] = 1      #select positive samples
    
    n = 0
    for i in range(len(items)*3):
        item = itemsPool[random.randint(0,len(itemsPool)-1)]#???
        if item in ret:
            continue
        ret[item] = 0   #select negative samples
        n += 1
        if n >= negLen:
            break
    return ret      #dict {item:1}
        
#initial P&Q
def initModel(userItems,F):
    pass
    
#predict rui
def predict(user,item):
    pass        