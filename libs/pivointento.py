import numpy as np
import math

def main():
    # m=np.matrix('1 -3 2;' +
    #             '5 6 -1;' +
    #             '4 -1 3')
    M = np.array([[4, -1, 0, 3], 
                  [1, 15.5, 3, 8], 
                  [0, -1.3, -4, 1.1],
                  [14, 5, -2, 30]])
    # m = np.matrix('0 0  1  0 1;' +
    #               '0 3 -2 -2 0;' +
    #               '2 0 -0.27 -1 -2;' +
    #               '0 1 -0.25 -0 0;' +
    #               '1.5 0 0 0 -1')

    # b = np.array([-12, 6, -6, 0])
    b = np.array([1, 1, 1, 1])
    luP(M,b)
    #gauss(m,b)
    x= np.array([-1, 0, 3, 4])
    y = np.array([15.5, 3, 8, 1])
    # x= np.array([-2, -1, 2, 3])
    # y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923])

    #vandermonde(x,y)


def switchCols(M, c1, c2):
    M[:, [c1, c2]] = M[:, [c2, c1]]
    return M


def switchRows(M, r1, r2):
    M[[r1, r2]] = M[[r2, r1]]
    return M


def gauss(M, b):

    lista =[]

    Ab = np.c_[M, b]
    n, columnas = Ab.shape
    Ab = Ab.astype(float) 

    if(np.linalg.det(M) == 0):
        print("El sistema no tiene solucion")
    else:
        for c in range(0, n):
            
            mayor = abs(Ab[c, c])
            filam = c
            columnam = c
            for f in range(c, n):
                for j in range(c, n):
                    if(abs(Ab[f, j]) > mayor):
                        mayor = abs(Ab[f, j])
                        filam = f
                        columnam = j
            if (filam != c):
                Ab = switchRows(Ab, filam, c)

            if (columnam != c):
                Ab = switchCols(Ab, columnam, c)


            for s in range(c + 1, n):
                multi = Ab[s, c]/Ab[c, c]
                for i in range(0, columnas):
                    Ab[s, i] = Ab[s, i] - multi * Ab[c, i]
                lista.append(np.copy(Ab))
    printM(Ab)
    #print(susRegresiva(Ab))
    return susRegresiva(Ab), lista
 
                
def gaussParcial(M, b):

    lista = []

    Ab = np.c_[M, b]
    n, columnas = Ab.shape
    Ab = Ab.astype(float) 

    if(np.linalg.det(M) == 0):
        print("El sistema no tiene solucion")
    else:
        for c in range(0, n):
            
            mayor = abs(Ab[c, c])
            filam = c
            columnam = c
            for f in range(c, n):
                for j in range(c, n):
                    if(abs(Ab[f, j]) > mayor):
                        mayor = abs(Ab[f, j])
                        filam = f
                        columnam = j
            if (filam != c):
                Ab = switchRows(Ab, filam, c)




            for s in range(c + 1, n):
                multi = Ab[s, c]/Ab[c, c]
                for i in range(0, columnas):
                    Ab[s, i] = Ab[s, i] - multi * Ab[c, i]
                
                lista.append(np.copy(Ab))

 
                
            
    


    printM(Ab)
    print("Vector Solucion")
    #print(susRegresiva(Ab))
    return susRegresiva(Ab), lista       
    




def gaussSimple(M, b):

    lista = []

    Ab = np.c_[M, b]
    n, columnas = Ab.shape
    Ab = Ab.astype(float) 
    if(np.linalg.det(M) == 0):
        print("El sistema no tiene solucion")
    else:
        for c in range(0, n):
            
            mayor = abs(Ab[c, c])
            filam = c
            columnam = c


            for s in range(c + 1, n):
                multi = Ab[s, c]/Ab[c, c]
                for i in range(0, columnas):
                    Ab[s, i] = Ab[s, i] - multi * Ab[c, i]
                
                lista.append(np.copy(Ab))


    
                
            
    

    
    printM(Ab)
    print("Vector Solucion")
    #print(susRegresiva(Ab))
    return susRegresiva(Ab), lista

def lu(M,b):
    lista = []
    Ab = np.c_[M, b]
    n, columnas = Ab.shape
    Ab = Ab.astype(float)

    x = np.identity(n) 
    
    U = np.zeros((n,n))
    if(np.linalg.det(M) == 0):
        print("El sistema no tiene solucion")
    else:
        print("Matriz Aumentada")
        printM(Ab)
        for c in range(0, n):
            mayor = abs(Ab[c, c])
            filam = c
            columnam = c
            for s in range(c + 1, n):
                multi = Ab[s, c]/Ab[c, c]
                for i in range(0, n+1):
                    
                    if(i<n):
                        Ab[s, i] = Ab[s, i] - multi * Ab[c, i]

                        x[s, i] = x[s, i] - multi * x[c, i]
                    else:
                        Ab[s, i] = Ab[s, i] - multi * Ab[c, i]

            lista.append([np.linalg.inv(np.copy(x)),np.copy(Ab)[:,:-1]])

    
    

    print("Matriz L")
    x= np.linalg.inv(x) 
    printM(x)

    print("Matriz U")
    printM(Ab[:,:-1])

    print("Matriz L*U")
    #C = np.dot(Ab,x)
    C = np.dot(x,Ab[:,:-1])
    printM(C)
    print("Vector Solucion")
    return susRegresiva(Ab), lista

def luP(M,b):
    lista = []

    Ab = np.c_[M, b]
    n, columnas = Ab.shape
    Ab = Ab.astype(float) 
    x = np.identity(n) 
    p = np.identity(n) 
    if(np.linalg.det(M) == 0):
        print("El sistema no tiene solucion")
    else:
        print("Matriz Aumentada")
        printM(Ab)
        for c in range(0, n):
            mayor = abs(Ab[c, c])
            filam = c
            columnam = c
            for f in range(c, n):
                if(abs(Ab[f, c]) > mayor):
                    mayor = abs(Ab[f, c])
                    filam = f
                    columnam = c
            if (filam != c):
                Ab = switchRows(Ab, filam, c)
                x = switchRows(x, filam, c) 
                p = switchRows(p, filam, c) 
            
            for s in range(c + 1, n):
                multi = Ab[s, c]/Ab[c, c]
                for i in range(0, n+1):
                    Ab[s, i] = Ab[s, i] - multi * Ab[c, i]
                    if(i<n):
                        x[s, i] = x[s, i] - multi * x[c, i]
            
            lista.append([np.linalg.inv(np.copy(x)),np.copy(Ab)[:,:-1],np.copy(p)])
        


            



    print("Matriz L")
    x= np.linalg.inv(x) 
    printM(x)
    print("Matriz U")
    printM(Ab[:,:-1])

    print("Matriz P")
    printM(p)

    print("Matriz L*U")
    #C = np.dot(Ab,x)
    C = np.dot(x,Ab[:,:-1])
    printM(C)
    print("Vector Solucion")
    return susRegresiva(Ab), lista

def susRegresiva(A):
    
    n = A.shape[0]
    x = [0]*n
    for i in range (n-1,-1,-1):
        x[i] = A[i,n] / A[i,i]
        for k in range(i-1, -1, -1):
            A[k,n] -= A[k,i] * x[i]
    return(x)

def susRegresivaR(A):
    print(A)
    n = A.shape[1]
    x = [0]*n
    for i in range (n-1,-1,-1):
        suma = 0
        
        for k in range(i+1, n):
            suma = suma + A[i,k] * x[k]
        x[i] = (A[i,n+1]-suma)/A[i,i]
    return(x)

def vandermonde(x,y):
    
    n = len(x)
    M = np.zeros((n,n))
    for j in range(n):
        for i in range(n):
            M[i,j] = x[i]**j
    print("Matriz de Vandermonde")
    printM(M)
    print("Gauss Total")
    Ab = gauss(M,y)
    A = Ab[:,:-1]
    




def printM(M):

    for i in range(0, M.shape[0]):

        for j in range(0, M.shape[1]):
            print("|"+str("%.4f" % M[i, j]).center(6, " ")[:6]+"|", end='')
        print("")



if __name__ == "__main__":
    main()
