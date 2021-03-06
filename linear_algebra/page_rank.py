#!/usr/bin/env python
# coding: utf-8

# In[116]:


import numpy as np

# A = np.array([[0, 1, 1, 0, 0, 0],
#               [1, 0, 1, 0, 0, 0],
#               [1, 0, 0, 1, 1, 0],
#               [1, 0, 0, 0, 0, 1],
#               [0, 1, 1, 1, 0, 1],
#               [0, 0, 0, 1, 0, 0]])

A = np.array([[0, 0, 1, 1],
              [0, 1, 0, 1],
              [1, 0, 0, 0],
              [1, 0, 1, 1]])

print('A - the adjacency matrix, row - from which vertex, column - to which vertex', A, sep='\n\n', end='\n\n')
P_right = np.array([(j / sum(i)) for i in A for j in i]).reshape(A.shape)
print('P_right - right stochastic matrix', P_right, sep='\n\n', end='\n\n')

P_left = P_right.T
print('P_left - left stochastic matrix, the same as in the lecture', P_left, sep='\n\n', end ='\n\n')

Q = (1 / len(A[0])) * np.ones(A.shape)

P_coef = 0.85 * P_left + 0.15 * Q
print('P_coef', P_coef, sep='\n\n', end='\n\n')

v, w = np.linalg.eig(P_coef)

for value in v:
    if round(value) == 1:
        index = list(v).index(value)

eigenvector = w.T[index]
eigenvector = [round(v, 2) for v in eigenvector]
print('eigenvector', eigenvector, sep='\n\n', end='\n\n')

vertex = eigenvector.index(max(eigenvector))
print('The most influenced vertex in this graph (numbering starts from 0) is', vertex)


# In[ ]:




