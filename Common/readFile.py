'''
Created on Mar 11, 2014

@author: Administrator
'''
#read train file and store into train{user:{item:rating}}
from numpy import random
from numpy.ma import floor


def readFile2train(filename,Delimiter = '\t',hasTitle = False):
    train = dict()
    filer = open(filename,'r')
    if hasTitle:        #the first line is the title&invalid
        filer.readline()
    for eachLine in filer:  #read as str by default???
        (user,item,rating,timestamp) = eachLine.strip().split(Delimiter)
        train.setdefault(user,{})   #set dict[user] as dict{ }!!!
        train[user][item] = float(rating)
    filer.close()
    return train    #return train{user:{item:rating}}

#read LanguageAnalysis file and store into LanguageAnalysis{user:{item:rating}}
def readFile2test(filename,Delimiter = '\t'):
    test = dict()
    filer = open(filename,'r')
    for eachLine in filer:
        (user,item,rating,timestamp) = eachLine.strip().split(Delimiter)
        test.setdefault(user,{})
        test[user][item] = float(rating)
    filer.close()
    return test


#loadData for SVD
def loadData():
    return[ [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [1, 1, 1, 0, 0],
           [5, 5, 5, 0, 1],
           [1, 1, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1] ]
    
def loadSvdData(randomGenarate = False):
    if(randomGenarate):
        A = floor(random.rand(7,5)*10)#how to genarate sparse mat
    else:
        A = [[4, 4, 0, 2, 2 ],
            [4, 0, 0, 3, 3],
            [4, 0, 0, 1, 1],
            [1, 1, 1, 2, 0],
            [2, 2, 2, 0, 0],
            [1, 1, 1, 0, 0],
            [5, 5, 5, 0, 0] ]
    return A

def loadSvdData2():
    return[[2,0,0,4,4,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,5],
           [0,0,0,0,0,0,0,1,0,4,0],
           [3,3,4,0,3,0,0,2,2,0,0],
           [5,5,5,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,5,0,0,5,0],
           [4,0,4,0,0,0,0,0,0,0,5],
           [0,0,0,0,0,4,0,0,0,0,4],
           [0,0,0,0,0,0,5,0,0,5,0],
           [0,0,0,3,0,0,0,0,4,5,0],
           [1,1,2,1,1,2,1,0,4,5,0]]
    
