#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 5, PHYS 220, UMBC.

Course information:
--------------------------------------------------------------------------------
    Name:               Introduction to Computational Physics
    ID:                 PHYS 220
    Instructor:         Dr. Zhibo Zhang
    Teaching assistant: Erick Edward Shepherd
    Institution:        University of Maryland, Baltimore County
    Department:         Department of Physics

Assignment information:
--------------------------------------------------------------------------------
    Author:             Dr. Zhibo Zhang, Professor
    E-mail:             Zhibo.Zhang@UMBC.edu
    Date:               2017-01-30
    Assignment:         06
    Assignment name:    Homework 5
    Available points:   100
    Grade percentage:   5.71%
    
    Description:        Numerical differentiation in Python.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-04-14
    
Copyright information:
--------------------------------------------------------------------------------
    This document contains the intellectual property of both Dr. Zhibo Zhang and
    Erick Edward Shepherd. The problems given are the copyright of Dr. Zhibo 
    Zhang, all rights reserved. The solutions to each respective problem are 
    the copyright of Erick Edward Shepherd, all rights reserved.
    
    This program is distributed in the hope that it will be useful for 
    educational purposes, but without any warranty; without even the implied 
    warranty of merchantability or fitness for a particular purpose. All of the
    contents of this document are protected from copying under U.S. and 
    international copyright laws and treatises. Any unauthorized copying, 
    alteration, distribution, transmission, performance, display, or other use 
    of this material is prohibited.
    
    The intended audience of the publication of this document is the students
    enrolled in the Introduction to Computational Physics (PHYS 220) course 
    taught Dr. Zhibo Zhang at the University of Maryland, Baltimore County 
    (UMBC). Use of the contents of this repository by students of UMBC is 
    restricted by the academic integrity policies and principles of UMBC.
"""

# Future module imports for Python 2-3 compatibility.
from __future__ import division, print_function

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np

# Local application imports.
# Let "Monte Carlo radiative transfer" be denoted by "MCRT".
from MCRT_Erick_Shepherd import MCRT_OOP, MCRT_procedural, LoadingBar

# Author's note:
#   In the file MCRT.py, I have included both a procedural and an object
#   oriented approach to solving the Monte Carlo radiative transfer problem.
#   This MCRT variable is an alias for whichever function you wish to use in
#   the ensuing code: MCRT_procedural or MCRT_OOP. Comment/uncomment as needed.
#    - Erick Shepherd

MCRT = MCRT_procedural
#MCRT = MCRT_OOP

# Author's note:
#   The number of photons to use in each run of the Monte Carlo simulation plays
#   a critical role in the runtime of the program as a whole, so this variable
#   is the dominant term in the function of the runtime of the application.
#   Tweak it as needed to produce results in a reasonable time; however, do note
#   that the larger a sample size is used, the less noise there is in the 
#   results. 10,000 (1e5) is fairly reasonable for most purposes both in terms 
#   of accuracy and runtime. I use 100,000 (1e6) for a higher quality image.
#    - Erick Shepherd
N_photons = 1000

def derivative(f, h = 1e-5):
    
    """
    Uses the definition of the derivative to compute the derivative of a
    function f.
    """
    
    return lambda x_n: (f(x_n + h / 2) - f(x_n - h / 2)) / h

def bisection(f, x_1, x_2, tolerance = 1e-5, max_steps = 100, steps = 0):
    
    """
    Given a function f and two bounds x_1 and x_2, this function returns the 
    root of f using the bisection method.
    """
    
    steps += 1
    
    if steps == max_steps:
        
        print("Maximum number of iterations reached before convergence.")
        return None, steps
    
    else:
        
        x_m = (x_1 + x_2) / 2
        
        if f(x_m) * f(x_2) < 0:
            x_1 = x_m
        else:
            x_2 = x_m
            
        if abs(x_1 - x_2) < tolerance:
            return x_m, steps
        else:
            return bisection(f, x_1, x_2, tolerance, max_steps, steps)
        
def newton(f, x_n, h = 1e-5, tolerance = 1e-5, max_steps = 100, steps = 0,
           output = False, x_string = None, y_string = None, x_minimum = None,
           x_reset = None):
    
    """
    Given a function f, its derivative f_prime, and a starting position to
    "guess" the proximity of the root, this function returns the root of f
    using Newton's method.
    """

    if steps == max_steps:
        
        print("Maximum number of iterations reached before convergence.")
        return None, steps
        
    else:
    
        steps += 1

        f_prime = derivative(f, h)
        
        try:
            
            x_m = x_n - f(x_n) / f_prime(x_n)
            
        except ZeroDivisionError:
            
            while f_prime(x_n) == 0:
                x_n += h
                
            x_m = x_n - f(x_n) / f_prime(x_n)
            
        if x_minimum != None and x_reset != None:
            if x_m < x_minimum:
                x_m = x_reset
            
        if output:
            print("Step {:0>2}.".format(steps), 
                  x_string.format(x_m) + ",",
                  y_string.format(f(x_m)))
        
        if abs(f(x_m)) < tolerance:
            return x_m, steps
        else:
            return newton(f, x_m, h, tolerance, max_steps, steps,
                          output, x_string, y_string, x_minimum, x_reset)

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         20
    Weight:         1.00
    Percentage:     20.00%
    
    Description:    Use Newton's and bisection methods to compute the roots of
                    f(x) = 15 * pi - x * e^(-0.2 * sin(x / 5)) in the range
                    [0, 100] with an error tolerance of 1e-5.
"""

# Author's note:
#   The root of this function is found at 15pi. This may be verified using
#   WolframAlpha:
#
#       goo.gl/5EpCVr
#
#   The derivative here is found numerically from the definition of the
#   derivative, but the function may also be verified using WolframAlpha:
#
#       goo.gl/Uguj5r
#
#   - Erick Shepherd

x_min = 0
x_max = 100
x_mid = (x_min + x_max) / 2

f       = lambda x: 15 * np.pi - x * np.exp(-0.2 * np.sin(x / 5))
f_prime = derivative(f)
    
f_string       = r"$f(x)=15\pi-xe^{-0.2\sin\frac{x}{5}}$"
f_prime_string = r"$f'(x)=e^{-0.2\sin\frac{x}{5}}(0.04x\cos\frac{x}{5}-1)$"

x       = np.linspace(x_min, x_max, 100)
y       = f(x)
y_prime = f_prime(x)

bisection_root, bisection_steps = bisection(f, x_min, x_max)
newton_root,    newton_steps    = newton(f, x_mid)

plt.figure()
plt.title("Problem 1")
plt.xlabel(r"x")
plt.ylabel(r"y")
plt.plot(x, y, label = f_string, zorder = 2)
plt.plot(x, y_prime, label = f_prime_string, zorder = 1)
plt.scatter(bisection_root, 0, label = "Root by bisection method", zorder = 3)
plt.scatter(newton_root,    0, label = "Root by Newton's method",  zorder = 4)
plt.xlim(x_min, x_max)
plt.axhline(0, color = "k")
plt.axvline(0, color = "k")
plt.grid()
plt.legend()

output_string = "{} method converged to {:.8f} after {} steps."

print("Problem 1:")
print(output_string.format("Bisection", bisection_root, bisection_steps))
print(output_string.format("Newton's ", newton_root, newton_steps), end = "\n\n")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    Given the initial conditions L = 1.2, R = 3.0, and
                    s(0) = s(L) = R for the formula s(z) = a * cosh((z - b) / a)
                    where b = a * arccosh(R / a), numerically solve for alpha 
                    (a) and beta (b), print their values, and use them to plot
                    the radius of the soap film between two rings as a function
                    of height using s(z).
                    
                    See "HW5.pdf" for more information.
"""

L = 1.2
R = 3

r_min = 0
r_max = R
dr    = 0.1

z_0 = 0
z_f = L

# Author's note:
#
#   From HW5.pdf, we are given the following:
#       s(z) = a * cosh((z - b) / a)
#       b = a * arccosh(R / a)
#       s(0) = s(L) = R
#
#   By substitution:
#       => s(z) = a * cosh((z - a * arccosh(R / a)) / a)
#       => s(z) = a * cosh(z / a - arccosh(R / a))
#
#   From our initial conditions:
#       => s(0) = a * cosh(0 / a - arccosh(R / a)) = R
#               = a * cosh(- arccosh(R / a)) = R
#               = a * (R / a) = R
#               = R = R
#
#       Thus s(0) is trivial and cannot be used to solve for alpha.
#
#       => s(L) = a * cosh(L / a - arccosh(R / a)) = R
#               = a * cosh(L / a - arccosh(R / a)) - R = 0
#
#   Thus we search for the roots of the following:
#       f(a) = a * cosh(L / a - arccosh(R / a)) - R = 0
#
#   - Erick Shepherd

f_alpha = lambda a: a * np.cosh(L / a - np.arccosh(R / a)) - R
f_beta  = lambda alpha: alpha * np.arccosh(R / alpha)
s       = lambda z, alpha, beta: alpha * np.cosh((z - beta) / alpha)

# Author's note:
#   This function is undefined due to division by zero for alpha = 0 and is
#   for the same reason asymptotic about 0 for very small alpha. The function
#   actually has two roots: One near its minimum value and one near its maximum
#   value.
#   - Erick Shepherd
alpha1, _ = newton(f_alpha, r_min + dr)
alpha2, _ = newton(f_alpha, r_max - dr)

beta1 = f_beta(alpha1)
beta2 = f_beta(alpha2)
    
z  = np.linspace(z_0, z_f, 100)
r1 = s(z, alpha1, beta1)
r2 = s(z, alpha2, beta2)

label_string = r"$\alpha = {:.3f}, \beta = {:.3f}$"

plt.figure()
plt.title("Problem 2")
plt.xlabel(r"z")
plt.ylabel(r"R")
plt.plot(z, r1, label = label_string.format(alpha1, beta1))
plt.plot(z, r2, label = label_string.format(alpha2, beta2))
plt.xlim(z_0, z_f)
plt.axhline(0, color = "k")
plt.axvline(0, color = "k")
plt.grid()
plt.legend()

output_string = "Root {}: alpha = {:.8f}, beta = {:.8f}."

print("Problem 2:")
print(output_string.format(1, alpha1, beta1))
print(output_string.format(2, alpha2, beta2), end = "\n\n")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    Find a cloud optical thickness t* to minimize the function
                    |R(t*) - R_obs|, where R(t*) is the Monte Carlo radiative
                    transfer (MCRT) function for a given cloud optical thickness
                    and R_obs is the observed cloud optical thickness.
                    
                    See "HW5.pdf" for more information.
"""

def inverse_MCRT(COT, SSA = 1, SZA = 0, R_obs = 0.6):
        
    difference = abs(MCRT(COT, SSA, SZA, N_photons)["reflectance"] - R_obs)
    
    return difference

SSA   = 1
SZA   = 0
R_obs = 0.6

T = lambda COT: inverse_MCRT(COT, SSA, SZA, R_obs)

print("Problem 3:")
tau, _ = newton(T, 1, 0.01, 0.01, output = True, 
                x_string = "t* = {:.4f}", y_string = "|R(t*) - R_obs| = {:.4f}",
                x_minimum = 0, x_reset = 1)

R_confirmed = MCRT(tau, 1, 0, N_photons)["reflectance"]

output_string_1 = "\nThe cloud optical thickness corresponding to an\n" + \
                  "observed reflectance of {} for a single scattering\n" + \
                  "albedo of {} and a solar zenith angle of {} is\n" + \
                  "t* = {:.4f}.\n"
        
output_string_2 = "Substituting the cloud optical thickness t* = {0:.4f}\n" + \
                  "from the inverse problem into the forward problem, we\n" + \
                  "find that R({0:.4f}) = {1:.4f} vs. an observed\n" + \
                  "reflectance of {2}."

print(output_string_1.format(R_obs, SSA, SZA, tau))
print(output_string_2.format(tau, R_confirmed, R_obs))

plt.show()