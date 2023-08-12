import numpy as np
import matplotlib.pyplot as plt

random_seed = np.random.randint(0, 99999999)
np.random.seed(random_seed)
# np.random.seed(26938635)
print("Random Seed:", random_seed)

def generate_random_sphere_points(num_points, radius):
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    phi = np.random.uniform(0, np.pi, num_points)
    random_radii = radius * (np.random.uniform(0, 1, num_points))**(1/3)
    x = random_radii * np.sin(phi) * np.cos(theta)
    y = random_radii * np.sin(phi) * np.sin(theta)
    z = random_radii * np.cos(phi)
    return x, y, z

def get_rand_ball(radius, points, max_center):
    center = np.random.uniform(-max_center, max_center, 3)
    sphere_points = generate_random_sphere_points(points, radius)
    sphere_points += center[:, np.newaxis]
    return sphere_points


def get_eig(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    # Sort eigenvalues and corresponding eigenvectors in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    return sorted_eigenvectors, sorted_eigenvalues

def main():
    num_spheres = 4
    num_points_per_sphere = 25
    max_center = 5
    max_radius = 0.5

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sphere_points = {}
    for i in range(num_spheres):
        sphere_points[i] = get_rand_ball(
            max_radius,
            np.random.randint(num_points_per_sphere - 5, num_points_per_sphere + 5),
            max_center
        )

    m_i = []
    S_i = []
    for i in range(num_spheres):
        m_i.append(np.mean(sphere_points[i], axis=1))
        x_minus_m_i = sphere_points[0] - m_i[0][:, np.newaxis]
        # print("x_minus_m_i = " + str(x_minus_m_i))
        S_i.append(x_minus_m_i @ x_minus_m_i.T)
    Sw = np.zeros(np.shape(S_i[0]))
    for i in S_i:
        Sw += i
    print("Sw = " + str(Sw))
    Sw_det = np.linalg.det(Sw)
    if (abs(Sw_det) > 0.001):
        print("Sw is non-singular. Its det is %.3f" % (Sw_det))

    # Mean of all data across all classes
    m = []
    for i in range(len(sphere_points[0])):
        m.append(np.mean(
            np.concatenate([matrix[i] for matrix in sphere_points.values()])
        ))
    print("The mean of all data is " + str(m))
    print("The means of each class are " + str(m_i))
    SB = np.zeros(np.shape(S_i[0]))
    for i in range(len(sphere_points)):
        n_i = len(sphere_points[i][0])
        m_i_minus_m = np.array(m_i[i])[None, :] - np.array(m)[None, :]
        SB += n_i * (m_i_minus_m.T @ m_i_minus_m)
    print("SB = " + str(SB))

    Sw1SB = np.linalg.inv(Sw) @ SB
    eVec, eVal = get_eig(Sw1SB)

    # Plot Linear Discriminant
    c = ['r', 'g', 'b']
    mm = np.mean(m_i, axis=0)
    for i in range(len(eVec)-1):
        prin_eVec = eVec[:, i]
        t = np.linspace(-max_center, max_center, 100)
        x_points = mm[0] + t * prin_eVec[0]
        y_points = mm[1] + t * prin_eVec[1]
        z_points = mm[2] + t * prin_eVec[2]
        ax.plot(x_points, y_points, z_points, c=c[i])

    dist = []
    for i in range(len(m_i)):
        prin_eVec = eVec[:, 0]
        m_proj = np.dot(m_i[i] - m, prin_eVec) * prin_eVec + m
        distance = np.linalg.norm(m_i[i] - m_proj)
        dist.append(distance)
        print("m_%d is %.2f distance from PC1" % (i, distance))
        ax.plot([m_i[i][0], m_proj[0]], [m_i[i][1], m_proj[1]], [m_i[i][2], m_proj[2]], c='g')

    # # Other code
    # class1_data = np.array(sphere_points[0]).T
    # class2_data = np.array(sphere_points[1]).T
    # mean_class1 = np.mean(class1_data, axis=0)
    # mean_class2 = np.mean(class2_data, axis=0)
    # between_class_scatter = np.outer(mean_class1 - mean_class2, mean_class1 - mean_class2)
    # within_class_scatter_class1 = np.cov(class1_data, rowvar=False)
    # within_class_scatter_class2 = np.cov(class2_data, rowvar=False)
    # within_class_scatter = within_class_scatter_class1 + within_class_scatter_class2
    # eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(within_class_scatter) @ between_class_scatter)
    # principal_component = eigenvectors[:, np.argmax(eigenvalues)]
    # # prin_eVec = eVec[:, i]
    # t = np.linspace(-max_center, max_center, 100)
    # x_points = mm[0] + t * principal_component[0]
    # y_points = mm[1] + t * principal_component[1]
    # z_points = mm[2] + t * principal_component[2]
    # ax.plot(x_points, y_points, z_points, c='orange')

    print("Seed " + str(random_seed) + " gave dist " + str(dist))
    for i in range(num_spheres):
        ax.scatter(sphere_points[i][0], sphere_points[i][1], sphere_points[i][2], marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

if __name__ == "__main__":
    main()
