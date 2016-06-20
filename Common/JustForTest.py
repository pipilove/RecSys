'''
Created on Mar 15, 2014

@author: pipi
'''
from numpy import mat, random ,linalg as la, zeros_like, diag

from Common.readFile import loadData


mymat = mat(loadData())
A = random.rand(3,5)
print A
U,S,V = la.svd(A)
print S
Sig = diag(S)
print Sig