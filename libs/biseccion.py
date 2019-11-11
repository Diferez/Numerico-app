import math

def same_sign(a, b):
    return a*b < 0


def biseccion(func, low, high, n, tol):

    # Returns an error if the current interval has no root ##f(a)∗f(b) < 0 teorema raiz
    assert same_sign(func(low), func(high)), 'Intervalo NO valido'
    if (func(high) == 0):
        print(high, "es Raiz")
        return high

    xm = (low + high)/2.0
    cont = 1
    error = tol + 1
    ret = []
    print("|iter|       a      |      xm      |      b       |   f(Xm)  |     E   |")
    print("| 1  |","%.10f" % low,"|", "%.10f" % xm,"|", "%.10f" % high,"|", "%.1e" % func(xm),"|         |")
    ret.append([cont,"%.10f" % low,"%.10f" % xm, "%.10f" % high,str("%.1e" % func(xm)),""])

    while(cont < n and error > tol and func(xm) != 0):

        if (same_sign(func(xm), func(high))):
            low = xm
        else:
            high = xm

        xtemp = xm
        xm = (low + high)/2.0
        error = abs(xm-xtemp)
        cont += 1
        #ret.append([cont,low,xm,high,func(xm),error])
        ret.append([cont,"%.10f" % low,"%.10f" % xm, "%.10f" % high,str("%.1e" % func(xm)),"%.1e" % error])
        print("|",str(cont).ljust(2),"|","%.10f" % low,"|", "%.10f" % xm,"|", "%.10f" % high,"|", str("%.1e" % func(xm)).ljust(8),"|", "%.1e" % error,"|")
    if(func(xm) == 0):
        print(xm, 'es Raiz')
    else:
        if (error < tol):
            print(xm, "se aproxima a una raiz con tolerancia", tol)
        else:
            print("Fracaso en ", n, "iteraciones")
    return xm, ret


def f(x):
    return x**2-x+1.25-math.exp(x)
        # Here goes the function that we want
    #return math.log((math.sin(x)**2) + 1) - (1/2) x**2-x+1.25-E**x


if __name__ == "__main__":
    Xi = 0
    Xs = 1
    tol = 1e-7
    n = 100
    x = biseccion(f, Xi, Xs, n, tol)
    
