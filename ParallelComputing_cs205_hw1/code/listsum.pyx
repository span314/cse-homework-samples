from cython cimport boundscheck, wraparound
from cython.parallel import prange
import numpy as np
cimport numpy as np

#serial summation (adapted from example from install check)
@boundscheck(False)
@wraparound(False)
cpdef long long sum_serial(np.int32_t[:] arr) nogil:
    cdef:
        long long i, total
    total = 0
    for i in range(arr.shape[0]):
        total += arr[i]
    return total

#parallel summation
@boundscheck(False)
@wraparound(False)
cpdef long long sum_parallel(np.int32_t[:] arr) nogil:
    cdef:
        long long i, total
    total = 0
    #guided seems to give the best performance
    for i in prange(arr.shape[0], schedule="guided"):
        total += arr[i]
    return total

#dot product
@boundscheck(False)
@wraparound(False)
cpdef long long dot(np.int32_t[:] a, np.int32_t[:] b) nogil:
    cdef:
        long long i, total
    total = 0
    for i in range(a.shape[0]):
        total += a[i] * b[i]
    return total

#serial matrix vector multiplication
#inputs: matrix, vector, and result (0-initialized array to store output)
@boundscheck(False)
@wraparound(False)
cpdef int matrix_vector_serial(np.int32_t[:,:] mat, np.int32_t[:] vec, np.int32_t[:] result) nogil:
    cdef:
        long long i, j
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            result[i] += mat[i, j] * vec[j]
    return 0

#parallel matrix vector multiplication
#inputs: matrix, vector, and result (0-initialized array to store output)
@boundscheck(False)
@wraparound(False)
cpdef int matrix_vector_parallel(np.int32_t[:,:] mat, np.int32_t[:] vec, np.int32_t[:] result) nogil:
    cdef:
        long long i, j
    for i in prange(mat.shape[0], schedule="guided"):
        for j in range(mat.shape[1]):
           result[i] += mat[i, j] * vec[j]
    return 0