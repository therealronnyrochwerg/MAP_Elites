from scipy.spatial import distance as dist
from numpy.random import default_rng
from numpy.linalg import matrix_rank, norm
import numpy as np
import timeit

# function to create a matrix of centroids
def create_centroids(num, dim, seed = None):
    ind_vec = lin_independent_vectors(num, dim, seed=seed)
    return gram_schmidt(ind_vec)

# generates linearly independent vectors and returns them in a matrix that is mxn
# this gives n vectors of dimension m
# for CVT-Elites, this would give m niches, and n would be the number of samples (error vector length)
def lin_independent_vectors(m,n, seed = None):
    rng = default_rng(seed = seed)

    vectors = rng.random((m, n))
    rank = matrix_rank(vectors)

    while rank < n:
        M = rng.random((m, n))
        rank = matrix_rank(M)

    return vectors


def gram_schmidt(A):
    """Orthogonalize a set of vectors stored as the columns of matrix A."""
    # Get the number of vectors.
    A = A.copy()
    n = A.shape[1]
    for j in range(n):
        # To orthogonalize the vector in column j with respect to the
        # previous vectors, subtract from it its projection onto
        # each of the previous vectors.
        for k in range(j):
            A[:, j] -= np.dot(A[:, k], A[:, j]) * A[:, k]

        A[:, j] = A[:, j] / norm(A[:, j])
    return A

# finds teh closest centroid to a vector using cosine distance
def closest_centroid(centroids, vector):
    vector = np.array([vector])
    distances = dist.cdist(centroids, vector, 'cosine')

    return np.argmin(distances)

#above is faster, keeping this just in case (above calcs distance into a 2d ndarray)
# def closest_centroid2(centroids, vector):
#     distances = np.dot(centroids,vector)/(norm(centroids, axis=1)*norm(vector))
#
#     return np.argmax(distances)

# shifts a centroid when a vector is added to a niche. centroid should be the chosen centroid, not all of them
# The shift is the vector between the two, can add weights later if needed (shift closer to centroid for example)
def shift_centroid(centroid, vector):
    centroid_unit = centroid / norm(centroid)
    vector_unit = vector / norm(vector)

    print(centroid_unit)
    print(vector_unit)
    return  centroid_unit + vector_unit

if __name__ == '__main__':
    testy = np.array([[1, 2, 3, 4], [-1, -2, -3, -4], [-4, -3, 2, 1]])

    test2 = np.array([1,2,3,4])

    testy = np.array([1,1])
    test2 = np.array([-1,1])

    print(shift_centroid(testy, test2))


