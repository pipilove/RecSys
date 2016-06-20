'''
Created on Mar 15, 2014

@author: pipi
'''
from RecSys.Common.Evaluator import printEvaluate
from RecSys.Common.readFile import readFile2train
from RecSys.Common.readFile import readFile2test
from RecSys.Common.writeFile import writeRecFile
from RecSys.USERCF.UserCFRec import getRecommend


def userCFTest():       
#get the train & LanguageAnalysis set
    train = readFile2train(r'E:\mechine_learning\datasets\ml-100k\u1.baseUserCF','\t',True)
    test = readFile2test(r'E:\mechine_learning\datasets\ml-100k\u1.testUserCF')    
#write recommend lists into file
    writeRecFile(train,getRecommend,r'E:\mechine_learning\datasets\uCF_recommend_list')
#print evaluating result 
    printEvaluate(train,test,getRecommend)
    
    
#UserCF
# recall =  0.10137306456324861
# precision =  0.46266666666666667
# coverage =  0.07592190889370933  
# popularity =  4.165121912130333

#UserCF-IIF
# recall =  0.10356412503651767
# precision =  0.4726666666666667
# coverage =  0.07809110629067245
# popularity =  4.156198387386623
    
    
         
if __name__ == '__main__':
    print('UserCFTest loading...')
    userCFTest()    
    print('UserCFTest ends!!!')
    
    