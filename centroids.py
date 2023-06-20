from scipy.spatial import distance as dist
from numpy.linalg import matrix_rank, norm
import numpy as np
from numpy.random import default_rng

# function to create a matrix of centroids
def create_centroids(num_samples, num_niches, rng):
    ind_vec = lin_independent_vectors(num_samples, num_niches, rng)
    return gram_schmidt(ind_vec.T)

# generates linearly independent vectors and returns them in a matrix that is mxn
# this gives n vectors of dimension m
# for CVT-Elites, this would give m niches, and n would be the number of samples (error vector length)
def lin_independent_vectors(m,n, rng):
    # initializing it to nxm because of array inside array works in python (this gives n arrays of length m)
    vectors = rng.random((n, m))
    rank = matrix_rank(vectors)

    while rank < n:
        vectors = rng.random((n, m))
        rank = matrix_rank(vectors)


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

    return A.T

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

    return  centroid_unit + vector_unit

if __name__ == '__main__':
    rng = default_rng(seed=1)

    ind_vec = lin_independent_vectors(150,4,rng)


    orth2 = gram_schmidt(ind_vec.T)
    print(ind_vec.shape)
    print(orth2.shape)

    for i in range(orth2.shape[0]):
        for j in range(i + 1, orth2.shape[0]):
            print(i,j)
            print(np.dot(ind_vec[i], ind_vec[j]))
            print(np.dot(orth2[i], orth2[j]))



