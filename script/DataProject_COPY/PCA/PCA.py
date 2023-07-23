import numpy as np
import matplotlib.pyplot as plt
import HW1969_PCA

from HW1969_PCA import data1969


class PCA: 
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = None
        self.mean = None
        
    def fit(self, X):
        # mean
        self.mean = np.mean(X, axis=0)
        X = X - self.mean
        
        # covariance
        # row = 1 sample, column = feature
        cov = np.cov(X.T)
        
        # eigenvectors, eigenvalues
        eigenvalues, eigenvectors = np.linalg.eig(cov)
        #v[:, i]
        
        # sort eigenvectors
        eigenvectors = eigenvectors.T
        idxs = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idxs]
        eigenvectors = eigenvectors[idxs]
        
        # store first n eigenvectors
        self.components = eigenvectors[0:self.n_components]
        
    def transform(self, X):
        #project data
        X = X - self.mean
        return np.dot(X, self.components.T)
data = HW1969_PCA()    
X= data.data
y= data.target

#projection onto 2 primary linear discriminatnts
pca = PCA(2)
pca.fit(X,y)
X_projected = pca.transform(X)

print('SHape of X:', X.shape)
print('Shape of Transformed X:', X_projected.shape)

x1= X_projected[:, 0]
x2 = X_projected[:, 1]

plt.scatter(x1, x1,
            c=y, edgecolor='none', alpha=0.8,
            cmap=plt.cm.get_cmap('',3))

plt.xlabel('Linear Discriminant 1')
plt.ylabel('Linear Discriminant 2')
plt.colorbar()
plt.show()