import numpy as np
def main():
    # M=np.matrix('45 13 -4 8;' +
    #             '-5 -28 4 -14;' +
    #             '9 15 63 -7;' +
    #             '2 3 -8 -42')
    
    # M = M.astype(float)

    M = np.array([[4, -1, 0, 3], 
                  [1, 15.5, 3, 8], 
                  [0, -1.3, -4, 1.1],
                  [14, 5, -2, 30]])
    b = np.array([1, 1, 1, 1]).astype(float)
    x = np.array([0, 0, 0, 0]).astype(float)

    # m=np.matrix('8 2 3 1;' +
    #             '0 6 4 0;' +
    #             '2 3 9 3;' +
    #             '1 2 3 7')
    # m = m.astype(float)
    # b = np.array([25, 24, 47, 42]).astype(float)
    # x = np.array([1, 1, 1, 1]).astype(float)

    tol = 1e-7
    n = 100
    norma = 2
    gausSeidel(M,b,x,norma,tol,n)

def gausSeidel(M,b,x,norm,tol,iteMax):
    n = len(x)
    L = np.tril(M)
    U = M - L
    lista  = []
    ite = 0
    print("|iter|", end = "")
    for i in range(n):
        print("      x{0}    |".format(i), end = "")
    print("   E   |")
    while(norm > tol and ite < iteMax):
        xold = x
        x = np.dot(np.linalg.inv(L), b - np.dot(U, x))
        norm = max(abs((x-xold)))
        print("|",str(ite).ljust(2),"|",end="")
        for i in x:
            print("%.9f"%i,"|", end = "")
        
        print("%.1e"%norm,"|")
        lista.append([ite,x,norm])
        ite +=1
    return x,lista

if __name__ == "__main__":
    main()