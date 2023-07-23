import matplotlib.pyplot as plt
import LDA

from LDA import LDA
#importing data
#data = datasets.
X= data.data
y= data.target

#projection onto 2 primary linear discriminatnts
lda = LDA(2)
lda.fit(X,y)
X_projected = lda.transform(X)

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