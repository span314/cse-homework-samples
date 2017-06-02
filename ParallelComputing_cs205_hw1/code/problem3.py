#!/usr/bin/python
from __future__ import print_function
import numpy as np
import time

import pyximport
pyximport.install()

import listsum

#TESTS
np.random.seed(0)
n = 100
testarray = np.random.randint(10, size=n, dtype=np.int32)
sums = listsum.sum_serial(testarray)
sump = listsum.sum_parallel(testarray)
sumnp = np.sum(testarray)
assert sums == sumnp
assert sump == sumnp

testmatrix = np.random.randint(10, size=(n, n), dtype=np.int32)
testresultserial = np.zeros(n, dtype=np.int32)
testresultparallel = np.zeros(n, dtype=np.int32)
listsum.matrix_vector_serial(testmatrix, testarray, testresultserial)
listsum.matrix_vector_parallel(testmatrix, testarray, testresultparallel)
testresultsnp = np.dot(testmatrix, testarray)
assert np.array_equal(testresultsnp, testresultserial)
assert np.array_equal(testresultsnp, testresultparallel)
print("Tests Passed")

#helper class for timing
class Timer(object):
    def __init__(self):
        self.times = []

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.times.append(time.time() - self.start_time)


#Summation

#problem sizes 2^N
problem_sizes = [6, 10, 20, 24, 28, 32]


serial_timer = Timer()
parallel_timer = Timer()
for logn in problem_sizes:
    n = 2**logn
    testarray = np.ones(n, dtype=np.int32)
    #serial code
    serial_timer.start()
    print(listsum.sum_serial(testarray))
    serial_timer.stop()
    #parallel code
    parallel_timer.start()
    print(listsum.sum_parallel(testarray))
    parallel_timer.stop()


print("Problem Sizes")
print(problem_sizes)
print("Serial Addition Times")
print(serial_timer.times)
print("Parallel Addition Times")
print(parallel_timer.times)
print("Serial / Parallel")
print([serial_timer.times[i] / parallel_timer.times[i] for i in range(len(serial_timer.times))])


#Matrix vector multiplication

#vector sizes 2^N
vector_sizes = [6, 10, 12, 14, 16]

serial_timer = Timer()
parallel_timer = Timer()
for logn in vector_sizes:
    n = 2**logn
    testmatrix = np.ones((n, n), dtype=np.int32)
    testarray = np.ones(n, dtype=np.int32)
    testresultserial = np.zeros(n, dtype=np.int32)
    testresultparallel = np.zeros(n, dtype=np.int32)
    #serial code
    serial_timer.start()
    listsum.matrix_vector_serial(testmatrix, testarray, testresultserial)
    serial_timer.stop()
    print(testresultserial)
    #parallel code
    parallel_timer.start()
    listsum.matrix_vector_parallel(testmatrix, testarray, testresultparallel)
    parallel_timer.stop()
    print(testresultparallel)

print("Vector Sizes")
print(vector_sizes)
print("Serial MV-Mult Times")
print(serial_timer.times)
print("Parallel MV-Mult Times")
print(parallel_timer.times)
print("Serial / Parallel")
print([serial_timer.times[i] / parallel_timer.times[i] for i in range(len(serial_timer.times))])