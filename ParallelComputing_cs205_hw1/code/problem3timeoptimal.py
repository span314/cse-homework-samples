#!/usr/bin/python
from __future__ import print_function
import numpy as np
import time

import pyximport
pyximport.install()

import fastsum

#helper class for timing
class Timer(object):
    def __init__(self):
        self.times = []

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.times.append(time.time() - self.start_time)

#TESTS
#summation
a = np.arange(16, dtype=np.int32)
print(a)
sum_serial = fastsum.sum_serial(a)
sum_parallel = fastsum.sum_timeopt(a)
print(a)
assert sum_serial == sum_parallel
#matrix vec
np.random.seed(0)
rows = 100
cols = 16
testarray = np.random.randint(10, size=cols, dtype=np.int32)
testmatrix = np.random.randint(10, size=(rows, cols), dtype=np.int32)
testresultserial = np.zeros(rows, dtype=np.int32)
testresultparallel = np.zeros(rows, dtype=np.int32)
fastsum.matrix_vector_serial(testmatrix, testarray, testresultserial)
fastsum.matrix_vector_timeopt(testmatrix, testarray, testresultparallel)
testresultsnp = np.dot(testmatrix, testarray)
print(testresultparallel)

assert np.array_equal(testresultsnp, testresultserial)
assert np.array_equal(testresultsnp, testresultparallel)
print("Tests Passed")


#Matrix vector multiplication
timer = Timer()
rows = 1000000
cols = 16
testarray = np.random.randint(10, size=cols, dtype=np.int32)
testmatrix = np.random.randint(10, size=(rows, cols), dtype=np.int32)
testresultserial = np.zeros(rows, dtype=np.int32)
testresultparallel = np.zeros(rows, dtype=np.int32)
timer.start()
fastsum.matrix_vector_serial(testmatrix, testarray, testresultserial)
timer.stop()
timer.start()
fastsum.matrix_vector_timeopt(testmatrix, testarray, testresultparallel)
timer.stop()
print(timer.times)