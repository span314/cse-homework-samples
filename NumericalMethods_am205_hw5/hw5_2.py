#!/usr/bin/python
#Shawn Pan
#AM205
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin_bfgs
from scipy.optimize import check_grad

L = 1.0
p = 1.0
#p = 0
R = 2.0
w = 5.0
k = np.arange(1, 21)
pi_k_R = np.pi * k / R

def x(s, b):
  return L * s / R + np.dot(b[:20], np.sin(pi_k_R * s))

def y(s, b):
  return np.dot(b[20:], np.sin(pi_k_R * s))

def dxds(s, b):
  return L / R + np.dot(pi_k_R * b[:20], np.cos(pi_k_R * s))

def dyds(s, b):
  return np.dot(pi_k_R * b[20:], np.cos(pi_k_R * s))

def dydd(s, b):
  return np.sin(pi_k_R * s)

def dTds(s, b):
  return p * y(s, b) ** 2 * w ** 2

def dVds(s, b, mu):
  return mu * (np.sqrt(dxds(s, b) ** 2 + dyds(s, b) ** 2) - 1) ** 2

def ddc_dxds(s): #also = ddd_dyds
  return pi_k_R * np.cos(pi_k_R * s)

# Simpson's rule from 0 to R (derived from lecture 10 example)
n = 251 #control points
h = R / n #step size
def simp(f):
    fi = f(0)+f(R)
    for i in xrange(1, 251):
        fi+=4*f((i-0.5)*h)+2*f(i*h)
    fi+=4*f(R-0.5*h)
    return fi*h/6.0

#residual function
def r(b, mu):
  return simp(lambda s: dVds(s, b, mu) - dTds(s, b))

def dVdcds(s, b, mu):
  a = np.sqrt(dxds(s, b) ** 2 + dyds(s, b) ** 2)
  return mu * 2 * (a - 1) / a * dxds(s, b) * ddc_dxds(s)

def dVddds(s, b, mu):
  a = np.sqrt(dxds(s, b) ** 2 + dyds(s, b) ** 2)
  return mu * 2 * (a - 1) / a * dyds(s, b) * ddc_dxds(s)

def dVdddT(s, b):
  return 2 * p * w ** 2 * y(s, b) * dydd(s, b)

#grad resid
def grad_r(b, mu):
  grad_c = simp(lambda s: dVdcds(s, b, mu))
  grad_d = simp(lambda s: dVddds(s, b, mu) - dVdddT(s, b))
  result = np.zeros(40)
  result[:20] = grad_c
  result[20:] = grad_d
  return result

#find optimal b and plot on axis
s_points = np.linspace(0, R, 100)
def opt(b0, ax):
  for mu in (20, 200, 2000):
    bopt = fmin_bfgs(lambda b: r(b, mu), b0, fprime=lambda b: grad_r(b, mu))
    ax.plot([x(s, bopt) for s in s_points], [y(s, bopt) for s in s_points], label="mu " + str(mu))
    ax.plot([x(s, bopt) for s in s_points], [-y(s, bopt) for s in s_points], color="grey", linestyle="dotted")

b0 = np.zeros(40)
b0[20] = 1 #d1 = 1
print "Gradient vs Numeric Error", check_grad(lambda b: r(b, 20), lambda b: grad_r(b, 20), b0)
plt.figure(figsize=(5, 4))
opt(b0, plt.gca())
plt.legend(loc="lower right")
plt.title("Jump Rope d1=1")
plt.xlabel("x")
plt.ylabel("y")
plt.ylim((-2, 2))
plt.savefig("rope1.png", bbox_inches="tight")

b0 = np.zeros(40)
b0[21] = 0.5 #d2 = 0.5
print "Gradient vs Numeric Error", check_grad(lambda b: r(b, 20), lambda b: grad_r(b, 20), b0)
plt.figure(figsize=(5, 4))
opt(b0, plt.gca())
#plt.legend()
plt.title("Jump Rope d2=0.5")
plt.xlabel("x")
plt.ylabel("y")
plt.ylim((-2, 2))
plt.savefig("rope2.png", bbox_inches="tight")