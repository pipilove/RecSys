'''
Created on Mar 26, 2014

@author: pipi
'''
from numpy import linalg as la, mat

from Common.readFile import loadData, loadSvdData, loadSvdData2
from SVD.Calculator import pearsSim, euclidSim, cosSim, svdEst, standEst
from SVD.svdRec import recommend


def test():    
    dataMat = mat(loadSvdData2())
    print 'dataMat:\n',dataMat,'\n'
    
    #print 'std - cosSim : ',recommend(dataMat,2,2,cosSim)  #euclidSim,pearsSim,cosSim
    #print 'std - euclidSim : ',recommend(dataMat,2,2,euclidSim)
    print 'std - pearsSim : \n',recommend(dataMat,user = 1,N = 2,simMeasure = pearsSim,estMethod = standEst)
    
    #svdEst(dataMat,user = 2,item = 2,simMeasure = pearsSim)
    print 'svd - pearson : \n', recommend(dataMat,user = 1,N = 2,simMeasure = pearsSim,estMethod = svdEst)
    
    
if __name__ == '__main__':
    test()   
    
    