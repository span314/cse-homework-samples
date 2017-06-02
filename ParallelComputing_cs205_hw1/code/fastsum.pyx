from cython cimport boundscheck, wraparound
from cython.parallel import prange, parallel, threadid
from openmp cimport omp_get_thread_num
from libc.stdlib cimport abort, malloc, free
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

#time optimal summation (log n) for 8 processors and array of size 16
#warning modifies input array
@boundscheck(False)
@wraparound(False)
cpdef int sum_timeopt(np.int32_t[::1] arr) nogil:
    cdef:
        int i, tid, start, next_add
        int n = arr.shape[0]
        #int s = 2
        #hack to make cython put the correct openmp directives, otherwise while loop hangs
        np.int32_t * a = &arr[0]

    with parallel(num_threads=8):
        #TODO figure out how to force cython to make s global, otherwise while loop over s hangs
        # for i in prange(0, 16, s, schedule="static"):
        #     tid = omp_get_thread_num()
        #     start = tid * s
        #     next_add = start + s / 2
        #     a[start] += a[next_add]

        for i in prange(0, n, 2, schedule="static"):
            tid = omp_get_thread_num()
            start = tid * 2
            next_add = start + 2 / 2
            a[start] += a[next_add]

        for i in prange(0, n, 4, schedule="static"):
            tid = omp_get_thread_num()
            start = tid * 4
            next_add = start + 4 / 2
            a[start] += a[next_add]

        for i in prange(0, n, 8, schedule="static"):
            tid = omp_get_thread_num()
            start = tid * 8
            next_add = start + 8 / 2
            a[start] += a[next_add]

        for i in prange(0, n, 16, schedule="static"):
            tid = omp_get_thread_num()
            start = tid * 16
            next_add = start + 16 / 2
            a[start] += a[next_add]
    return a[0]


#serial matrix vector multiplication
#inputs: matrix, vector, and result (0-initialized array to store output)
@boundscheck(False)
@wraparound(False)
cpdef int matrix_vector_serial(np.int32_t[:,:] mat, np.int32_t[:] vec, np.int32_t[:] result) nogil:
    cdef:
        int i, j
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            result[i] += mat[i, j] * vec[j]
    return 0

#parallel matrix vector multiplication
#inputs: matrix, vector, and result (0-initialized array to store output)
def matrix_vector_timeopt(mat, vec, result):
    for i in range(mat.shape[0]):
        prod = mat[i,:] * vec
        result[i] = sum_timeopt(prod)