import numpy as np
from sympy import *
def divi(x,y):
    n = len(x)
    b = np.zeros((n,n))
    b[0] = y
    b = b.transpose()
    print("----Matriz----")
    print(b)
    for j in range(1,n):
        for i in range(j,n):
            b[i,j] = (b[i,j-1]-b[i-1,j-1])/(x[i]-x[i-j])

    xt = 1
    yi = b[0,0]
    print("----Matriz Diferencias----")
    print(b)
    p = str(b[0,0])
    xx = x*-1
    for j in range(1,j):
        signo = ''
        if (b[j,j]>=0):
            signo = '+'
        xt = ''
        for i in range(0,j):
            signo2 = ''
            if (xx[i]>=0):
                signo2 = '+'
            
            xt = xt + '*(x'+signo2+str(xx[i])+')'

        p = p+signo+str(b[j,j])+xt
    
    print("Newton Polinomio =",p)
    s = simplify(p)

    print("Newton Polinomio simplificado =",p)
    print("Evaluacion =",p)
    return b,p,s

def diferenciasdiv(x,y):
    n = len(x)
    b = np.zeros((n,n))
    b[0] = y
    b = b.transpose()
    print("----Matriz----")
    print(b)
    for j in range(1,n):
        for i in range(j,n):
            b[i,j] = (b[i,j-1]-b[i-1,j-1])/(x[i]-x[i-j])

    xt = 1
    yi = b[0,0]
    print(b)
    return b

if __name__ == "__main__":
    vectorx = np.array([-1,0,3,4])
    vectory = np.array([15.5,3,8,1])

    #newton(vectorx,vectory)
    diferenciasdiv(vectorx,vectory)
