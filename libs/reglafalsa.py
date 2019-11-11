import math
def same_sign(a, b):
    return a*b > 0


def reglaFalsa(func, low, high, n, tol):

    # Returns an error if the current interval has no root
    assert not same_sign(func(low), func(high)), 'Intervalo NO valido'


    if (func(low) == 0):
        print(high, "es Raiz")
        return high
    
    if (func(low) == 0):
        print(low, "es Raiz")
        return low

    
    cont = 1
    xm = high - (func(high) * (high - low)) / (func(high) - func(low))
    error = 1+tol
    print("|iter|       a      |      xm      |      b       |   f(Xm)  |     E   |")
    print ("| 1  |",str(low).ljust(12),"|","%.10f" % xm,"|","%.10f" % high,"|","%.1e" % func(xm),"|         |")
    while(cont < n and error > tol and func(xm) != 0):
        
        if not same_sign(func(xm), func(high)):
            low = xm
        else:
            high = xm
        xtemp = xm
        xm = high - ((func(high) * (high - low)) / (func(high) - func(low)))
        error = abs(xm-xtemp)
        cont += 1
        print ("|",str(cont).ljust(2),"|","%.10f" %low,"|","%.10f" % xm,"|","%.10f" % high,"|",str("%.1e" % func(xm)).ljust(8),"|","%.1e" % error, "|")
    if(func(xm) == 0):
        print(xm, 'es Raiz')
    else:
        if (error < tol):
            print(xm, "se aproxima a una raiz con tolerancia", tol)
        else:
            print("Fracaso en ", n, "iteraciones")
    
    return xm


def f(x):

    # funcion
    return math.log(math.sin(x)**2 + 1) - (1/2)




if __name__ == "__main__":
    Xi = 0
    Xs = 1
    tol = 1e-7
    n = 100

    x = reglaFalsa(f, Xi, Xs, n, tol)
    print(x, f(x))
