#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 6, PHYS 220, UMBC.

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
    Assignment name:    Homework 6
    Available points:   100
    Grade percentage:   5.71%
    
    Description:        Numerical differentiation in Python.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-05-06
    
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

from scipy.interpolate import interp1d
from scipy.interpolate import lagrange
from scipy.optimize    import curve_fit

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         30
    Weight:         1.00
    Percentage:     30.00%
    
    Description:    Use the linear, Lagrange, and cubic spline methods to 
                    interpolate and get high-angular resolution data every 0.5 
                    degrees.
                    
                    See "Homework6.pdf" for more information.
"""

# Assuming the target files are in the same folder as the HW6_Erick_Shepherd.py file.
work_path = ""

# Given data set - Low resolution.
X_low  = np.load(work_path + "scattering_angle_low.npy")
Y_low  = np.load(work_path + "Phase_function_low.npy")

# Given data set - High resolution.
X_high = np.load(work_path + "scattering_angle_high.npy")
Y_high = np.load(work_path + "Phase_function_high.npy")

# Problem 1 - Part 1: Linear interpolation
X_low_linear     = np.arange(min(X_low), max(X_low), 0.5)
linearFunction   = interp1d(X_low, Y_low, kind = "linear")
Y_low_linear     = linearFunction(X_low_linear)

# Author's note:
#
#   Per both the course documents on numerical interpolation and the SciPy 
#   documentation on the Lagrange function within the module, the Lagrange 
#   method is numerically unstable and is problematic when graphing either 
#   highly variable data or data where the number of data points is larger 
#   than twenty.
#
#   In this particular case, we have a highly variable data set which is 
#   comprised of twenty four data points. Thus, unless we restrict the domain 
#   over which we take the Lagrange interpolation, the graph displays a nearly 
#   vertical line and establishes no trend.
#
#   The domain of elements 10 through 19 of the data set (indices 9 to 19) 
#   appears to produce the best fit.
#
#   - Erick Shepherd

# Problem 1 - Part 2: Lagrange interpolation
X_low_lagrange   = X_low_linear
lagrangeFunction = lagrange(X_low[9:19], Y_low[9:19])
Y_low_lagrange   = lagrangeFunction(X_low_lagrange)

# Problem 1 - Part 3: Cubic spline interpolation
X_low_cubic      = X_low_linear
cubicFunction    = interp1d(X_low.astype(np.double), Y_low.astype(np.double), kind = "cubic")
Y_low_cubic      = cubicFunction(X_low_cubic)

def plotDataPoints():

    label1 = "Data"
    label2 = "Want"

    plot1  = plt.scatter(X_low,  Y_low,  c = "b", zorder = 1, s  = 15,    edgecolor = "k")
    plot2, = plt.plot   (X_high, Y_high, c = "r", zorder = 0, ls = "--",  linewidth = 1.0)

    plt.xlabel("Scattering Angle")
    plt.ylabel("P11")

    plt.xlim([90, 160])
    plt.ylim([0.0, 0.5])

    plt.xticks(np.arange(90,  160 + 1,   10))
    plt.yticks(np.arange(0.0, 0.5 + 0.1, 0.1))

    plt.grid(b = True, which = 'both', color = 'gray', linestyle = '--')

    labels = [label1, label2]
    plots  = [plot1,  plot2]

    return plots, labels

def graphProblem1():

    figure = plt.figure()
    figure.subplots_adjust(hspace = 0.5, wspace = 0.5)

    plt.get_current_fig_manager().window.state("zoomed")

    plt.suptitle("Scattering Phase Function vs. Scattering Angle")

    # Subplot 1 - Raw data
    plt.subplot(221)

    plt.title("Desired Fit vs. Data Set")

    plots, labels = plotDataPoints()

    plt.legend(plots, labels, loc = 2)

    # Subplot 2 - Linear interpolation (Graph of problem 1 - part 1)
    plt.subplot(222)

    plt.title("Desired Fit vs. Linear Interpolation")

    plots, labels = plotDataPoints()

    label = "Linear interpolation"
    plot, = plt.plot   (X_low_linear,   Y_low_linear)

    labels.append(label)
    plots.append(plot)

    plt.legend(plots, labels, loc = 2)

    # Subplot 3 - Lagrange interpolation (Graph of problem 1 - part 2)
    plt.subplot(224)

    plt.title("Desired Fit vs. Lagrange Interpolation")

    plots, labels = plotDataPoints()

    label = "Lagrange interpolation"
    plot, = plt.plot(X_low_lagrange, Y_low_lagrange)

    labels.append(label)
    plots.append(plot)

    plt.legend(plots, labels, loc = 2)

    # Subplot 4 - Cubic interpolation (Graph of problem 1 - part 3)
    plt.subplot(223)

    plt.title("Desired Fit vs. Cubic Interpolation")

    plots, labels = plotDataPoints()

    label = "Cubic interpolation"
    plot, = plt.plot(X_low_cubic, Y_low_cubic)

    labels.append(label)
    plots.append(plot)

    plt.legend(plots, labels, loc = 2)

graphProblem1()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         30
    Weight:         1.00
    Percentage:     30.00%
    
    Description:    Assume your Monte-Carlo radiative transfer code computes the
                    cloud reflectances (“Ref”) for several values of cloud 
                    optical thickness (“Tau”). See data below.
                    
                        1) Use cubic spline method the interpolate the data.
                        
                        2) Use the model Ref = Tau / (a + b * Tau) to fit the 
                           data, where a and b are two adjustable parameters. 
                           Find the optimal values for a and b.
                           
                        3) Convert the second problem to a linear fitting 
                           problem.
                    
                    See "Homework6.pdf" for more information.
"""

# Given data set.
Tau = np.array([0.299,      1.29400003, 2.28900003, 3.28399992, 4.27899981,
                5.27399969, 6.26900005, 7.26399994, 8.25900078, 9.25400066,
                10.2490005, 11.2440004, 12.2390003, 13.2340002, 14.2290001,
                15.2240009, 16.2189999, 17.2140007, 18.2089996, 19.2040005])

# Given data set.
Ref = np.array([0.17678887, 0.48721159, 0.62823123, 0.70785129, 0.75912076,
                0.79498094, 0.82153791, 0.84198004, 0.85822612, 0.87143803,
                0.8823905,  0.89163792, 0.89952338, 0.90634716, 0.91229314, 
                0.91752762, 0.92218465, 0.92633438, 0.93006754, 0.93343675])

# Problem 2 - Part 1: Cubic spline interpolation
Tau_cubic      = np.arange(min(Tau), max(Tau), 0.1)
cubicFunction  = interp1d(Tau.astype(np.double), Ref.astype(np.double), kind = "cubic")
Ref_cubic      = cubicFunction(Tau_cubic)

# Problem 2 - Part 2: Optimal values of the reflectance function.

reflectanceFunction = lambda Tau, a, b: Tau / (a + b * Tau)

optimalParameters, _ = curve_fit(reflectanceFunction, Tau, Ref)

a = optimalParameters[0]
b = optimalParameters[1]

# Problem 2 - Part 3: Linear regression of the reflectance function.

def linearfit(x, y, yError = None):

    if yError is None or np.sum(yError) == 0:
        w = None
        
    else:
        w = 1 / yError

    p    = np.polyfit(x, y, 1, w = w)
    yfit = np.polyval(p, x)
    
    SS_total = np.var(y) * y.size
    residual = y - yfit
    SS_res   = np.sum(residual ** 2) 

    if yError is None or np.sum(yError)==0:
        chiSquared = None
        
    else:
        chiSquared = np.sum((resid / yError) ** 2) /(y.size - 2)

    R2 = 1.0 - SS_res / SS_total

    return yfit, p, R2, chiSquared, residual

x = 1 / Tau
y = 1 / Ref

linearizedY, _, _, _, _ = linearfit(x, y)

def graphProblem2():

    figure = plt.figure()
    figure.subplots_adjust(hspace = 0.5, wspace = 0.5)

    plt.get_current_fig_manager().window.state("zoomed")

    plt.suptitle("Cloud Reflectance vs. Cloud Optical Thickness")

    # Raw data
    plt.subplot(221)
    plt.scatter(Tau, Ref, c = "b", zorder = 5, s  = 15, edgecolor = "k")
    plt.xlabel(r"Cloud Optical Thickness $[\tau]$")
    plt.ylabel(r"Cloud Reflectance $[R]$")
    plt.grid(b = True, which = 'both', color = 'gray', linestyle = '--')
    plt.title("Raw data")
    plt.xlim([0, 20])

    # Cubic spline interpolation (Graph of problem 2 - part 1)
    plt.subplot(222)
    plt.plot(Tau_cubic, Ref_cubic, c = "r", zorder = 0, ls = "--", linewidth = 1.0)
    plt.scatter(Tau, Ref, c = "b", zorder = 5, s  = 15, edgecolor = "k")
    plt.xlabel(r"Cloud Optical Thickness $[\tau]$")
    plt.ylabel(r"Cloud Reflectance $[R]$")
    plt.grid(b = True, which = 'both', color = 'gray', linestyle = '--')
    plt.title("Cubic spline interpolation")
    plt.xlim([0, 20])

    # Optimized function fit (Graph of problem 2 - part 2)
    plt.subplot(223)
    plt.plot(Tau, reflectanceFunction(Tau, a, b))
    plt.scatter(Tau, Ref, c = "b", zorder = 5, s  = 15, edgecolor = "k")
    plt.xlabel(r"Cloud Optical Thickness $[\tau]$")
    plt.ylabel(r"Cloud Reflectance $[R]$")
    plt.grid(b = True, which = 'both', color = 'gray', linestyle = '--')
    plt.title("Optimized function fit")
    plt.xlim([0, 20])

    # Converted linear fit (Graph of problem 2 - part 3)
    plt.subplot(224)
    plt.plot(x, y, c = "r", zorder = 0, ls = "--", linewidth = 1.0)
    plt.scatter(x, linearizedY, c = "b", zorder = 5, s  = 15, edgecolor = "k")
    plt.xlabel(r"Inverse Cloud Optical Thickness $[\frac{1}{\tau}]$")
    plt.ylabel(r"Inverse Cloud Reflectance $[\frac{1}{R}]$")
    plt.grid(b = True, which = 'both', color = 'gray', linestyle = '--')
    plt.title("Converted linear fit")
    
graphProblem2()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    Based on the cloud fraction data, develop a non-linear model 
                    to describe the diurnal variation of cloud in the Southeast 
                    Atlantic region. Print out the formula of your model and list 
                    all adjustable parameters. Plot the fitting result in the 
                    same figure with the original data.
                    
                    See "Homework6.pdf" for more information.
"""

cf   = np.load(work_path + "Cloud_Fraction.npy")
time = np.zeros(cf.shape, float)

for n in range(len(time)):
    for m in range(len(time[n])):
        time[n][m] = n + 1

cf_mean   = [np.mean(cf[n])   for n in range(len(cf))]
time_mean = [np.mean(time[n]) for n in range(len(time))]

sineFunction = lambda time, a, b, c, d: a * np.sin(b * time + c) + d

guess = (cf_mean[-1], (2 * np.pi) / time_mean[-1], 1, 1)

optimalParameters, _ = curve_fit(sineFunction, time_mean, cf_mean, p0 = guess)

a = optimalParameters[0]
b = optimalParameters[1]
c = optimalParameters[2]
d = optimalParameters[3]

print("Problem 3:")
print("  Formula: f(x) = a * sin(b * t + c) + d")
print("    a =", a)
print("    b =", b)
print("    c =", c)
print("    d =", d)

x = np.linspace(np.amin(time), np.amax(time), 100)
y = sineFunction(x, a, b, c, d)

def graphProblem3():

    plt.figure()

    plt.get_current_fig_manager().window.state("zoomed")

    plt.plot   (x,    y,  c = "r")
    plt.scatter(time, cf, c = "b", edgecolors = "k")

    plt.xlabel("Local time [hr]")
    plt.ylabel("Cloud Fraction [%]")

    plt.xlim([0, len(time)])
    plt.ylim([40, 90])

    plt.xticks(np.arange(0, np.amax(time) + 1, 6))
    plt.yticks(np.arange(40, 90 + 1, 10))

    plt.grid(b = True, which = 'both', color = 'gray', linestyle = '--')

    plt.title("Diurnal variation of cloud fraction in the Southeast Atlantic region")

graphProblem3()

plt.show()