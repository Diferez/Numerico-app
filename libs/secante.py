import math


def Secante(x0, x1, tol, n, f):


    if (f(x0) == 0):
        print(x0, "es Raiz")
        return x0
    
    i = 2
    error = tol+1
    print("|iter|      xi      |      f(x)     |     E   |")
    print ("| 0  |",  "%.10f" %x0,"|", str("%.1e" %f(x0)).ljust(13),"|         |")
    print ("| 1  |", "%.10f" % x1,"|",str("%.1e" %f(x1)).ljust(13),"|         |")
    while (error>tol and f(x0) != 0 and i < n and f(x1)!=0):

        x = x1 - ((x1 - x0) * f(x1) / (f(x1) - f(x0)))
        


        
        x0 = x1  # redefine x0
        x1 = x  # redefine x1
        error = abs((x1 - x0))
        print ("|",str(i).ljust(2),"|", "%.10f" % x,"|", str("%.1e" %f(x)).ljust(13),"|", "%.1e" % error,"|")
        i = i + 1

    if(f(x0) == 0):
        print(x0, 'es Raiz')
    else:
        if (error < tol):
            print(x0, "se aproxima a una raiz con tolerancia", tol)
        else:
            print("Fracaso en ", n, "iteraciones")


#f = lambda x: x ** 3 + 4 * x ** 2 - 10
def f(x):
    #funcion
    return x**2-x+1.25-math.exp(x)
    #return math.log(math.sin(x)**2 + 1) - (1/2)


if __name__ == "__main__":
    x0 = 0.5
    x1 = 1
    n= 100
    tol= 1e-7
    x = Secante(x0, x1, tol, n, f)
