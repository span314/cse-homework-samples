#!/usr/bin/python
#Shawn Pan
#AM205
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=5)

n = 1921
n0 = 961
n6 = 1441
x = np.linspace(-12, 12, n)
h = x[1] - x[0]
ih2 = 1 / (h * h)

# Simpson's rule applied to an array of points with spacing h
def simp(points):
  fi = points[0] + points[-1]
  for i in xrange(1, len(points) - 1):
    scale = 2 * (1 + (i % 2)) #scale odd points by 4, even points by 2
    fi += scale * points[i]
  return fi * h / 3.0

def eigenmodes(v, title, ymin, ymax):
  offdiag = np.full(n - 1, -ih2)
  potential = v(x)
  H = np.diag(offdiag, -1) + np.diag(potential + 2 * ih2) + np.diag(offdiag, 1)
  eigval, eigvec = np.linalg.eigh(H)
  prob = np.zeros(5)

  #plot and caculate probabilties
  plt.figure()
  plt.plot(x, potential, label="Potential")
  for i in xrange(4, -1, -1):
    psi = eigvec[:, i]
    energy = eigval[i]
    prob[i] = simp(np.square(psi[n0:n6+1])) / simp(np.square(psi))
    plt.axhline(energy, -12, 12, color="lightgrey")
    plt.plot(x, 3 * psi + energy, label="E{} {:8.6f}".format(i+1, energy))

  plt.legend(bbox_to_anchor=(1.4, 1))
  plt.xlim((-12, 12))
  plt.ylim((ymin, ymax))
  plt.title("Eigenmodes {}".format(title))
  plt.xlabel("x")
  plt.ylabel("Energy")
  plt.savefig("eig{}".format(title), bbox_inches="tight")

  print "Energies", eigval[:5]
  print "Probability", prob


eigenmodes(lambda x: x * x / 10.0, "v0", 0, 4)
eigenmodes(lambda x: np.abs(x), "v1", 0, 6)
eigenmodes(lambda x: 12 / 10000. * x ** 4 - x ** 2 / 18. + x / 8. + 1.3, "v2", 0, 2.5)
eigenmodes(lambda x: 8 * np.abs(np.abs(np.abs(x) - 1) - 1), "v3", 0, 10)