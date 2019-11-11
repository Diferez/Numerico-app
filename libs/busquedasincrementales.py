import math
def same_sign(a, b):
    return a*b > 0


def busquedasincrementales(f, x0, delta, n):

    #assert not same_sign(f(value), f(xnew))

    if (f(x0) == 0):
        print(x0, "es Raiz")
        return x0

    x1 = x0 + delta
    cont = 0
    while ( cont < n):
        x0 = x1
        x1 = x0 + delta
        if not(same_sign(f(x0),f(x1))) :
            print("Hay una raiz de f en [" , x0, x1 , "]")
        cont += 1
    
    if(f(x1) == 0):
        print(x0, 'es Raiz')
    else:
        if (same_sign(f(x0),f(x1))):
            #print("Hay una Raiz entre", x0,"y", x1)
            pass
        else:
            print("Fracaso en ", n, "iteraciones")

    return x0


def f(x):
    return math.exp(-(1/(x-1)**2))-(x/2)+0.6
    # return function


if __name__ == "__main__":
    x0 = 0
    delta = 0.3
    n = 100
    x = busquedasincrementales(f, x0, delta, n)
    #print(x, f(x))
