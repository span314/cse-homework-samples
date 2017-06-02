#!/usr/bin/python
#####################
# CS 181, Spring 2016
# Homework 2, Problem 1
# Shawn Pan
##################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

#Part 1
D = np.array([0] + [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0], dtype=np.float) #add 0 initial counts to see priors
n = np.arange(len(D))
n1 = np.cumsum(D)
n0 = n - n1

print "D", D
print "n0", n0
print "n1", n1

theta_mle = n1 / (n0 + n1)
theta_map = (3 + n1) / (4 + n0 + n1)
ppd = (4 + n1) / (6 + n0 + n1)

plt.figure()
plt.plot(n, theta_mle, label="MLE")
plt.plot(n, theta_map, label="MAP")
plt.plot(n, ppd, label="PPD")
plt.title("Estimates")
plt.xlabel("Sample Number")
plt.ylabel("Theta")
plt.legend(loc="lower right")
plt.savefig("problem1part1")

#Part 2
prange = np.linspace(0, 1, 101)
plt.figure()
for i in range(0, len(n0), 4):
  plt.plot(prange, beta.pdf(prange, 4 + n1[i], 2 + n0[i]), label=str(i) + " Samples")
plt.legend(loc="upper left")
plt.title("Posterior Distribution")
plt.xlabel("Theta")
plt.ylabel("PDF")
plt.savefig("problem1part2")