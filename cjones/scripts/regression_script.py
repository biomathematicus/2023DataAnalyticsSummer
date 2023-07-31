import numpy as np
from numpy import linalg as la
from matplotlib import pyplot as plt

def main():
    t = np.arange(0,np.pi,.1).reshape(-1,1)
    n = np.size(t)
    s = np.std(np.multiply(np.cos(t),t)/np.random.rand())
    x = np.multiply(np.cos(t),t) + s * np.random.rand(n,1)
    b = 10

    x1 = regression(t,x,b,1)
    x2 = regression(t,x,b,2)
    x3 = regression(t,x,b,3)

    fig = plt.figure(1) 
    fig.clf()
    plt.plot(t,x)
    plt.plot(t,x1)
    plt.plot(t,x2)
    plt.plot(t,x3)
    plt.show()

def regression(x, y, b, basis):
    x = x-x[0];
    L = x[-1] - x[0]
    alpha = np.random.rand()
    beta = np.random.rand()
    cBasis = []
    A = np.zeros((b,b))
    w = np.zeros(b)
    s = np.zeros((len(x),1))
    for i in range(b):
        if basis == 1:
            cBasis.append(np.cos((i) * np.pi * x / L))
        if basis == 2:
            cBasis.append(np.multiply(np.power(x, i), np.exp(i * x / L)))
        if basis == 3:
            cBasis.append(np.power(x, i))
    cBasis = np.array(cBasis)
    for i in range(b):
        for j in range(b):
            A[i][j] = CNintegral(x, np.multiply(cBasis[i], cBasis[j]))
        w[i] = CNintegral(x, np.multiply(y, cBasis[i]))
    w = w.reshape(b,1)
    c = la.lstsq(A, w, rcond=0)
    c = c[0]
    for i in range(b):
        s = (s +  c[i] * cBasis[i])
    return s

def CNintegral(x,y):
    I = 0
    n = len(x)
    dx = (x[-1] - x[0]) / n
    for i in range(1,n):
        I = I + (y[i-1]+y[i]) / 2 * dx
    return I    

if __name__ == "__main__":
    main()