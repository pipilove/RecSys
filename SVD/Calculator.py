#coding=gbk
'''
Created on Mar 23, 2014

@author: pipi
'''
from numpy import linalg as la, corrcoef, shape, nonzero, logical_and, diag, mat


#A&B are all column vectors
#Euclidean  distance
def euclidSim(A,B):
    return 1.0/(1.0+la.norm(A-B))

#pearson correlation coefficient
def pearsSim(A,B):
    if len(A) < 3:
        return 1.0
    return 0.5+ 0.5*corrcoef(A,B,rowvar = 0)[0][1]

#cosine similarity
def cosSim(A,B):
    num = float(A.T*B)
    denum = la.norm(A)*la.norm(B)
    return 0.5 + 0.5*(num/denum)
    

#calculate ItemBased estimatedScore of (user,item)
def standEst(dataMat , user , item ,simMeasure ):
    n = shape(dataMat)[1]   #num of items
    simTotal = 0.0
    ratSimTotal = 0.0
    
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0:
            continue
        overlap = nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
        if len(overlap) == 0:
            similarity = 0
        else:
            similarity = simMeasure(dataMat[overlap,item],dataMat[overlap,j])
        simTotal += similarity
        ratSimTotal += similarity*userRating
    
    if simTotal == 0.0:
        return 0.0
    return ratSimTotal/simTotal #归一化,float    

#calculate index of 90% sigma**2 
def calSigma(Sigma):
    sigma2 = Sigma**2
    sumSigma2 = sum(sigma2)*0.9   #计算总能量的90%
    sumValid = 0.0
    validD = 0
    while(sumValid < sumSigma2):
        sumValid += sigma2[validD]
        validD += 1
    return validD+1

#calculate svdBased&ItemBased estimatedScore of (user,item)
def svdEst(dataMat,user,item,simMeasure):
    n = shape(dataMat)[1]   #num of items
    simTotal = 0.0
    ratSimTotal = 0.0
    (U,Sigma,VT) = la.svd(dataMat)
    validD = calSigma(Sigma)
    SigmaD = mat(diag(Sigma[:validD]))#mat(eye(validD)*Sigma[:validD])
#     print '\nvalidD = ',validD
#     print 'dataMat.T\n',dataMat.T,'\nU[:,:validD]\n',U[:,:validD],'\nSigmaD.I\n',SigmaD.I
    xformedItems = dataMat.T * U[:,:validD] * SigmaD.I  #???构建转换后的物品[item-item]
#     print U[:,:validD] * SigmaD * VT[:validD,:]
#     print 'xformedItems :\n ',xformedItems
    for j in range(n):#improve:calculate not 0 first???
        userRating = dataMat[user,j]
        if userRating == 0 | j == item:
            continue
        similarity = simMeasure(xformedItems[item,:].T,xformedItems[j,:].T)
        print 'similarity: %d - %d  = %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity*userRating
    if simTotal == 0:
        return 0.0
    print 'item %d simTotal = %f,ratSimTotal = %f,ratSimTotal/simTotal = %f' \
            % (item,simTotal,ratSimTotal,ratSimTotal/simTotal)
    #Extreme case:user rate only 1 item,return is always userrating 
    return ratSimTotal/simTotal
    
