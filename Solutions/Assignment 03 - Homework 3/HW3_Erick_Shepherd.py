#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 3, PHYS 220, UMBC.

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
    Assignment:         03
    Assignment name:    Homework 3
    Available points:   100
    Grade percentage:   5.71%
    
    Description:        Python basics exercises.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-04-07
    
Copyright information:
--------------------------------------------------------------------------------
    This document contains the intellectual property of both Dr. Zhibo Zhang and
    Erick Edward Shepherd. The problems given are the copyright of Dr. Zhibo 
    Zhang, all rights reserved. The solutions to each respective problem are 
    the copyright of Erick Edward Shepherd, all rights reserved.
    
    This program is distributed in the hope that it will be useful for 
    educational purposes, but without any warranty; without even the implied 
    warranty of merchantability or fitness for a particular purpose.
    
    The intended audience of the publication of this document is the students
    enrolled in the Introduction to Computational Physics (PHYS 220) course 
    taught Dr. Zhibo Zhang at the University of Maryland, Baltimore County 
    (UMBC). Use of the contents of this repository by students of UMBC is 
    restricted by the academic integrity policies and principles of UMBC.
    
    All of the contents of this document are protected from copying under U.S. 
    and international copyright laws and treatises. Any unauthorized copying, 
    alteration, distribution, transmission, performance, display, or other use 
    of this material is prohibited.
"""

# Future module imports for Python 2-3 compatibility.
from __future__ import division

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Model 1,000 random walkers over 300 steps for a step size
                    of 3.5 mm and a step time of 1.0 s. Track the position of
                    each walker at each step. See HW3_corrected.pdf for more
                    information.
"""

Nw = 1000       # The number of walkers.
Ns = 300        # The number of steps.
dL = 3.5 / 1000 # The step size in meters.
dt = 1.0        # The step time in seconds.

# Pass a seed to this function if you want consistent output between runs.
np.random.seed()

# Author's note:
#   1 is added to the number of steps Ns to account for the origin, the point
#   before a step is taken by any of the walkers.
#    - Erick shepherd
direction = lambda: (-1) ** np.random.randint(0, 2)
step      = lambda: round(dL * direction(), 4)
path      = lambda: [step() if j > 0 else 0 for j in range(Ns + 1)]

# The 1D spatial and temporal displacements of each walker at a given time step.
X = np.asarray([np.cumsum(path()) for i in range(Nw)]).T
t = np.arange(0, (Ns + 1) * dt)

x_delta = 50 * dt # Time in seconds.

y_delta = 100 / 1000 # Displacement in meters.
y_limit = np.ceil(np.max(np.abs(X)) / y_delta) * y_delta

plt.figure()
plt.plot(t, X)
plt.title("Walker Displacement vs. Time")
plt.xlabel(r"Time [$s$]",         fontsize = "large")
plt.ylabel(r"Displacement [$m$]", fontsize = "large")
plt.xticks(np.arange(0, t[-1] + x_delta, x_delta))
plt.yticks(np.arange(-y_limit, y_limit + y_delta, y_delta))
plt.xlim(0, Ns)
plt.ylim(-y_limit, y_limit)
plt.grid()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         20
    Weight:         1.00
    Percentage:     20.00%
    
    Description:    Compute the mean displacement and the mean square 
                    displacement of all walkers at each step. Then, in the same 
                    figure, plot the mean displacement and the root mean square 
                    (RMS) displacement.
"""

X_mean = np.abs(np.mean(X, axis = 1))
X_rms  = np.sqrt(np.mean(np.power(X, 2), axis = 1))

plt.figure()
plt.title("Displacement vs. Time")
plt.plot(t, X_mean, c = "b", label = r"${\langle}{X}{\rangle}_i$")
plt.plot(t, X_rms,  c = "k", label = r"$\sqrt{{\langle}{X}{\rangle}_i}$")
plt.xlabel(r"Time [$s$]",         fontsize = "large")
plt.ylabel(r"Displacement [$m$]", fontsize = "large")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    In the same figure as problem 2, show that the RMS 
                    displacement is approximately the square root of 2Dt, where 
                    D is the diffusion coefficient D = (dL)^2 / (2dt).
"""

D = dL ** 2 / (2 * dt)
X_analytical = np.sqrt(2 * D * t)

X_series = np.concatenate((X_mean, X_rms, X_analytical))

y_delta       = 10 / 1000 # Displacement in meters.
y_lower_limit = np.floor(np.min(X_series) / y_delta) * y_delta
y_upper_limit = np.ceil(np.max(X_series)  / y_delta) * y_delta

plt.plot(t, X_analytical, c = "r", label = r"$\sqrt{2Dt}$")
plt.xlim(np.min(t), np.max(t))
plt.ylim(y_lower_limit, y_upper_limit)
plt.legend()
plt.grid()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        4
    Points:         20
    Weight:         1.00
    Percentage:     20.00%
    
    Description:    Compute the normalized number density function of walkers at
                    each time step in the interval x to x + dx. See the file
                    HW3_corrected.pdf for more information.
    
    
"""

# Let "experimental normalized number density function" be denoted by "ENNDF".
def ENNDF(x = 0, t = 150, dx = 3 * dL):
    
    dNw = None
    
    # For a constant time t:
    if isinstance(x, np.ndarray) and not isinstance(t, np.ndarray):
        
        dNw = np.zeros(x.size) # Walkers in the displacement interval.
        
        for index, position in enumerate(x):
            
            # Author's note:
            #   dx is divided by 2 to ensure that the interval is symmetric 
            #   about the position.
            #    - Erick Shepherd
            upper_bound = position + dx / 2
            lower_bound = position - dx / 2
            
            interval = lambda Y: (lower_bound <= Y) & (Y <= upper_bound)
            
            Y = X[t]
            
            dNw[index] = Y[interval(Y)].size
                
    # For a constant position x:
    elif not isinstance(x, np.ndarray) and isinstance(t, np.ndarray):
       
        # Author's note:
        #   dx is divided by 2 to ensure that the interval is symmetric about x.
        #    - Erick Shepherd
        upper_bound = x + dx / 2
        lower_bound = x - dx / 2

        interval = lambda Y: (lower_bound <= Y) & (Y <= upper_bound)
    
        dNw = np.zeros(Ns + 1) # Walkers in the displacement interval.
    
        for step, time in enumerate(t):
        
            Y = X[step]
            
            dNw[step] = Y[interval(Y)].size
                
    # For invalid input:
    else:
        
        raise ValueError("Either x must be an array and t must be a scalar," + \
                         " or x must be a scalar and t must be an array.")
    
    P = dNw / Nw # The probability of finding a walker in the interval.
    
    return P

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        5
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    Show that the normalized number density function from
                    problem 4 agrees with the analytical solution of the 
                    diffusion equation. You can plot both functions as either
                    functions of time at a particular displacement or functions
                    of displacement at a particular time.
"""

# Let "analytical normalized number density function" be denoted by "ANNDF".
def ANNDF(x, t):
    
    P = np.exp((-x ** 2) / (4 * D * t)) / np.sqrt(4 * np.pi * D * t)
    
    return P

dx = 3 * dL

# Solution as a function of position:
x_bound = np.ceil(np.max(np.abs(X)) / dx) * dx
x       = np.round(np.arange(-x_bound, x_bound + dx, dx), 4)
t       = 150

# Let "position function normalization constant" be denoted by "PFNC".
PFNC = np.max(ANNDF(x, 1))

P_experimental = ENNDF(x, t, dx)
P_analytical   = ANNDF(x, t) / PFNC

P_series = np.concatenate((P_experimental, P_analytical))

x_delta = 0.1
x_limit = np.ceil(np.max(np.abs(x)) / x_delta) * x_delta

y_delta       = 0.1
y_upper_limit = np.ceil(np.max(P_series) / y_delta) * y_delta

plt.figure()
plt.plot(x, P_experimental, c = "k", label = "Experimental")
plt.plot(x, P_analytical,   c = "r", label = "Analytical")
plt.suptitle("Walker Number Density vs. Position")
plt.title(r"$t={}$ s, $dx={}$ m".format(t, dx))
plt.xlabel(r"Position [$m$]")
plt.ylabel(r"Normalized Number Density")
plt.xlim(-x_limit, x_limit)
plt.ylim(0, y_upper_limit)
plt.legend()
plt.grid()

# Solution as a function of time:
x = 0
t = np.arange(0, (Ns + 1) * dt)

# Let "time function normalization constant" be denoted by "PFNC".
TFNC = np.max(ANNDF(0, t[t != 0]))

# Author's note:
#   Masking the time dimension with t[t != 0] prevents division by zero in the 
#   analytical solution.
#    - Erick Shepherd
P_experimental = ENNDF(x, t, dx)
P_analytical   = ANNDF(x, t[t != 0]) / TFNC

plt.figure()
plt.plot(t,         P_experimental, c = "k", label = "Experimental")
plt.plot(t[t != 0], P_analytical,   c = "r", label = "Analytical")
plt.suptitle("Walker Number Density vs. Time")
plt.title(r"$x={}$ m, $dx={}$ m".format(x, dx))
plt.xlabel(r"Time [$s$]")
plt.ylabel(r"Normalized Number Density")
plt.xlim(t[0], t[-1])
plt.ylim(0, 1)
plt.legend()
plt.grid()

plt.show()