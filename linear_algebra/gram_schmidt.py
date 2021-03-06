import numpy as np
from numpy import sqrt
import numpy.linalg as LA


def gs_cofficient(a, b):
    denominator = np.dot(b, b)
    if denominator == 0:
        return 0
    return np.dot(a, b) / np.dot(b, b)  # getting the coefficient for each b_i


def gs_process(A):
    B = []
    for i in np.arange(A.shape[0]):
        a_i = A[i]
        for b in B:
            proj_vec = gs_cofficient(a_i, b) * b
            a_i = a_i - proj_vec
        B.append(a_i)
    return np.array(B)


# to normalize the basis:
def normalize(X):
    return np.array([x / LA.norm(x)
                     if LA.norm(x) != 0
                     else np.zeros(len(x))
                     for x in X])


if __name__ == '__main__':
    # example use
    # a1 = np.array([1, 1, 0, 0])
    # a2 = np.array([-2, 0, 1, 0])
    # a3 = np.array([-1, 0, 0, 1])
    # A = np.array([a1, a2, a3])
    # a1 = np.array([2, 0, -4, 1])
    # a2 = np.array([-3, 0, -5, 9])
    # A = np.array([a1, a2])
    # basis = gs_process(A)
    # print("Orthogonal basis:", basis)

    # normalized = normalize(basis)
    # print("Orthonormal basis:", normalized)

    U = np.array([[1/sqrt(7), 1/sqrt(2), -1/sqrt(3), -1/sqrt(42)],
                  [-1/sqrt(7), 1/sqrt(2), 1/sqrt(3), 1/sqrt(42)],
                  [2/sqrt(7), 0, 1/sqrt(3), -sqrt(2/21)],
                  [1/sqrt(7), 0, 0, sqrt(6/7)]])

    S = np.array([[sqrt(63), 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
    V = np.array([[-2/3, sqrt(2)/6, 1/sqrt(2)],
                  [-1/3, -sqrt(8)/3, 0],
                  [-2/3, sqrt(2)/6, -1/sqrt(2)]])

    res = U @ S @ V.T
    print(res.round(0))

