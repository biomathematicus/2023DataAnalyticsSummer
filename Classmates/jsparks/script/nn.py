import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from defs import *

'''
Credit for original working code to Tamoghno Bhattacharya
https://gist.githubusercontent.com/TamoghnoBhattacharya/4883a801d0653d7f320dda6dfb56d695/raw/9c23333463d755ef248e6bb428c088dd4ac66183/neuralnet_from_scratch
https://towardsdatascience.com/an-introduction-to-neural-networks-with-implementation-from-scratch-using-python-da4b6a45c05b

'''

def relu(z):
    a = np.maximum(0,z)
    return a

class NeuralNetwork:
    def __init__(self,
                 X: np.ndarray,
                 Y: np.ndarray,
                 learning_rate: float,
                 layer_sizes: list,
                 Activ: Fct = Relu,
                 test_size: float = 0.2,
                 params: dict = {},
                 verbose: bool = False
                 ):
        self.X = X
        self.Y = Y
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=test_size)
        self.learning_rate = learning_rate
        self.Activ = Activ
        self.layer_sizes = layer_sizes
        self.params = params
        self.verbose = verbose
        if self.params == {}:
            self.randomize_params()

    def randomize_params(self):
        self.params = {}
        for i in range(1, len(self.layer_sizes)):
            self.params['W' + str(i)] = np.random.randn(self.layer_sizes[i], self.layer_sizes[i - 1]) * 0.01
            self.params['B' + str(i)] = np.random.randn(self.layer_sizes[i], 1) * 0.01

    def forward_propagation(self, input):
        layers = len(self.params) // 2
        values = {}
        for i in range(1, layers + 1):
            if i == 1:
                values['Z' + str(i)] = np.dot(self.params['W' + str(i)], input.T) + self.params['B' + str(i)]
                values['A' + str(i)] = self.Activ.reg(values['Z' + str(i)])
            else:
                values['Z' + str(i)] = np.dot(self.params['W' + str(i)], values['A' + str(i - 1)]) + self.params['B' + str(i)]
                if i == layers:
                    values['A' + str(i)] = values['Z' + str(i)]
                else:
                    values['A' + str(i)] = self.Activ.reg(values['Z' + str(i)])
        return values

    def compute_cost(self, values: dict):
        layers = len(values) // 2
        Y_pred = values['A' + str(layers)]
        cost = 1 / (2 * len(self.Y_train.T)) * np.sum(np.square(Y_pred - self.Y_train.T))
        return cost

    def backward_propagation(self,values: dict):
        layers = len(self.params) // 2
        m = len(self.Y_train.T)
        grads = {}
        for i in range(layers, 0, -1):
            if i == layers:
                dA = 1 / m * (values['A' + str(i)] - self.Y_train.T)
                dZ = dA
            else:
                dA = np.dot(self.params['W' + str(i + 1)].T, dZ)
                # dZ = np.multiply(dA, np.where(values['A' + str(i)] >= 0, 1, 0))
                dZ = np.multiply(dA, self.Activ.der(values['A' + str(i)]))
            if i == 1:
                grads['W' + str(i)] = 1 / m * np.dot(dZ, self.X_train)
                grads['B' + str(i)] = 1 / m * np.sum(dZ, axis=1, keepdims=True)
            else:
                grads['W' + str(i)] = 1 / m * np.dot(dZ, values['A' + str(i - 1)].T)
                grads['B' + str(i)] = 1 / m * np.sum(dZ, axis=1, keepdims=True)
        return grads

    def update_params(self, grads):
        layers = len(self.params) // 2
        params_updated = {}
        for i in range(1, layers + 1):
            params_updated['W' + str(i)] = self.params['W' + str(i)] - self.learning_rate * grads['W' + str(i)]
            params_updated['B' + str(i)] = self.params['B' + str(i)] - self.learning_rate * grads['B' + str(i)]
        self.params = params_updated

    def model(self, epochs):
        for i in range(epochs):
            values = self.forward_propagation(self.X_train)
            cost = self.compute_cost(values)
            grads = self.backward_propagation(values)
            self.update_params(grads)
            if (self.verbose):
                print('Cost at iteration ' + str(i + 1) + ' = ' + str(cost) + '\n')

    def compute_accuracy(self):
        values_train = self.forward_propagation(self.X_train)
        values_test = self.forward_propagation(self.X_test)
        train_acc = np.sqrt(mean_squared_error(self.Y_train, values_train['A' + str(len(self.layer_sizes) - 1)].T))
        test_acc = np.sqrt(mean_squared_error(self.Y_test, values_test['A' + str(len(self.layer_sizes) - 1)].T))
        return train_acc, test_acc

    def predict(self, X):
        values = self.forward_propagation(X.T)
        predictions = values['A' + str(len(values) // 2)].T
        return predictions

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

NN = NeuralNetwork(data, target, 0.03, [13, 5, 5, 1])
NN.Activ = Sigmoid
NN.model(100000)

train_acc, test_acc = NN.compute_accuracy()
print('Root Mean Squared Error on Training Data = ' + str(train_acc))
print('Root Mean Squared Error on Test Data = ' + str(test_acc))