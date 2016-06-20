'''
Created on Mar 25, 2014

@author: pipi
'''
import os


#write recommend list into file
def writeRecFile(train,getRecommend,filename = r'E:\mechine_learning\datasets\recommend_list'):
    userRecItems = dict()
    n = 10
    filew = open(filename,'w')
    for user in train.keys():
        rank = getRecommend(user, train, n)
        userRecItems[user] = dict(rank).keys()
        filew.write('%s%s' % (user,'\t'))
        for i in userRecItems[user]:
            filew.write('%s,' % i)
        filew.write('%s' % '\n')#os.linesep)
    filew.close()
    
    