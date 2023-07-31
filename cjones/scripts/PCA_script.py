import numpy as np

def PCA(X):
    #we find Xbar and extract values of dimensions from X
    Xbar = X - np.mean(X,0)

    #we find the scatter matrix, SUM_[k=1]^n (x_k - m)^T(x_k - m)
    scatterX = np.dot(Xbar.T, Xbar)

    #find the eigenvalues and eigenvectors of the covariance matrix, using np.linalg.eigh()
    #Note: numpy.eigh() returns a matrix of eigenvectors and a matrix of RIGHT eigenvalues
    #our equation, Se=lambda*e, requires only the right eigvenvalues so this is fine, but
    #be aware of this in the future. Also, since we know that the covariance matrix is symmetric
    #we should use numpy.eigh() instead of numpy.eig() since it is optimized for symmetric
    #matrices
    eigVals, eigVecs = np.linalg.eigh(scatterX)

    #project X onto 2-dimensions
    x = X @ eigVecs[:,-1]
    y = X @ eigVecs[:,-2]
    z = X @ eigVecs[:,-3]

    #if not using eigh(), use the following arguments to sort the e-vals in ascending order 
    #and then sort the e-vecs to them
    # idx.argsort()[::-1]
    # eigVals = eigVals[idx]
    # eigVecs = eigVecs[:,idx]
    
    #return the projection of X onto 2-D
    return x, y, z