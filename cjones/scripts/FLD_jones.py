import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as la

#dummy data
n = 1
m = 100
A = np.linspace(0,10,100).reshape(1,100)
B = A + 1
# A = np.random.rand(m,n)
# B = A + 0.2
X = np.concatenate((A,B),axis=0)

#finds the means of each dimenions (column-vector)
#converts the output to a (5,1) vector instead of a (5,) object
Xbar1 = np.mean(A,0).reshape(m,1)
Xbar2 = np.mean(B,0).reshape(m,1)

Sw1 = []
Sw2 = []
for i in range(m):
    Sw1.append(np.dot((A[0][i]-Xbar1),(A[0][i]-Xbar1).T))
    Sw2.append(np.dot((B[0][i]-Xbar2),(B[0][i]-Xbar2).T))
Sw1 = np.array(Sw1)
Sw2 = np.array(Sw2)
Sw1 = np.sum(Sw1,axis=0)
Sw2 = np.sum(Sw2,axis=0)
Sw = Sw1 + Sw2

#building the within-class scatter matrix, Sw = S_1 + S_2, where
#S_1 = SUM x IN D_1 (x - m_i)^T(x - m_i), S_2 defined similarly for x IN D_2
#all of this math is twice confirmed, and the Python operations are confirmed
# Sw1 = []
# Sw2 = []
# for i in range(m):
#     Sw1.append(np.dot((A[i]-Xbar1),(A[i]-Xbar1).T))
#     Sw2.append(np.dot((B[i]-Xbar2),(B[i]-Xbar2).T))
# Sw1 = np.array(Sw1)
# Sw2 = np.array(Sw2)
# Sw1 = np.sum(Sw1,axis=0)
# Sw2 = np.sum(Sw2,axis=0)
# Sw = Sw1 + Sw2

# #building the between-class scatter matrix, Sb = (m_1 - m_2)^T(m_1 - m_2)
Sb = np.dot((Xbar1 - Xbar2), (Xbar1 - Xbar2).T)

# #getting the ordered eigenvalues and eigenvectors by solving 
# # Sw^{-1}Sbw=lambda*w; note, Sw must be non-singular
eigVals, eigVecs = la.eigh(np.dot(la.inv(Sw), Sb))

# # #build w using the e-vectors of Sw^{-1}Sbw=lambda*w, making the e-vecs
# # #the columns of w
w = np.dot(la.inv(Sw),(Xbar1-Xbar2))
Y = w.T @ X
fig = plt.figure(1)
fig.clf()
plt.scatter(X,Y)
plt.show()

# #projecting the data X onto the space Y using w
x = X @ eigVecs[:,-1]
y = X @ eigVecs[:,-2]

fig = plt.figure(2)
fig.clf()
plt.scatter(x[0:m-1],y[0:m-1])
plt.scatter(x[m:-1],y[m:-1])
plt.show()