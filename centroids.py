from scipy.spatial import distance as dist
from numpy.random import default_rng
from numpy.linalg import matrix_rank, norm
import numpy as np


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

def closest_centroid(centroids, vector):
    pass


if __name__ == '__main__':
    # lin_ind = lin_independent_vectors(10,5, seed=1)
    # print((lin_ind[:,1] - (dot(lin_ind[:,0], lin_ind[:,1]) * lin_ind[:, 0])),
    #       '\n')
    # orth = gram_schmidt(lin_ind)
    # for i in range(orth.shape[1]):
    #     for y in range(i, orth.shape[1]):
    #         print(1 - dist.cosine(orth[:,i],orth[:,y]), '\n')
    # print()
    #
    # print(lin_ind, '\n')
    # print(orth)
    testy = [[1,2,3,4],[-1,-2,-3,-4],[-4,-3,2,1]]
    print(type(testy))
    testy = np.array([[1, 2, 3, 4], [-1, -2, -3, -4], [-4, -3, 2, 1]])
    print(type(testy))
    testy2 = np.array([[1,2,3,4]])
    print(dist.cdist(testy2,testy,'cosine'))

