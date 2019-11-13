from math import sqrt
from pprint import pprint
 
def cholesky(A):

    n = len(A)

    L = [[0.0] * n for _ in range(len(A))]


    for i in range(len(A)):
        for k in range(i+1):
            suma = sum(L[i][j] * L[k][j] for j in range(k))
            
            if (i == k):
                L[i][k] = sqrt(A[i][i] - suma)
            else:
                L[i][k] = (1.0 / L[k][k] * (A[i][k] - suma))
    return L
 


if __name__ == "__main__":
    A = [[4, -1, 0, 3], 
         [1, 15.5, 3, 8], 
         [0, -1.3, -4, 1.1], 
         [14, 5, -2, 30]]
    L = cholesky(A)
    print ("A:")
    pprint(A)
    print ("L:")
    pprint(L)