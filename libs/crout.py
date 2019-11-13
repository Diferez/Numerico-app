import numpy as np

def crout(A,b):
    
    A = np.c_[A, b]
    n, columnas = A.shape
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for k in range(0, n):
        U[k, k] = 1 

        for j in range(k, n):
            sum0 = sum([L[j, s] * U[s, k] for s in range(0, j)]) 
            L[j, k] = A[j, k] - sum0 

        for j in range(k+1, n):
            sum1 = sum([L[k, s] * U[s, j] for s in range(0, k)]) 
            U[k, j] = (A[k, j] - sum1) / L[k, k]



    print(L)
    print()
    print(U)
    return L, U


if __name__ == "__main__":
    A = np.array([[4, -1, 0, 3], 
         [1, 15.5, 3, 8], 
         [0, -1.3, -4, 1.1], 
         [14, 5, -2, 30]])
    b = np.array([1,1,1,1])
    crout(A,4)