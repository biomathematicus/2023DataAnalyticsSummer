import numpy as np

np.random.seed(10)
np.seterr(all='raise')
sig_max = 600

def relu(x):
    return np.maximum(0, x)
def relu_derivative(x):
    return np.where(x > 0, 1, 0)

class Fct:
    def __init__(self, reg, der):
        self.reg = reg
        self.der = der
    def regVal(self, x):
        return self.reg(x)
    def derVal(self, x):
        return self.der(x)

def sigmoid(x):
    if x > sig_max: return 1
    if x < -sig_max: return 0
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    if abs(x) > sig_max: return 0
    return x * (1 - x)

def inverse_sigmoid(x):
    if x == 0: return -1001
    if x == 1: return 1001
    return np.log(x / (1 - x))
def inverse_sigmoid_derivative(x):
    return 1 / (x * (1 - x))

def linear(x):
    return x
def linear_derivative(x):
    return 1

Sigmoid = Fct(sigmoid, sigmoid_derivative)
Sigmoid.inv = inverse_sigmoid
Sigmoid.invDer = inverse_sigmoid_derivative

Relu = Fct(relu, relu_derivative)
Linear = Fct(linear, linear_derivative)
Linear.inv = lambda x: x

# Define Mean Squared Error loss function
def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)