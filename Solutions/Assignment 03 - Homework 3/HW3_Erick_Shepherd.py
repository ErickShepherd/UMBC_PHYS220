#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 1, PHYS 220, UMBC.

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
    (UMBC). 
    
    All of the contents of this document are protected from copying under U.S. 
    and international copyright laws and treatises. Any unauthorized copying, 
    alteration, distribution, transmission, performance, display or other use of 
    this material is prohibited.
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

X = np.asarray([np.cumsum(path()) for i in range(Nw)]).T
t = np.arange(0, (Ns + 1) * dt)

x_delta = 50 * dt # Time in seconds.

y_delta = 100 / 1000 # Displacement in meters.
y_bound = np.ceil(np.max(np.abs(X)) / y_delta) * y_delta

plt.figure()
plt.plot(t, X)
plt.title("Walker Displacement vs. Time")
plt.xlabel(r"Time [$s$]",         fontsize = "large")
plt.ylabel(r"Displacement [$m$]", fontsize = "large")
plt.xticks(np.arange(0, t[-1] + x_delta, x_delta))
plt.yticks(np.arange(-y_bound, y_bound + y_delta, y_delta))
plt.xlim(0, Ns)
plt.ylim(-y_bound, y_bound)
plt.grid()


"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    The function  max_of_three() will only work for three 
                    numbers, but suppose we have many more numbers, or suppose 
                    we cannot tell in advance how many numbers there will be?  
                    Write a function max_in_list() that takes a list of numbers 
                    and returns the largest one.
"""



"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Define two functions sum() and a function multiply() which
                    respectively sum and multiply all numbers in a list of 
                    numbers. For example, sum([1, 2, 3, 4]) should return 10, 
                    and multiply([1, 2, 3, 4]) should return 24.
                    
    Author's notes: Be wary when implementing something like this in situations
                    outside of the classroom; "sum" is a built-in function in
                    Python, and defining another function by the same name
                    will override the built-in function by that name in the
                    scope in which it is defined. - Erick Shepherd
"""

plt.show()