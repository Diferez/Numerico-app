from biseccion import biseccion
def f(x):

        # Here goes the function that we want
    return -26 + 85*x - 95 * x**2 + 44*x**3 + x**5

def bisec():

    Xi = 0
    Xs = 1
    tol = 1e-7
    n = 100
    x = biseccion(f, Xi, Xs, n, tol)
    print(x)

bisec()