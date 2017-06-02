#!/usr/bin/python
from __future__ import division

def max_sum(arr):
  x = 0 #start index
  y = 0 #end index
  z = 0 #current sum
  best_x = 0 #best start index
  best_y = 0 #best stop index
  best_z = 0 #best sum
  for y, value in enumerate(arr):
    z += value
    if z > best_z: #update best
      best_x = x
      best_y = y
      best_z = z
    if z < 0: #discard negative subsequence, better to leave out
      x = y + 1
      z = 0
  return (best_x, best_y, best_z)

def run_test(arr):
  print("Input Array")
  print(arr)
  print("X, Y, Z")
  print(max_sum(arr))

#tests
run_test([1, 2, 3, 4, 5])
run_test([1, -5, 3])
run_test([3, -2, 3])
run_test([-2, 1, 7, -4, 5, 2, -3, -6, 4, 3, -8, -1, 6, -7, -9, -5])