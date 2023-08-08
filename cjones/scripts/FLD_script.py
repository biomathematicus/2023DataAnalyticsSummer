import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as la

def FLD(X, y, numComponents):
     # determines number of classes and components to put put into the projection matrix
    c = len(np.unique(y))
    numComponents = min(c - 1, X.shape[1])
    #calculate overall mean and class means
    Xbar = np.mean(X, axis = 0).reshape(-1,1)
    Xbar_k = [np.mean(X[y == i], axis=0) for i in np.unique(y)]
    Sw = np.zeros((X.shape[1],X.shape[1]))
    Sb = np.zeros((X.shape[1],X.shape[1]))
    #calculating within-class scatter matrix Sw and between-class scatter matrix Sb
    for i in range(c):
        Xsi = X[y == i]
        Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
        Bi = Xsi.shape[0] * (Xbar_k[i] - Xbar) @ (Xbar_k[i] -Xbar).T
        Sw += Si
        Sb += Bi
    #getting the ordered eigenvalues and eigenvectors by solving 
    # Sw^{-1}Sbw=lambda*w; note, Sw must be non-singular
    eigVals, eigVecs = la.eig(np.dot(la.inv(Sw), Sb))
    eigVals = np.real(eigVals)
    eigVecs = np.real(eigVecs)
    idx = eigVals.argsort()[::-1]   
    eigVals = eigVals[idx]
    eigVecs = eigVecs[:,idx]

    W = eigVecs[:, :numComponents]
    return X @ W

