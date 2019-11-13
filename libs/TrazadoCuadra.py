import numpy as np
import math
from sympy import *

def trazaCuadra(x):
    n = (len(x)*2)    
    a = np.zeros((n,n+1))
    k = len(x)
    i=0
    j=2

    while j >= 0:
        a[0,i] = (x[0]**j)
        j-=1
        i+=1
    i=0
    j=2
    for l in range(1,k):
        while j >= 0:
            a[l,i] = (x[l]**j)
            j-=1
            i+=1
            p=l
        j=2
    i=0
    j=2
    u=0
    for p in range(k,n-2):
        if p == k:
            while j >= 0:
                a[p,i] = a[u+1,i]
                a[p,i+3] = -a[u+1,i]
                j-=1
                i+=1

            j=2
            u+=2            
        else:
            while j >= 0:
                a[p,i] = a[u,i]
                a[p,i+3] = -a[u,i]
                j-=1
                i+=1
            j=2
            u+=2
    i=0
    u=0
    print(p)
    for p in range(6,8):
        if p == 6:
            while j >= 0:
                a[p,i] = j*a[u+1,i+1]
                a[p,i+3] = -j*a[u+1,i+1]
                j-=1
                i+=1
            j=2
            u+=2
        else:
            while j >= 0:
                a[p,i] = j*a[u,i+1]
                a[p,i+3] = -j*a[u,i+1]
                j-=1
                i+=1
            j=2
            u+=2
    print(a)
    polito=[]

    return a, polito

    
if __name__ == "__main__":
    vectorx = np.array([-1,1,3,4])
    vectory = np.array([15.5,3,8,1])
    
    trazaCuadra(vectorx)