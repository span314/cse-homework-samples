#!/usr/bin/python
#Shawn Pan
#AM205
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def f(x, y):
  return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2

def gradf(x, y):
  dx = -400 * (y - x ** 2) * x - 2 * (1 - x)
  dy = 200 * (y - x ** 2)
  return np.array([dx, dy])

def hessf(x, y):
  dxdx = -400 * y + 1200 * x ** 2 + 2
  dxdy = -400 * x
  dydx = -400 * x
  dydy = 200
  return np.array([[dxdx, dxdy],[dydx, dydy]])

def powerspace(a, b, n, power):
  return np.linspace(a ** power, b ** power, n) ** (1 / power)

#setup rosenbrock plot
n = 200
xs = np.linspace(-1, 3, n)
ys = np.linspace(-1, 3, n)
xgrid, ygrid = np.meshgrid(xs, ys)
zgrid = np.empty((n, n))
for i in xrange(n):
  for j in xrange(n):
    zgrid[i, j] = f(xgrid[i, j], ygrid[i, j])
levels = powerspace(np.min(zgrid), np.max(zgrid), 20, 0.3)

#plot one path
def plot_path(xvalues, title, x0):
  plt.figure(figsize=(5, 5))
  plt.contour(xgrid, ygrid, zgrid, levels=levels)
  plt.plot(xvalues[:, 0], xvalues[:, 1], marker=".", color="black")
  plt.xlim((-1, 3))
  plt.ylim((-1, 3))
  plt.title("{} {}".format(title, x0))
  plt.xlabel("x")
  plt.ylabel("y")
  plt.savefig("rosenbrock-{}{}.png".format(title, x0[0]).replace("_", "-"), bbox_inches="tight")

def steepest_descent(x0):
  xvalues = [x0] #store points for plotting later
  for k in xrange(2000):
    x, y = x0
    sx, sy = -gradf(x, y)
    linesearch = minimize(lambda eta: f(x + sx * eta, y + sy * eta), 0.0, method="Nelder-Mead")
    eta = linesearch.x[0]
    x1 = np.array([x + eta * sx, y + eta * sy])
    #print x0, linesearch.fun
    xvalues.append(x1)
    if np.linalg.norm(x0 - x1) < 1e-8:
      break
    x0 = x1
  return x1, linesearch.fun, k+1, np.array(xvalues)

def newton(x0):
  xvalues = [x0] #store points for plotting later
  for k in xrange(2000):
    s = np.linalg.solve(hessf(*x0), -gradf(*x0))
    x1 = x0 + s
    #print x0, f(*x0)
    xvalues.append(x1)
    if np.linalg.norm(x0 - x1) < 1e-8:
      break
    x0 = x1
  return x1, f(*x1), k+1, np.array(xvalues)

def bfgs(x0):
  Bk = np.identity(2)
  xvalues = [x0] #store points for plotting later
  for k in xrange(2000):
    grad0 = gradf(*x0)
    sk = np.linalg.solve(Bk, -grad0)
    x1 = np.array(x0 + sk)
    yk = gradf(*x1) - grad0
    #convert to 1D vectors to 2D column matricies
    ykm = np.array([yk]).T
    skm = np.array([sk]).T
    deltaB = ykm.dot(ykm.T) / ykm.T.dot(skm) - Bk.dot(skm).dot(skm.T).dot(Bk) / skm.T.dot(Bk).dot(skm)
    Bk = Bk + deltaB
    #print x0, f(*x0)
    xvalues.append(x1)
    if np.linalg.norm(x0 - x1) < 1e-8:
      break
    x0 = x1
  return x1, f(*x1), k+1, np.array(xvalues)

for method in (steepest_descent, newton, bfgs):
  for x0 in (np.array([-1, 1]), np.array([0, 1]), np.array([2, 1])):
    print method.__name__, x0
    xopt, fopt, nsteps, steps = method(x0)
    plot_path(steps, method.__name__, x0)
    print "Steps", nsteps
    print "Opt", xopt, fopt
    print