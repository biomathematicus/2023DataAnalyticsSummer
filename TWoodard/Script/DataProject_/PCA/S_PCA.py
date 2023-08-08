import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

m = 100
n = 20
X = np.random.rand(m,n)
Z = np.random.rand(m,n) + 0.1
# X1 = np.random.rand(m,n) + 1
Y = np.concatenate((X,Z),axis = 0)


#Standardize X
N_x = Y-Y.mean(0)

#Covariance of X
covX = np.cov(N_x.T)

#eval/evec of our covariance matrix
eva, eve = np.linalg.eig(covX)

#indicies
ind = eva.argsort()[::-1]
eva = eva[ind]
eve = eve[:,ind]

x = Y @ eve[:,0]
y = Y @ eve[:,1]
z = Y @ eve[:,2]

fig = plt.figure(1)
plt.scatter(x[0:m-1],y[0:m-1], label= 'X', marker='d')
plt.scatter(x[m:],y[m:], label= 'Z', marker= 'X')
# plt.scatter(x[2*m:],y[2*m:], label= 'X1', marker= 'h')
plt.show()

fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[0:m-1],y[0:m-1], z[0:m-1], label= 'X', marker= 'd')
ax.scatter(x[m:-1],y[m:-1], z[m:-1], label= 'Z', marker= 'X')
# ax.scatter(x[2*m:],y[2*m:], z[2*m:], label= 'X1', marker= 'h')
plt.show()