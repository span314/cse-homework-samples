#!/usr/bin/python
#Shawn Pan
#CS222 HW2
import numpy as np

#fix pseudorandom seed
np.random.seed(0)

#ceiling log 2
log2 = lambda x: int(np.ceil(np.log(x) / np.log(2)))

#create data sets
datasets = []
nsim = 10
n = 10000
for i in xrange(nsim):
  data = np.random.randint(0, 2**30, n)
  data.sort()
  datasets.append(data)

#original scheme
for data in datasets:
  diff = data[1:] - data[:-1]
  k = log2(np.max(diff))
  print "bits used:", 30 + 5 + k * (n - 1), "k:", k

#mask scheme
m = 13
bins = 2**m
mask_right = (1 << (30 - m)) - 1
mask_left = ((1 << 30) - 1) ^ mask_right

for data in datasets:
  right = np.bitwise_and(data, mask_right)
  left = np.bitwise_and(data, mask_left) >> (30 - m)

  counts = np.zeros(bins)
  for i in left:
    counts[i] += 1
    min_count = np.min(counts)
  bits_per_bin = log2(np.max(counts))
  print np.sum(counts==0)
  print "bits used:", n * (30 - m) + bins * bits_per_bin, "bits per bin:", bits_per_bin