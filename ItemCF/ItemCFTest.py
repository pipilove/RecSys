'''
Created on Mar 16, 2014

@author: Administrator
'''
from Common.Evaluator import printEvaluate
from Common.readFile import readFile2train, readFile2test
from Common.writeFile import writeRecFile
from ItemCF.ItemCFRec import getRecommend


def itemCFTest():       
#get the train & LanguageAnalysis set
    train = readFile2train(r'E:\mechine_learning\datasets\ml-100k\u1.baseItemCF','\t',True)
    test = readFile2test(r'E:\mechine_learning\datasets\ml-100k\u1.testItemCF')
#write recommend lists into file
    writeRecFile(train,getRecommend)   
#print evaluating result 
    printEvaluate(train,test,getRecommend)  
    
    
#ItemCF
# recall =  0.07668711656441718
# precision =  0.35
# coverage =  0.2725958062183659
# popularity =  3.5859398523449504

#ItemCF-IUF
# recall =  0.09056383289512124
# precision =  0.41333333333333333
# coverage =  0.210412147505423
# popularity =  3.840520846963231
    
#ItemCF-Norm
# recall =  0.07449605609114812
# precision =  0.34
# coverage =  0.21402747650036152
# popularity =  3.686392581067494
    
    
    
if __name__ == '__main__':
    print('ItemCFTest loading...')
    itemCFTest()    
    print('ItemCFTest ends!!!')
             
                
        