import numpy as np
import math
import sympy as sp

def trazaLinea(x,y):
    n = (len(x)*2)
    m = math.ceil(n-(len(x)/2))
    
    a = np.zeros((m,n-2))
    k = len(x)
    i=0
    j=1

    while j >= 0:
        a[0,i] = (x[0]**j)
        j-=1
        i+=1
    i=0
    j=1
    for l in range(1,k):
        while j >= 0:
            a[l,i] = (x[l]**j)
            j-=1
            i+=1
            p=l
        j=1
    i=0
    j=1
    u=0
    for p in range(k,m):
        if p == k:
            while j >= 0:
                a[p,i] = a[u+1,i]
                a[p,i+2] = -a[u+1,i]
                j-=1
                i+=1

            j=1
            u+=2
        else:
            while j >= 0:
                a[p,i] = a[u,i+(u-2)]
                a[p,i+2] = -a[u,i+(u-2)]
                j-=1
                i+=1
            j=1
            u+=2
        
    print(a)
    
    trazalineal(x, y, a)

def trazalineal(xi,fi,M):
    n = len(xi)
    x = sp.Symbol('x')
    polinomio = []
    tramo=1
    while not(tramo>=n):
        m =(fi[tramo]-fi[tramo-1])/(xi[tramo]-xi[tramo-1])
        inicio = fi[tramo-1]-m*xi[tramo-1]
        ptramo = inicio + m*x
        polinomio.append(ptramo)
        tramo = tramo + 1
    print('Polinomios por tramos: ')
    for tramo in range(1,n,1):
        print(' x = ['+str(xi[tramo-1])
             +','+str(xi[tramo])+']')
        print(str(polinomio[tramo-1]))
    
    return M, polinomio
    
if __name__ == "__main__":
    vectorx = np.array([-1,0,3,4])
    vectory = np.array([15.5,3,8,1])
    
    trazaLinea(vectorx,vectory)