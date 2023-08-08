import numpy as np
from numpy import linalg as la

def MDA(X,y,numComponents):
    # calculating number of classes, number of c
    c = len(np.unique(y))
    numComponents = min(c - 1, X.shape[1])
    #calculate overall mean and class means
    Xbar = np.mean(X,0).reshape(-1,1)
    Xbar_k = [np.mean(X[y == i]) for i in np.unique(y)]
    #finding within-class scatter, Sw=SUM_{i=1}^c SUM_{x IN D_i} (x - m_i)(x - m_i)^T and
    #finding between-class scatter, Sb=SUM_{i=1}^c n_i(m_i - m)(m_i - m)^T
    Sw = np.zeros((X.shape[1],X.shape[1]))
    Sb = np.zeros((X.shape[1],X.shape[1]))
    for i in range(c):
        Xsi = X[y == i]
        Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
        Bi = Xsi.shape[0] * (Xbar_k[i] - Xbar) @ (Xbar_k[i] - Xbar).T
        Sw += Si        
        Sb += Bi
    #solving Sw^-1Sbw_i=lambda_iSww_i for the eigenvalues and eigenvectors
    eigVals, eigVecs = la.eig(la.inv(Sw) @ Sb)
    eigVals = np.real(eigVals)
    eigVecs = np.real(eigVecs)
    #sorting the e-values and e-vectors
    idx = eigVals.argsort()[::-1]   
    eigVals = eigVals[idx]
    eigVecs = eigVecs[:,idx]

    #building the projection matrix W
    W = eigVecs[:, :numComponents]

    projX = X @ W
    return X