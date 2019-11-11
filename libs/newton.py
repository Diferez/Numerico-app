import math

def newton(f, df, x0, tol, n):

    error = tol + 1
    cont = 0
    print("|iter|      xi      |    f(x)  |     E   |")
    print ("| 0  |", "%.10f" %x0,"|", "%.1e" %f(x0),"|         |")
    while (error > tol and f(x0) != 0 and cont < n):

        x1 = x0 - f(x0)/df(x0)

        error = abs((x1-x0))
        x0 = x1
        cont += 1
        print ("|",str(cont).ljust(2),"|", "%.10f" %x0,"|", "%.1e" %f(x0),"|", "%.1e" %error,"|")

    if(f(x0) == 0):
        print(x0, 'es Raiz')
    else:
        if (error < tol):
            print(x0, "se aproxima a una raiz con tolerancia", tol)
        else:
            print("Fracaso en ", n, "iteraciones")
    return x0


def f(x):
    #funcion
    #rota = math.log(math.sin(x)**2 + 1) - (1/2)
    rota = math.exp(-(1/(x-1)**2))-(x/2)+0.6
    return rota

def df(x):
    #derivada
    return -1/2 + 2*math.exp(-1/(x-1)**2)/(x-1)**3

if __name__ == "__main__":
    n = 100
    tol = 1e-7
    x = newton(f, df, 1.2, tol, n)

