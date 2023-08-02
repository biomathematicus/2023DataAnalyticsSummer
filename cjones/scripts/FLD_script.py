import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as la

def FLD(X, y, numComponents):
    # finds the within-class scatter matrix, Sw = SUM_{x IN D_i} (x - m_i)(x - m_i)^T
    c = len(np.unique(y))
    m = X.shape[0]/len(np.unique(y))
    indexArr = np.repeat(np.arange(c), m)
    Sw = np.zeros((X.shape[1],X.shape[1]))
    Sb = np.zeros((X.shape[1],X.shape[1]))
    Xbar = np.mean(X, axis = 0).reshape(-1,1)
    Xbar_k = [np.mean(X[indexArr == i], axis=0) for i in range(c)]
    for i in range(c):
        Xsi = X[indexArr == i]
        Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
        Bi = Xsi.shape[0] * (Xbar_k[i] - Xbar) @ (Xbar_k[i] -Xbar).T
        Sw += Si
        Sb += Bi
    #getting the ordered eigenvalues and eigenvectors by solving 
    # Sw^{-1}Sbw=lambda*w; note, Sw must be non-singular
    eigVals, eigVecs = la.eig(np.dot(la.inv(Sw), Sb))

    idx = eigVals.argsort()[::-1]   
    eigVals = eigVals[idx]
    eigVecs = eigVecs[:,idx]

    # W = eigVecs[:, :numComponents]
    # return W @ X

    x = X @ eigVecs[:,0]
    y = X @ eigVecs[:,1]

    return x, y
