from defs import *

# Generate random integer input matrix (30 samples, 3 categories)
input_matrix = np.random.randint(1, 11, size=(30, 3))
output_matrix = np.copy(input_matrix)

input_min = np.min(input_matrix)
input_scale = np.max(input_matrix) - input_min
output_min = np.min(output_matrix)
output_scale = np.max(output_matrix) - output_min

input_matrix = (input_matrix - input_min) / input_scale
output_matrix = (output_matrix - output_min) / output_scale

# Split data into training and validation sets
split_ratio = 0.8
split_index = int(input_matrix.shape[0] * split_ratio)
x_train = input_matrix[:split_index]
y_train = output_matrix[:split_index]
x_val = input_matrix[split_index:]
y_val = output_matrix[split_index:]

# print(np.shape(input_matrix))
d_0, d_1 = int(np.shape(input_matrix)[0]), int(np.shape(input_matrix)[1])
d_L1 = int(np.shape(output_matrix)[1])
d_3 = d_L1
# print(np.shape(output_matrix))
arch = [3]
w1 = np.random.rand(d_1,arch[0])
b1 = np.random.rand(d_0,arch[0])

# w1, residuals, _, _ = np.linalg.lstsq(input_matrix, np.vectorize(Sigmoid.inv)(output_matrix), rcond=None)
# w1, residuals, _, _ = np.linalg.lstsq(input_matrix, output_matrix, rcond=None)
b1 = np.zeros((d_0,arch[0]))
w1 = np.eye(3, dtype='int')

# print(input_matrix @ w1 + b1)
print(np.linalg.norm(
    output_matrix - np.vectorize(Linear.reg)(input_matrix @ w1 + b1)
))
print(np.linalg.norm(np.zeros((30,3))))


w1 = np.random.rand(d_1,arch[0])
# b1 = np.random.rand(d_0,arch[0])

rate = 0.00001
epochs = 1000000
norm_stop = 0.0000001
current_norm = 0
last_norm = 0

Activ = Linear

for i in range(epochs):
    Z = input_matrix @ w1
    Y_pred = np.vectorize(Activ.reg)(Z)
    dC_dY_pred = Y_pred - output_matrix
    dC_dW = input_matrix.T @ (dC_dY_pred * np.vectorize(Activ.der)(Z))
    # dC_db = np.sum(dC_dY_pred * np.vectorize(Activ.der)(Z), axis=0, keepdims=True)

    w1 = w1 - rate * dC_dW
    # b1 = b1 - rate * dC_db
    if i % 10000 == 0:
        current_norm = np.linalg.norm(
            output_matrix - np.vectorize(Activ.reg)(input_matrix @ w1 + b1)
        )
        print(str(i) + "\t%2.6f\t%2.6f" % (current_norm, current_norm - last_norm))
        last_norm = current_norm
    if current_norm < norm_stop:
        print("norm limit %2.6f reached in %d epochs" % (norm_stop, i))
        break
print(w1)
print(output_matrix - np.vectorize(Activ.reg)(input_matrix @ w1 + b1))

# dCdw=2*(np.vectorize(Sigmoid.reg)(input_matrix @ w1 + b1)).T
# print(np.shape(2*(np.vectorize(Sigmoid.reg)(input_matrix @ w1 + b1))))
# print(np.shape((np.vectorize(Sigmoid.der)(input_matrix @ w1 + b1))))
# print(np.shape(input_matrix))
# dCdw = dCdw @ (np.vectorize(Sigmoid.der)(input_matrix @ w1 + b1)) @ input_matrix


