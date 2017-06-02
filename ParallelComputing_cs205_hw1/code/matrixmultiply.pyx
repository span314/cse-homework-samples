from __future__ import division
from cython cimport boundscheck, wraparound
from cython.parallel import prange
import numpy as np
cimport numpy as np

#serial matrix multiplication
#inputs: matrix, vector, and result (0-initialized array to store output)
@boundscheck(False)
@wraparound(False)
cpdef int matrix_multiply_serial(np.float64_t[:,:] A, np.float64_t[:,:] B, np.float64_t[:,:] C) nogil:
    cdef:
        long long i, j, k
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return 0

#parallel matrix multiplication
#inputs: matrix, vector, and result (0-initialized array to store output)
@boundscheck(False)
@wraparound(False)
cpdef int matrix_multiply_parallel(np.float64_t[:,:] A, np.float64_t[:,:] B, np.float64_t[:,:] C) nogil:
    cdef:
        long long i, j, k
    for i in prange(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return 0


#parallel block-based matrix multiplication for square matrices
#inputs: matrix, vector, and result (0-initialized array to store output)
@boundscheck(False)
@wraparound(False)
cpdef int matrix_multiply_block(np.float64_t[:,:] A, np.float64_t[:,:] B, np.float64_t[:,:] C) nogil:
    cdef:
        long long n, b, blocks, ib, jb, kb, i, j, k, istart, istop, jstart, jstop, kstart, kstop
    n = A.shape[0]
    b = 256 #block size
    blocks = (n - 1) // b + 1 #ceiling of n/b
    for ib in range(blocks):
        istart = ib * b
        istop = min(istart + b, n) #check for partial blocks
        for jb in range(blocks):
            jstart = jb * b
            jstop = min(jstart + b, n)
            for kb in range(blocks):
                kstart = kb * b
                kstop = min(kstart + b, n)
                #standard parallel multiply for each block
                for i in prange(istart, istop):
                    for j in range(jstart, jstop):
                        for k in range(kstart, kstop):
                            C[i, j] += A[i, k] * B[k, j]
    return 0

def matrix_multiply_strassen(A, B):
    n = A.shape[0]
    n2 = n // 2
    #do parallel multiply for chunks smaller than cache size
    if A.shape[0] <= 64:
        C = np.zeros((n, n))
        matrix_multiply_parallel(A, B, C)
        return C

    A11 = A[:n2, :n2]
    A12 = A[:n2, n2:]
    A21 = A[n2:, :n2]
    A22 = A[n2:, n2:]

    B11 = B[:n2, :n2]
    B12 = B[:n2, n2:]
    B21 = B[n2:, :n2]
    B22 = B[n2:, n2:]

    M1 = matrix_multiply_strassen((A11 + A22), (B11 + B22))
    M2 = matrix_multiply_strassen((A21 + A22), B11)
    M3 = matrix_multiply_strassen(A11, (B12 - B22))
    M4 = matrix_multiply_strassen(A22, (B21 - B11))
    M5 = matrix_multiply_strassen((A11 + A12), B22)
    M6 = matrix_multiply_strassen((A21 - A11), (B11 + B12))
    M7 = matrix_multiply_strassen((A12 - A22), (B21 + B22))

    C = np.empty((n, n))
    C[:n2, :n2] = M1 + M4 - M5 + M7
    C[:n2, n2:] = M3 + M5
    C[n2:, :n2] = M2 + M4
    C[n2:, n2:] = M1 - M2 + M3 + M6

    return C