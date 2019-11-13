import numpy as np
import math
import sympy as sym

def trazaCubo(x):
    n = (len(x)*3)    
    a = np.zeros((n,n))
    k = len(x)
    i=0
    j=3
    
    while j >= 0:
        a[0,i] = (x[0]**j)
        j-=1
        i+=1
    i=0
    j=3
    for l in range(1,k):
        while j >= 0:
            a[l,i] = (x[l]**j)
            j-=1
            i+=1
            p=l
        j=3
    i=0
    j=3
    u=0
    for p in range(k,n-6):
        if p == k:
            while j >= 0:
                a[p,i] = a[u+1,i]
                a[p,i+3] = -a[u+1,i]
                j-=1
                i+=1

            j=3
            u+=2            
        else:
            while j >= 0:
                a[p,i] = a[u,i]
                a[p,i+3] = -a[u,i]
                j-=1
                i+=1
            j=3
            u+=2
    i=0
    u=0
    for p in range(6,n-4):
        if p == 6:
            while j >= 0:
                a[p,i] = j*a[u+1,i+1]
                a[p,i+4] = -j*a[u+1,i+1]
                j-=1
                i+=1
            j=3
            u+=2
        else:
            while j >= 0:
                a[p,i] = j*a[u,i+1]
                a[p,i+4] = -j*a[u,i+1]
                j-=1
                i+=1
            j=3
            u+=2
    i=0
    u=0
    for p in range(8,n-2):
        if p == 8:
            while j >= 0:
                a[p,i] = (j*(j-1))*a[u+1,i+2]
                a[p,i+4] = -(j*(j-1))*a[u+1,i+2]
                j-=1
                i+=1
            j=3
            u+=2
        else:
            while j >= 0:
                a[p,i] = (j*(j-1))*a[u,i+2]
                a[p,i+4] = -(j*(j-1))*a[u,i+2]
                j-=1
                i+=1
            j=3
            u+=2
    i=0
    u=0
    for p in range(10,n):
        if p == 10:
            while j >= 0:
                a[p,i] = (j*(j-1))*a[u+1,i+3]
                j-=1
                i+=1
            j=3
            u+=2
        else:
            while j >= 0:
                a[p,i] = (j*(j-1))*a[u,i+3]
                j-=1
                i+=1
            j=3
            u+=2
    print(a)
    
def trazacubica(xi,yi):
    n = len(xi)
    
    # Valores h
    h = np.zeros(n-1, dtype = float)
    for j in range(0,n-1,1):
        h[j] = xi[j+1] - xi[j]
    
    # Sistema de ecuaciones
    A = np.zeros(shape=(n-2,n-2), dtype = float)
    B = np.zeros(n-2, dtype = float)
    S = np.zeros(n, dtype = float)
    A[0,0] = 2*(h[0]+h[1])
    A[0,1] = h[1]
    B[0] = 6*((yi[2]-yi[1])/h[1] - (yi[1]-yi[0])/h[0])
    for i in range(1,n-3,1):
        A[i,i-1] = h[i]
        A[i,i] = 2*(h[i]+h[i+1])
        A[i,i+1] = h[i+1]
        B[i] = 6*((yi[i+2]-yi[i+1])/h[i+1] - (yi[i+1]-yi[i])/h[i])
    A[n-3,n-4] = h[n-3]
    A[n-3,n-3] = 2*(h[n-3]+h[n-2])
    B[n-3] = 6*((yi[n-1]-yi[n-2])/h[n-2] - (yi[n-2]-yi[n-3])/h[n-3])
    
    # Resolver sistema de ecuaciones
    r = np.linalg.solve(A,B)
    # S
    for j in range(1,n-1,1):
        S[j] = r[j-1]
    S[0] = 0
    S[n-1] = 0
    
    # Coeficientes
    a = np.zeros(n-1, dtype = float)
    b = np.zeros(n-1, dtype = float)
    c = np.zeros(n-1, dtype = float)
    d = np.zeros(n-1, dtype = float)
    for j in range(0,n-1,1):
        a[j] = (S[j+1]-S[j])/(6*h[j])
        b[j] = S[j]/2
        c[j] = (yi[j+1]-yi[j])/h[j] - (2*h[j]*S[j]+h[j]*S[j+1])/6
        d[j] = yi[j]
    
    # Polinomio trazador
    x = sym.Symbol('x')
    polinomio = []
    for j in range(0,n-1,1):
        ptramo = a[j]*(x-xi[j])**3 + b[j]*(x-xi[j])**2 + c[j]*(x-xi[j])+ d[j]
        ptramo = ptramo.expand()
        polinomio.append(ptramo)
    
    print('Polinomios por tramos: ')
    for tramo in range(1,n,1):
        print(' x = ['+str(xi[tramo-1])+','+str(xi[tramo])+']')
        print(str(polinomio[tramo-1]))


if __name__ == "__main__":
    vectorx = np.array([-1,0,1,2])
    vectory = np.array([1,0,-1,4])
    
    trazaCubo(vectorx)
    trazacubica(vectorx,vectory)