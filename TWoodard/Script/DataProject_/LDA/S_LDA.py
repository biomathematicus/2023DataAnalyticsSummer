import numpy as np
import matplotlib.pyplot as plt

m = 250
n = 20
X = np.random.rand(m, n)

# Standardizing the data
class Scaler:
    def __init__(self):
        self.mean_ = None
        self.std_ = None
        
    def fit(self, X):
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        
    def transform(self, X):
        if self.mean_ is None or self.std_ is None:
            raise ValueError("Scaler has not been fitted. Call fit() before transform().")
        return (X - self.mean_) / self.std_

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
scaler = Scaler()
X_scaled = scaler.fit_transform(X)

#LDA Setup
class LDA:
    def __init__(self):
        self.W = None
    
    def fit(self, X, y):  
        m, n = X.shape
        nClass = len(np.unique(y))
        nFeat = X.shape[1]
        Xmean = X.mean(axis=0)
        
        C_mean = []
        C_cov = []
        for i in range(nClass):
            C_mean.append(X[y == i].mean(axis=0))
            C_cov.append(np.cov(X[y == i].T))
        
        # Within-Class Matrix    
        S_w = np.zeros((nFeat, nFeat))
        for i in range(nClass):
            S_w += C_cov[i]
        
        # Between-Class Matrix    
        S_b = np.zeros((nFeat, nFeat))
        for i in range(nClass):
            d_mean = C_mean[i] - Xmean
            S_b += len(X[y == i]) * np.outer(d_mean, d_mean)
        
        # Eigenvalue problem
        eva, eve = np.linalg.eig(np.linalg.inv(S_w) @ S_b)
        
        # Sorting the eigenvectors 
        idxs = np.argsort(eva)[::-1]
        eve = eve[:, idxs]
        
        # Data Projection
        self.W = eve[:, :nClass - 1]

    def transform(self, X):
        if self.W is None:
            raise ValueError("LDA has not been fitted. Call fit() before transform().")
        return X @ self.W

y = np.random.randint(0, 5, m)

# Perform LDA 
lda_model = LDA()
lda_model.fit(X_scaled, y)
X_lda = lda_model.transform(X_scaled)

# Plot the data in the LDA space
colors = ['r', 'g', 'b', 'y', 'm']
for i in range(5):
    plt.scatter(X_lda[y == i, 0], X_lda[y == i, 1], label=f'Class {i}', c=colors[i])

plt.xlabel('LD1')
plt.ylabel('LD2')
plt.legend()
plt.title('LDA on Data with Custom Class Labels in 2D')
plt.grid(True)
plt.show()

