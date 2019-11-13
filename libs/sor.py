import numpy as np

def main():
    # M=np.matrix('45 13 -4 8;' +
    #             '-5 -28 4 -14;' +
    #             '9 15 63 -7;' +
    #             '2 3 -8 -42')
    
    # M = M.astype(float)

    # M = np.array([[45, 13, -4, 8], 
    #               [-5, -28, 4, -14], 
    #               [9, 15, 63, -7],
    #               [2, 3, -8, -42]])
    # b = np.array([-25, 82, 75, -43]).astype(float)
    # x = np.array([2, 2, 2, 2]).astype(float)

    # m=np.matrix('8 2 3 1;' +
    #             '0 6 4 0;' +
    #             '2 3 9 3;' +
    #             '1 2 3 7')
    # m = m.astype(float)
    # b = np.array([25, 24, 47, 42]).astype(float)
    # x = np.array([1, 1, 1, 1]).astype(float)

    # tol = 1e-7
    # n = 100
    # norma = 2
    # omega=1.5
    # sor(M,b,x,norma,tol,n,omega)
    
    M = np.array([[4, -1, 0, 3], 
                  [1, 15.5, 3, 8], 
                  [0, -1.3, -4, 1.1],
                  [14, 5, -2, 30]])
    b = np.array([1, 1, 1, 1]).astype(float)
    x = np.array([0, 0, 0, 0]).astype(float)

    tol = 1e-7
    n = 100
    norma = 2
    omega=1.5
    sor(M,b,x,norma,tol,n,omega)

def sor(M,b,x,norm,tol,iteMax,omega):

    n = len(x)
    L = np.tril(M)
    U = M - L
    D = np.diag(M)
    
    ite = 0
    print("|iter|", end = "")
    for i in range(n):
        print("      x{0}    |".format(i), end = "")
    print("   E   |")
    while(norm > tol and ite < iteMax):
        xold = x
        Tw = np.dot(np.linalg.inv(D-L*omega),(1-omega)*D+omega*U)
        Cw = np.dot(omega*np.linalg.inv(D-omega*L),b)
        x = np.dot(Tw,x)+Cw

        
        norm = max(abs((x-xold)))
        print("|",str(ite).ljust(2),"|",end="")
        for i in x:
            print("%.9f"%i,"|", end = "")
        
        print("%.1e"%norm,"|")
        ite +=1


if __name__ == "__main__":
    main()