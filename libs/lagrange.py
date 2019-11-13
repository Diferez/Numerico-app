import numpy as np
from sympy import *

def lagrange(x,y,g):
    temp = ""

    for i in range(0,g):
        temp = temp+'('
        for j in range(0,g):
            if(j!=i):
                temp = temp +'(x-('+str(x[j])+'))*'
        temp = temp[:-1]
        temp =temp+')/('
        for j in range(0,g):
            if(j!=i):
                temp = temp +'('+str(x[i])+'-('+str(x[j])+'))*'
        temp = temp[:-1]
        
        temp = temp +')*('+str(y[i])+')+'
     
        
    temp=temp[:-1]
    
    print("lagrange: ",temp)
    
    p = simplify(temp)
    print("lagrange: ",p)
    # a = input("Desea evaluarlo? (s/n)")
    # if (a == 's'):
    #     inp = float(input("Ingrese el numero en el que lo desee evaluar"))
    #     xs = Symbol('x')
    #     p = p.evalf(subs={xs:inp})
    
    return temp, p


    print("Evaluacion =",p)

if __name__ == "__main__":
    vectorx = np.array([-1,0,3,4])
    vectory = np.array([15.5,3,8,1])

    lagrange(vectorx,vectory, 2)