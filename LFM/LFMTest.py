'''
Created on Mar 21, 2014

@author: pipi
'''
import os
from Common.readFile import readFile2train, readFile2test
from LFM.LFMRec import latentFactorModel, getRecommend


def write(train,P,Q,itemsPool):    
    userRecItems = dict()
    file = open(r'E:\datamining\mechine_learning\datasets\recommend_list','w')
    for user in train.keys():
        topN = getRecommend(user,P,Q,n = 10)
        userRecItems[user] = dict(topN).keys()
        file.write('%s%s' % (user,'\t'))
        for i in userRecItems[user]:
            file.write('%s,' % i)
        file.write('%s' % '\n')#os.linesep)
    file.close()
        
def LFMtest():
    train = readFile2train(r'E:\datamining\mechine_learning\datasets\ml-100k\u1.baseUserCF')
#     train = readFile2train(r'E:\datamining\RecSys\ml-100k\ua.base.txt')
    test = readFile2test(r'E:\datamining\mechine_learning\datasets\ml-100k\u1.testUserCF')
    
    #build itemsPool
    itemsPool = list()
    for user,items in train.items():
        for item in items.keys():
            itemsPool.append(item)
            
    #write LFMTest result    
    (P,Q) = latentFactorModel(train,itemsPool,  N = 100 ,   F = 100,alpha = 0.02 ,regular = 0.01,ratio = 10)
    write(train,P,Q,itemsPool)


if __name__ == '__main__':
    print('LFMtest loading...')
    LFMtest()
    print('LFMtest ends...')
    