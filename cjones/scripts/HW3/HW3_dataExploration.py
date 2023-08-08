import psycopg2 as psy
import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as la
import seaborn as sns
import pandas as pd

def main():
    n = 1  # Set the number of samples you want (change as needed)

    # Query the database 'n' times for 1000 samples each
    all_samples = [queryDB() for _ in range(n)]
    
    combinedData = np.concatenate(all_samples, axis=0)
    np.random.shuffle(combinedData)

    # Separate features from labels
    X = combinedData[:, :-1]
    y = combinedData[:, -1]

    columns = ["am_m_age36", "am_prenatal", "am_gestation", "am_birthweight"]
    # Visualize the distribution of each variable
    # Do this manually for each check, don't do this programmatically
    df = pd.DataFrame(X, columns=["am_m_age36", "am_prenatal", "am_gestation", "am_birthweight"])
    sns.pairplot(df)
    plt.show()
    
    xPCA, yPCA, zPCA, explainedVar, cumulativeExpVar = PCA(X)
    xPCAstd, yPCAstd, zPCAstd, explainedVarStd, cumulativeExpVarStd = stdPCA(X)
    xFLD = FLD(X,y)
    xMDA = MDA(X,y)

    components = [xPCA, yPCA, zPCA]
    labels = ['PCA1', 'PCA2', 'PCA3']
    pca_kde_plot(components, labels, y)
    PCAscatter(components, labels, y)
    explainedVariance(explainedVar, cumulativeExpVar)
    components = [xPCAstd, yPCAstd, zPCAstd]
    labels = ['PCA1std', 'PCA2std', 'PCA3std']
    pca_kde_plot(components, labels, y)
    PCAscatter(components, labels, y)
    explainedVariance(explainedVarStd, cumulativeExpVarStd)

    Sw_FLD, Sb_FLD, ratio_FLD = get_scat_ratio(X, y, FLD)
    Sw_MDA, Sb_MDA, ratio_MDA = get_scat_ratio(X, y, MDA)
    print("FLD Scatter Ratio: {:.4f}".format(ratio_FLD))
    print("MDA Scatter Ratio: {:.4f}".format(ratio_MDA))

    visualize_FLD(xFLD, y)
    visualize_MDA(xMDA, y, columns)

def pca_kde_plot(components,labels,y):
        # Scatter plot for each combination of PCA components in a single figure along with KDE plots
        fig, axes = plt.subplots(3, 3, figsize=(15, 15))
        fig.suptitle('Scatter Plots of PCA Components', fontsize=16)

        for i in range(3):
            for j in range(3):
                if i == j:
                    # Diagonal plots - KDE plots for individual components
                    sns.kdeplot(components[i], ax=axes[i, j], label=f'{labels[i]}', color='b')
                    axes[i, j].set_xlabel(labels[i])
                    axes[i, j].set_ylabel('Density')
                    axes[i, j].set_title(f'KDE Plot: {labels[i]}', y=1.02)  # Shift title upward
                    axes[i, j].legend()
                    sns.despine(ax=axes[i, j])  # Remove top and right spines
                else:
                    # Scatter plots for different pairs of PCA components
                    ax = axes[i, j]
                    for label in np.unique(y):
                        mask = (y == label)
                        ax.scatter(components[i][mask], components[j][mask], label=f'Class {label}', alpha=0.7)

                    ax.set_xlabel(labels[i])
                    ax.set_ylabel(labels[j])
                    ax.set_title(f'{labels[i]} vs {labels[j]}')
                    ax.legend()

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.subplots_adjust(hspace=0.5)  # Adjust spacing between subplots
        plt.show()

def PCAscatter(components,labels,y):
        # Scatter plot for xPCA, yPCA, and zPCA
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        xPCA = components[0]
        yPCA = components[1]
        zPCA = components[2]

        for label in np.unique(y):
            mask = (y == label)
            ax.scatter(xPCA[mask], yPCA[mask], zPCA[mask], label=f'Class {label}', alpha=0.7)

        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])
        ax.set_title('PCA Scatter Plot')
        ax.legend()
        plt.show()

def explainedVariance(expVar, cumExpVar):
        # Plot the explained variance (Scree Plot) of PCA
        plt.figure(figsize=(8, 6))
        plt.plot(np.arange(1, len(expVar) + 1), cumExpVar, marker='o')
        plt.xlabel('Number of Principal Components')
        plt.ylabel('Cumulative Explained Variance')
        plt.title('Explained Variance Plot')
        plt.grid(True)
        plt.show()

def get_scat_ratio(X, y, method):
    # Calculate within-class scatter Sw and between-class scatter Sb
    X_ld = method(X, y)
    Xbar = np.mean(X_ld, axis=0).reshape(-1, 1)
    Xbar_k = [np.mean(X_ld[y == i], axis=0) for i in np.unique(y)]
    Sw = np.zeros((X_ld.shape[1], X_ld.shape[1]))
    Sb = np.zeros((X_ld.shape[1], X_ld.shape[1]))
    for i in range(len(np.unique(y))):
        Xsi = X_ld[y == i]
        Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
        Bi = Xsi.shape[0] * (Xbar_k[i] - Xbar) @ (Xbar_k[i] - Xbar).T
        Sw += Si
        Sb += Bi

    # Calculate scatter ratio
    eigVals_Sw, _ = np.linalg.eig(Sw)
    eigVals_Sb, _ = np.linalg.eig(Sb)
    ratio = np.sum(eigVals_Sb) / np.sum(eigVals_Sw)

    return Sw, Sb, ratio

def visualize_FLD(X, y):
    xFLD = X

    if xFLD.shape[1] == 1:
        # 1D FLD
        plt.scatter(xFLD, np.zeros_like(xFLD), c=y, cmap='rainbow')
        plt.xlabel('FLD Component')
    elif xFLD.shape[1] == 2:
        # 2D FLD
        plt.scatter(xFLD[:, 0], xFLD[:, 1], c=y, cmap='rainbow')
        plt.xlabel('FLD Component 1')
        plt.ylabel('FLD Component 2')
    else:
        # For more than 2 FLD components, use PCA for further reduction
        from sklearn.decomposition import PCA

        pca = PCA(n_components=2)
        xFLD_reduced = pca.fit_transform(xFLD)

        plt.scatter(xFLD_reduced[:, 0], xFLD_reduced[:, 1], c=y, cmap='rainbow')
        plt.xlabel('FLD Component 1 (PCA)')
        plt.ylabel('FLD Component 2 (PCA)')

    plt.title('FLD Scatter Plot')
    plt.colorbar(label='Class Label')
    plt.show()

def visualize_MDA(X, y, variable_names):
    xMDA = X

    if xMDA.shape[1] == 2:
        # 2D MDA
        plt.scatter(xMDA[:, 0], xMDA[:, 1], c=y, cmap='rainbow')
        plt.xlabel(f'MDA Component 1 ({variable_names[0]})')
        plt.ylabel(f'MDA Component 2 ({variable_names[1]})')
        plt.title('MDA Scatter Plot (2D)')
        plt.show()

    elif xMDA.shape[1] == 3:
        # 3D MDA
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(xMDA[:, 0], xMDA[:, 1], xMDA[:, 2], c=y, cmap='rainbow')
        ax.set_xlabel(f'MDA Component 1 ({variable_names[0]})')
        ax.set_ylabel(f'MDA Component 2 ({variable_names[1]})')
        ax.set_zlabel(f'MDA Component 3 ({variable_names[2]})')
        ax.set_title('MDA Scatter Plot (3D)')
        plt.colorbar(scatter, label='Class Label')
        plt.show()

    else:
        # More than 3 MDA components, use scikit-learn's PCA for further reduction
        from sklearn.decomposition import PCA
        pca = PCA(n_components=3)
        xMDA_reduced = pca.fit_transform(xMDA)

        fig = plt.figure()
        ax = fig.add_subplot(121, projection='3d')
        scatter = ax.scatter(xMDA[:, 0], xMDA[:, 1], xMDA[:, 2], c=y, cmap='rainbow')
        ax.set_xlabel(f'MDA Component 1 ({variable_names[0]})')
        ax.set_ylabel(f'MDA Component 2 ({variable_names[1]})')
        ax.set_zlabel(f'MDA Component 3 ({variable_names[2]})')
        ax.set_title('MDA Scatter Plot (First 3 Components)')
        plt.colorbar(scatter, label='Class Label')

        ax = fig.add_subplot(122)
        scatter = ax.scatter(xMDA_reduced[:, 0], xMDA_reduced[:, 1], c=y, cmap='rainbow')
        ax.set_xlabel('PCA Component 1')
        ax.set_ylabel('PCA Component 2')
        ax.set_title('PCA Scatter Plot (2D)')
        plt.colorbar(scatter, label='Class Label')

        plt.tight_layout()
        plt.show()

def queryDB():
    oConn = psy.connect("dbname = USA user=postgres password=LIJq3hqw%!-jc58d(.")
    oCur = oConn.cursor()

    query = '''
        select "am_m_age36", "am_prenatal", "am_gestation", "am_birthweight", "in_married"
        from "USA"."natalityConf"
        where "in_married" not in ('8', '9') and "am_gestation" not in ('00', '99') and "am_birthweight" <> '9999' and "am_prenatal" not in ('&', '-')
        order by random()
        limit 1000;
    '''

    oCur.execute(query)
    results = np.array(oCur.fetchall())

    oCur.close()
    oConn.close()

    return results.astype(int)

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

def stdPCA(X):
    #Performs PCA on standardized data
    #we find Xbar and extract values of dimensions from X
    #also provides the necessary data for a Scree plot
    Xbar = X - np.mean(X,0) / X.std(axis=0)

    #we find the scatter matrix, SUM_[k=1]^n (x_k - m)^T(x_k - m)
    scatterX = np.dot(Xbar.T, Xbar) / (Xbar.shape[0] - 1)

    #find between-scatter
    eigVals, eigVecs = np.linalg.eigh(scatterX)
    eigVals = np.real(eigVals)
    eigVecs = np.real(eigVecs)

    #finding the explained variance data to plot to create Scree plot
    explainedVar = eigVals / np.sum(eigVals)
    cumulativeExpVar = np.cumsum(explainedVar)

    #project X onto 3-dimensions
    x = X @ eigVecs[:,-1]
    y = X @ eigVecs[:,-2]
    z = X @ eigVecs[:,-3]
    
    #return the projection of X onto 3-D
    return x, y, z, explainedVar, cumulativeExpVar

def FLD(X, y):
    # determines number of classes and components to put put into the projection matrix
    c = len(np.unique(y))
    numComponents = min(c - 1, X.shape[1])
    #calculate overall mean and class means
    Xbar = np.mean(X, axis = 0).reshape(-1,1)
    Xbar_k = [np.mean(X[y == i], axis=0) for i in np.unique(y)]
    Sw = np.zeros((X.shape[1],X.shape[1]))
    Sb = np.zeros((X.shape[1],X.shape[1]))
    #calculating within-class scatter matrix Sw and between-class scatter matrix Sb
    for i in range(c):
        Xsi = X[y == i]
        Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
        Bi = Xsi.shape[0] * (Xbar_k[i] - Xbar) @ (Xbar_k[i] -Xbar).T
        Sw += Si
        Sb += Bi
    #getting the ordered eigenvalues and eigenvectors by solving 
    # Sw^{-1}Sbw=lambda*w; note, Sw must be non-singular
    eigVals, eigVecs = la.eig(np.dot(la.inv(Sw), Sb))
    eigVals = np.real(eigVals)
    eigVecs = np.real(eigVecs)
    idx = eigVals.argsort()[::-1]   
    eigVals = eigVals[idx]
    eigVecs = eigVecs[:,idx]

    W = eigVecs[:, :numComponents]
    return X @ W

def MDA(X,y):
    # calculating number of classes, number of c
    c = len(np.unique(y))
    numComponents = min(c - 1, X.shape[1])
    #calculate overall mean and class means
    Xbar = np.mean(X,0).reshape(-1,1)
    Xbar_k = [np.mean(X[y == i]) for i in np.unique(y)]
    #finding within-class scatter, Sw=SUM_{i=1}^c SUM_{x IN D_i} (x - m_i)(x - m_i)^T and
    #finding between-class scatter, Sb=SUM_{i=1}^c n_i(m_i - m)(m_i - m)^T
    Sw = np.zeros((X.shape[1],X.shape[1]))
    Sb = np.zeros((X.shape[1],X.shape[1]))
    for i in range(c):
        Xsi = X[y == i]
        Si = (Xsi - Xbar_k[i]).T @ (Xsi - Xbar_k[i])
        Bi = Xsi.shape[0] * (Xbar_k[i] - Xbar) @ (Xbar_k[i] - Xbar).T
        Sw += Si        
        Sb += Bi
    #solving Sw^-1Sbw_i=lambda_iSww_i for the eigenvalues and eigenvectors
    eigVals, eigVecs = la.eig(la.inv(Sw) @ Sb)
    eigVals = np.real(eigVals)
    eigVecs = np.real(eigVecs)
    #sorting the e-values and e-vectors
    idx = eigVals.argsort()[::-1]   
    eigVals = eigVals[idx]
    eigVecs = eigVecs[:,idx]

    #building the projection matrix W
    W = eigVecs[:, :numComponents]

    projX = X @ W
    return X

if __name__ == "__main__":
    main()  