#!/usr/bin/python
from __future__ import print_function
import numpy as np

from numpy import array
from scipy.linalg.blas import dgemm
import time

import pyximport
pyximport.install()

import matrixmultiply

#TESTS
np.random.seed(0)
#non-square matrix (only for serial)
A = np.random.random(size=(8, 20))
B = np.random.random(size=(20, 5))
prod_np = np.dot(A, B)
prod_dgemm = dgemm(1.0, A, B)
prod_serial = np.zeros((8, 5), dtype=np.float64)
matrixmultiply.matrix_multiply_serial(A, B, prod_serial)
assert np.allclose(prod_np, prod_dgemm)
assert np.allclose(prod_np, prod_serial)
#square matrix
A = np.random.random(size=(8, 8))
B = np.random.random(size=(8, 8))
prod_np = np.dot(A, B)
prod_dgemm = dgemm(1.0, A, B)
prod_serial = np.zeros((8, 8), dtype=np.float64)
prod_parallel = np.zeros((8, 8), dtype=np.float64)
prod_block = np.zeros((8, 8), dtype=np.float64)
matrixmultiply.matrix_multiply_serial(A, B, prod_serial)
matrixmultiply.matrix_multiply_parallel(A, B, prod_parallel)
matrixmultiply.matrix_multiply_block(A, B, prod_block)
prod_strassen = matrixmultiply.matrix_multiply_strassen(A, B)
assert np.allclose(prod_np, prod_dgemm)
assert np.allclose(prod_np, prod_serial)
assert np.allclose(prod_np, prod_parallel)
assert np.allclose(prod_np, prod_block)
assert np.allclose(prod_np, prod_strassen)
#larger square matrix
A = np.random.random(size=(256, 256))
B = np.random.random(size=(256, 256))
prod_np = np.dot(A, B)
prod_dgemm = dgemm(1.0, A, B)
prod_serial = np.zeros((256, 256), dtype=np.float64)
prod_parallel = np.zeros((256, 256), dtype=np.float64)
prod_block = np.zeros((256, 256), dtype=np.float64)
matrixmultiply.matrix_multiply_serial(A, B, prod_serial)
matrixmultiply.matrix_multiply_parallel(A, B, prod_parallel)
matrixmultiply.matrix_multiply_block(A, B, prod_block)
prod_strassen = matrixmultiply.matrix_multiply_strassen(A, B)
assert np.allclose(prod_np, prod_dgemm)
assert np.allclose(prod_np, prod_serial)
assert np.allclose(prod_np, prod_parallel)
assert np.allclose(prod_np, prod_block)
assert np.allclose(prod_np, prod_strassen)
print("Tests Passed")

#helper class for timing
class Timer(object):
    def __init__(self):
        self.times = []

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.times.append(time.time() - self.start_time)


#Matrix matrix multiplication

#vector sizes 2^N
vector_sizes = [6, 8, 10]

blas_timer = Timer()
serial_timer = Timer()
parallel_timer = Timer()
block_timer = Timer()
strassen_timer = Timer()
for logn in vector_sizes:
    n = 2**logn
    A = np.ones((n, n), dtype=np.float64)
    #blas dgemm
    blas_timer.start()
    dgemm(1, A, A)
    blas_timer.stop()
    #serial code
    prod = np.zeros((n, n), dtype=np.float64)
    serial_timer.start()
    matrixmultiply.matrix_multiply_serial(A, A, prod)
    serial_timer.stop()
    #parallel code
    prod = np.zeros((n, n), dtype=np.float64)
    parallel_timer.start()
    matrixmultiply.matrix_multiply_parallel(A, A, prod)
    parallel_timer.stop()
    #block parallel code
    prod = np.zeros((n, n), dtype=np.float64)
    block_timer.start()
    matrixmultiply.matrix_multiply_block(A, A, prod)
    block_timer.stop()
    #strassen code
    strassen_timer.start()
    matrixmultiply.matrix_multiply_strassen(A, A)
    strassen_timer.stop()


print("Vector Sizes")
print(vector_sizes)
print("BLAS dgemm")
print(blas_timer.times)
print("Serial Mult Times")
print(serial_timer.times)
print("Parallel Mult Times")
print(parallel_timer.times)
print("Block Mult Times")
print(block_timer.times)
print("Strassen Mult Times")
print(strassen_timer.times)
print("Serial / BLAS dgemm")
print([serial_timer.times[i] / blas_timer.times[i] for i in range(len(serial_timer.times))])
print("Serial / Parallel")
print([serial_timer.times[i] / parallel_timer.times[i] for i in range(len(serial_timer.times))])
print("Serial / Block")
print([serial_timer.times[i] / block_timer.times[i] for i in range(len(serial_timer.times))])
print("Serial / Strassen")
print([serial_timer.times[i] / strassen_timer.times[i] for i in range(len(serial_timer.times))])