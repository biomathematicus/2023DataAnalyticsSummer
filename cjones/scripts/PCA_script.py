import numpy as np

def PCA(X):
    #Performs PCA without standardizing the data
    #we find Xbar and extract values of dimensions from X
    #also provides the necessary data for a Scree plot
    Xbar = X - np.mean(X,0)

    #we find the scatter matrix, SUM_[k=1]^n (x_k - m)^T(x_k - m)
    scatterX = np.dot(Xbar.T, Xbar)

    #find between-scatter
    eigVals, eigVecs = np.linalg.eigh(scatterX)
    eigVals = np.real(eigVals)
    eigVecs = np.real(eigVecs)

    #finding the explained variance data to create Scree plot
    explainedVar = eigVals / np.sum(eigVals)
    cumulativeExpVar = np.cumsum(explainedVar)

    #project X onto 3-dimensions
    x = X @ eigVecs[:,-1]
    y = X @ eigVecs[:,-2]
    z = X @ eigVecs[:,-3]
    
    #return the projection of X onto 3-D
    return x, y, z, explainedVar, cumulativeExpVar