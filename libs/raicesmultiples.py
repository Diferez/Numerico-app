import math

def RaizM(f, df1, df2, x0, tol, n):

    error = tol + 1
    cont = 0
    lista=[]
    while ( f(x0) != 0 and cont < n):

        x1 = x0 - ((f(x0)*df1(x0))/((df1(x0)**2)-f(x0)*df2(x0)))
        error = abs((x1-x0))
        x0 = x1
        cont += 1
        lista.append([cont, x0, f(x0), df1(x0), df2(x0), error])

    if(f(x0) == 0):
        print(x0, 'es Raiz')
    else:
        if (error < tol):
            print(x0, "se aproxima a una raiz con tolerancia", tol)
        else:
            print("Fracaso en ", n, "iteraciones")
    return x0, lista


def f(x):
    #funcion
    return math.exp(-(1/(x-1)**2))-(x/2)+0.6


def df1(x):
    #primera derivada
    return math.exp(-(1/(x-1)**2))-(1/2)


def df2(x):
    #segunda derivada
    return math.exp(-(1/(x-1)**2))


if __name__ == "__main__":
    n = 100
    tol = 1e-7
    x = RaizM(f, df1, df2, 0, tol, n)



