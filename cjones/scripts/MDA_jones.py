import numpy as np
from numpy import linalg as la

#dummy data
n = 5
m = 100
c = 2
A = np.random.rand(m,n)
B = A + 0.2
X = np.concatenate((A,B),axis=0)

#finding total mean vector and class mean vectors
Xbar = np.mean(X,0).reshape(n,1)
indexArr = np.repeat(np.arange(c), (m))
Xbar_k = [np.mean(X[indexArr == i]) for i in range(c)]

#finding within-class scatter, Sw=SUM_{i=1}^c SUM_{x IN D_i} (x - m_i)(x - m_i)^T
Sw = np.zeros((n,n))
for i in range(c):
    Xsi = X[indexArr == i]
    Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
    Sw += Si

#finding between-class scatter, Sb=SUM_{i=1}^c n_i(m_i - m)(m_i - m)^T
Sb = np.zeros((n,n))
for i in range(c):
    Ni = len(X[indexArr == i])
    Si = Ni * (Xbar_k[i] - Xbar) @ (Xbar_k[i] - Xbar).T

#solving Sw^-1Sbw_i=lambda_iSww_i for the eigenvalues and eigenvectors
eigVals, eigVecs = la.eig(la.inv(Sw) @ Sb)
#sorting the e-values and e-vectors
idx = eigVals.argsort()[::-1]   
eigVals = eigVals[idx]
eigVecs = eigVecs[:,idx]

#building the projection matrix W
numComponents = c-1
W = eigVecs[:, :numComponents]

projX = X @ W