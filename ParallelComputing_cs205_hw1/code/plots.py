#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

n_add = np.array([6, 10, 20, 24, 28, 32])
serial_add = np.array([4.076957702636719e-05, 1.4066696166992188e-05, 0.0010504722595214844, 0.017465829849243164, 0.27647829055786133, 4.418492317199707])
parallel_add = np.array([0.0003554821014404297, 6.365776062011719e-05, 0.0004951953887939453, 0.0066759586334228516, 0.10785222053527832, 1.7580146789550781])

plt.figure()
plt.plot(n_add, np.log10(serial_add), label="serial", marker="o")
plt.plot(n_add, np.log10(parallel_add), label="8 cores", marker="o")
plt.title("Cost Optimal Summation Time")
plt.xlabel("log2 n")
plt.ylabel("log10 time (s)")
plt.legend(loc="upper left")
plt.savefig("problem3add")

plt.figure()
plt.plot(n_add, serial_add / (8 * parallel_add), marker="o")
plt.title("Cost Optimal Summation Efficiency")
plt.xlabel("log2 n")
plt.ylabel("serial / (8 * parallel)")
plt.savefig("problem3addeff")


n_mv = np.array([6, 10, 12, 14, 16])
serial_mv = np.array([5.316734313964844e-05, 0.0018541812896728516, 0.0303041934967041, 0.483656644821167, 7.878865718841553])
parallel_mv = np.array([0.002688169479370117, 0.003236055374145508, 0.009030580520629883, 0.11242151260375977, 1.9520986080169678])

plt.figure()
plt.plot(n_mv, np.log10(serial_mv), label="serial", marker="o")
plt.plot(n_mv, np.log10(parallel_mv), label="8 cores", marker="o")
plt.title("Cost Optimal Matrix-Vector Multiplication")
plt.xlabel("log2 n")
plt.ylabel("log10 time (s)")
plt.legend(loc="upper left")
plt.savefig("problem3mv")

plt.figure()
plt.plot(n_mv, serial_mv / (8 * parallel_mv), marker="o")
plt.title("Cost Optimal Matrix-Vector Efficiency")
plt.xlabel("log2 n")
plt.ylabel("serial / (8 * parallel)")
plt.savefig("problem3mveff")


n_mm = np.array([6, 8, 10, 12])
n_mm2 = np.array([6, 8, 10, 12, 14])
serial_mm = np.array([0.0013585090637207031, 0.18106603622436523, 23.08880877494812, 8836.867682933807])
parallel_mm = np.array([0.0023436546325683594, 0.004044771194458008, 1.0069470405578613, 414.743891954422])
block_mm = np.array([0.0003314018249511719, 0.005831241607666016, 0.19164657592773438, 65.37864255905151, 6109.13455080986])
strassen_mm = np.array([0.0003199577331542969, 0.02479863166809082, 0.9015884399414062, 43.84881019592285, 2080.7139427661896])
blas_mm = np.array([0.00046563148498535156, 0.012619495391845703, 0.6524622440338135, 38.924904584884644, 1665.1936280727386])

plt.figure()
plt.plot(n_mm, np.log10(serial_mm), label="serial", marker="o")
plt.plot(n_mm, np.log10(parallel_mm), label="parallel", marker="o")
plt.plot(n_mm2, np.log10(block_mm), label="parallel+block", marker="o")
plt.plot(n_mm2, np.log10(strassen_mm), label="parallel+strassen", marker="o")
plt.plot(n_mm2, np.log10(blas_mm), label="blas dgemm", marker="o")
plt.title("Matrix-Matrix Multiplication")
plt.xlabel("log2 n")
plt.ylabel("log10 time (s)")
plt.legend(loc="upper left")
plt.savefig("problem4")

gflop = 2*8**n_mm / 1e9
gflop2 = 2*8**n_mm2 / 1e9
plt.figure()
plt.plot(n_mm, gflop / serial_mm, label="serial", marker="o")
plt.plot(n_mm, gflop / parallel_mm, label="parallel", marker="o")
plt.plot(n_mm2, gflop2 / block_mm, label="parallel+block", marker="o")
plt.plot(n_mm2, gflop2 / strassen_mm, label="parallel+strassen", marker="o")
plt.plot(n_mm2, gflop2 / blas_mm, label="blas dgemm", marker="o")
plt.title("Matrix-Matrix Multiplication")
plt.xlabel("log2 n")
plt.ylabel("GFlop/s")
plt.legend(loc="upper left")
plt.savefig("problem4gflop")
