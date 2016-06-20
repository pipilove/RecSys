'''
Created on Mar 20, 2014

@author: pipi
'''
from operator import itemgetter
from LFM.Samples import initModel, randomSelectSamples, predict


#build latent factor model(calculate the P&Q)
#                      train   ,itemsPool,iterate steps,factors,learning rate,    lambda    ,negsamples/possamples
def latentFactorModel(userItems,itemsPool,    N     ,   F = 100,alpha = 0.02 ,regular = 0.01,ratio = 10):
    [P,Q] = initModel(userItems,F)  #???
    for steps in range(N):
        for user,items in userItems.items():
            samples = randomSelectSamples(items,itemsPool,ratio)#select the p&q samples for each user
            for item,rui in samples.items():
                eui = rui - predict(user,item)  #???
                for f in range(F):
                    P[user][f] += alpha*(eui*Q[f][item] - regular*P[user][f])
                    Q[f][item] += alpha*(eui*P[user][f] - regular*Q[f][item])
        alpha *= 0.9
    return (P,Q)
                
#all recommendations for one user        
def recommend(user,P,Q):
    rank = dict()
    for f,puf in P[user].items():
        for item,qif in Q[f].items():
            rank[item].setdefault(0)
            rank[item] += puf*qif
    return rank #rank{item,rui}
            
def getRecommend(user,P,Q,n = 10):  # n = recommend numbers
    rank = recommend(user,P,Q)
    topN = sorted(rank.items(),key = itemgetter(1),reverse = True)[0:n]     
    return topN       #topN(item,rui)

    