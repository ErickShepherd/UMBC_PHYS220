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

# Standard library imports.
import os

# Third party imports.
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d, lagrange
from scipy.optimize    import curve_fit
from scipy.stats       import linregress

# Assuming the data files are in the same folder as this file.
work_path = ""

def load(filename):
    
    return np.load(os.path.join(work_path, filename)).astype(np.double)

def main():
    
    problem1()
    problem2()
    problem3()

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

def problem1():
    
    # Low resolution data set for interpolation.
    x_low  = load("scattering_angle_low.npy")
    y_low  = load("Phase_function_low.npy")

    # High resolution data set for fit comparison.
    x_high = load("scattering_angle_high.npy")
    y_high = load("Phase_function_high.npy")
    
    # Author's note:
    #
    #   Per both the course documents on numerical interpolation and the SciPy 
    #   documentation on the Lagrange function within the module, the Lagrange 
    #   method is numerically unstable and is problematic when graphing either 
    #   highly variable data or data where the number of data points is larger 
    #   than twenty.
    #
    #   In this particular case, we have a highly variable data set which is 
    #   comprised of twenty four data points. Thus, unless we restrict the  
    #   domain over which we take the Lagrange interpolation, the graph explodes
    #   beyond usefulness.
    #
    #   The domain of elements 10 through 19 of the data set (indices 9 to 19) 
    #   appears to produce a good fit which captures the relevant major features
    #   of the given data.
    #
    #   - Erick Shepherd
    
    # Angular resolution in in degrees.
    resolution = 0.5
    
    x = np.arange(np.min(x_low), np.max(x_low) + resolution, resolution)
    
    # Problem 1, part 1 - Linear interpolation.
    linear_function = interp1d(x_low, y_low, kind = "linear")
    y_linear        = linear_function(x)
    
    # Problem 1, part 2 - Lagrange interpolation.
    lagrange_function = lagrange(x_low[9:19], y_low[9:19])
    y_lagrange        = lagrange_function(x)
    
    # Problem 1, part 3 - Cubic spline interpolation.
    cubic_function = interp1d(x_low, y_low, kind = "cubic")
    y_cubic        = cubic_function(x)
    
    # Plot problem 1, part 1 - Linear interpolation.
    plt.figure()
    plt.suptitle("Problem 1 - Figure 1")
    plt.title("Linear Interpolation")
    plt.xlabel(r"Scattering Angle")
    plt.ylabel(r"P11")
    
    plot = plt.scatter(x_low, y_low, 
                c = "k", zorder = 3, label = "Raw data")
    
    plt.plot(x_high, y_high, ls = "--", 
             c = "r", zorder = 1, label = "Desired fit")
    
    plt.plot(x, y_linear, 
             c = "b", zorder = 2, label = "Interpolation")
    
    plt.xlim(np.min(x), np.max(x))
    
    plt.ylim(np.floor(np.min(y_high) * 2) / 2, 
             np.ceil(np.max(y_high) * 2) / 2)
    
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    # Plot problem 1, part 2 - Lagrange interpolation.
    plt.figure()
    plt.suptitle("Problem 1 - Figure 2")
    plt.title("Lagrange Interpolation")
    plt.xlabel(r"Scattering Angle")
    plt.ylabel(r"P11")
    
    plot = plt.scatter(x_low, y_low, 
                c = "k", zorder = 3, label = "Raw data")
    
    plt.plot(x_high, y_high, ls = "--", 
             c = "r", zorder = 1, label = "Desired fit")
    
    plt.plot(x, y_lagrange, 
             c = "b", zorder = 2, label = "Interpolation")
    
    plt.xlim(np.min(x), np.max(x))
    
    plt.ylim(np.floor(np.min(y_high) * 2) / 2, 
             np.ceil(np.max(y_high) * 2) / 2)
    
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    # Plot problem 1, part 3 - Cubic spline interpolation.
    plt.figure()
    plt.suptitle("Problem 1 - Figure 3")
    plt.title("Cubic Spline Interpolation")
    plt.xlabel(r"Scattering Angle")
    plt.ylabel(r"P11")
    
    plot = plt.scatter(x_low, y_low, 
                c = "k", zorder = 3, label = "Raw data")
    
    plt.plot(x_high, y_high, ls = "--", 
             c = "r", zorder = 1, label = "Desired fit")
    
    plt.plot(x, y_cubic, 
             c = "b", zorder = 2, label = "Interpolation")
    
    plt.xlim(np.min(x), np.max(x))
    
    plt.ylim(np.floor(np.min(y_high) * 2) / 2, 
             np.ceil(np.max(y_high) * 2) / 2)
    
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()

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

def problem2():

    # Given in "Homework6.pdf".
    tau = np.array([0.299,      1.29400003, 2.28900003, 3.28399992, 4.27899981,
                    5.27399969, 6.26900005, 7.26399994, 8.25900078, 9.25400066,
                    10.2490005, 11.2440004, 12.2390003, 13.2340002, 14.2290001,
                    15.2240009, 16.2189999, 17.2140007, 18.2089996, 19.2040005])

    # Given in "Homework6.pdf".
    ref = np.array([0.17678887, 0.48721159, 0.62823123, 0.70785129, 0.75912076,
                    0.79498094, 0.82153791, 0.84198004, 0.85822612, 0.87143803, 
                    0.8823905,  0.89163792, 0.89952338, 0.90634716, 0.91229314, 
                    0.91752762, 0.92218465, 0.92633438, 0.93006754, 0.93343675])
    
    # Problem 2, part 1 - Cubic spline interpolation.
    cubic_function = interp1d(tau, ref, kind = "cubic")
    ref_cubic      = cubic_function(tau)
    
    # Problem 2, part 2 - Optimized function fit.
    reflectance_function  = lambda tau, a, b: tau / (a + b * tau)
    fitted_parameters, _ = curve_fit(reflectance_function, tau, ref)

    a, b = fitted_parameters
    
    tau_optimized = np.linspace(np.min(tau), np.max(tau), 100)
    ref_optimized = reflectance_function(tau_optimized, a, b)
    
    # Problem 2, part 3 - Converted linear fit.
    tau_L = (a + b * tau) / tau
    ref_L = 1 / ref
    slope, intercept, r_value, p_value, std_err = linregress(tau_L, ref_L)
    linear_function = lambda x: slope * x + intercept
    ref_linear = linear_function(tau_L)
    
    # Plot problem 2, part 1 - Cubic spline interpolation.
    plt.figure()
    plt.suptitle("Problem 2 - Figure 1")
    plt.title("Cubic Spline Interpolation")
    plt.xlabel(r"$\tau$")
    plt.ylabel(r"$R$")
    plt.plot(tau, ref_cubic, zorder = 0, c = "b", label = "Interpolation")
    plt.scatter(tau, ref, zorder = 1, c = "k", label = "Raw data")
    plt.xlim(np.min(tau), np.max(tau))
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    # Plot problem 2, part 2 - Optimized fit function.
    plt.figure()
    plt.suptitle("Problem 2 - Figure 2")
    plt.title("Optimized Fit Function")
    plt.xlabel(r"$\tau$")
    plt.ylabel(r"$R$")
    plt.plot(tau_optimized, ref_optimized, zorder = 0, c = "b", 
             label = "Optimized fit")
    plt.scatter(tau, ref, zorder = 1, c = "k", label = "Raw data")
    plt.xlim(np.min(tau), np.max(tau))
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    # Plot problem 2, part 3 - Converted linear fit.
    plt.figure()
    plt.suptitle("Problem 2 - Figure 3")
    plt.title("Converted Linear Fit")
    plt.xlabel(r"$\frac{a + b\tau}{\tau}$")
    plt.ylabel(r"$\frac{1}{R}$")
    plt.plot(tau_L, ref_linear, zorder = 0, c = "b", 
             label = "Least squares fit")
    plt.scatter(tau_L, ref_L, zorder = 1, c = "k", label = "Raw data")
    plt.xlim(np.min(tau_L), np.max(tau_L))
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()

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

def problem3():

    cf = load("Cloud_Fraction.npy").T
    t  = np.repeat(np.arange(0, cf.shape[1]), cf.shape[0]).reshape(cf.T.shape).T
    
    mean_cf = np.mean(cf, axis = 0)
    
    # Problem 2, part 2 - Optimized function fit.
    a0 = np.abs(np.max(mean_cf) - np.min(mean_cf)) / 2
    b0 = 2.0 * np.pi / t[0].size
    c0 = 0.0
    d0 = np.mean(mean_cf)
    p0 = (a0, b0, c0, d0)
    
    cf_function          = lambda t, a, b, c, d: a * np.sin(b * t + c) + d
    fitted_parameters, _ = curve_fit(cf_function, t[0], mean_cf, p0 = p0)
    
    a, b, c, d = fitted_parameters
    
    t_fit  = np.linspace(np.min(t), np.max(t), 1000)
    cf_fit = cf_function(t_fit, a, b, c, d)
    
    x_buffer = np.std(t)
    y_buffer = np.std(cf)
    
    x_min, x_max = np.min(t), np.max(t)
    y_min, y_max = np.min(cf) - y_buffer, np.max(cf) + y_buffer

    label_data = "Raw data"
    label_fit  = "Optimized fit"
    
    text = r"$f(t)={:.2f}\sin({:.2f}t + {:.2f}) + {:.2f}$".format(a, b, c, d)
    text_x, text_y = x_min + x_buffer / 4, y_min + y_buffer / 4
    
    plt.figure()
    plt.suptitle("Problem 3")
    plt.title("Optimized Function Fit")
    plt.xlabel(r"Time [$hr$]")
    plt.ylabel(r"Cloud Fraction")
    plt.text(text_x, text_y, text, backgroundcolor = "w", size = "large")
    plt.plot(t_fit, cf_fit, zorder = 1, c = "b", label = label_fit)
    plt.scatter(t, cf, zorder = 0, c = "k", label = label_data)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(np.array(list(range(np.min(t), np.max(t), 4)) + [np.max(t)]))
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend(loc = 1)
    
    variables   = ["a", "b", "c", "d"]
    
    algebraic_formula = "{} * sin({} * t + {}) + {}"
    
    slots = ["{:.2f}" for i in range(algebraic_formula.count("{}"))]
    numerical_formula = algebraic_formula.format(*slots)
    
    algebraic_fit = algebraic_formula.format(*variables)
    numerical_fit = numerical_formula.format(*fitted_parameters)
    
    print("Problem 3:\n")
    print("Model formula: {}\n".format(algebraic_fit))
    print("Fitted variables:")
    
    for variable in variables:
        
        print("  {} = {}".format(variable, eval(variable)))
    
    print("\nFitted formula = {}".format(numerical_fit))

main()
plt.show()