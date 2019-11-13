import cmath
import math
import os
import sys

# Not working with some functions


def puntofijo(f, g, x, tol, n):

    error = tol+1
    i = 1
    xn = x
    lista = []
    print("|iter|      xi       |    g(xi)      |  f(xi)   |     E   |")
    print ("| 0  |" ,"%.10f" % xn,"|", "%.10f" %g(xn),"|", str("%.1e" %f(xn)).ljust(8),"|         |")
    lista.append([0,"%.10f" % xn, "%.10f" %g(xn),"%.1e" %f(xn),""])
    while (f(xn)!=0 and i < n and error > tol):
        temp = xn
        xn = g(xn)
        error = abs((temp - xn))
        #print("%d\t\t%.4f\t\t%.4f" % (i, xn, error))
        print ("|",str(i).ljust(2) ,"|", "%.10f" %xn,"|", "%.10f" %g(xn),"|",str("%.1e" %f(xn)).ljust(8),"|", "%.1e" %error,"|")
        lista.append([i,"%.10f" % xn, "%.10f" %g(xn),"%.1e" %f(xn),"%.1e" %error])
        i += 1

    if(f(xn) == 0):
        print(xn, 'es Raiz')
    else:
        if (error < tol):
            print(xn, "se aproxima a una raiz con tolerancia", tol)
        else:
            print("Fracaso en ", n, "iteraciones")
    return xn, lista



def f(x):

    # Here goes the function we will use
    return x**2-x+1.25-math.exp(x)
    #return math.log(math.sin(x)**2 + 1) - (1/2) - x
    

def g(x):
    #funcion secundaria
    return math.log(x**2-x+1.25)


if __name__ == "__main__":
    x = 0.5
    tol = 1e-7
    n = 100
    puntofijo(f, g, x, tol, n)

