#!/usr/bin/python
# coding=utf-8

"""
Solutions to the midterm, PHYS 220, UMBC.

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
    Assignment:         05
    Assignment name:    Midterm
    Available points:   100
    Grade percentage:   30%
    
    Description:        Numerical integration using the Trapezoidal Rule and
                        Simpson's Rule, and the applications thereof.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-04-10
    
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
from __future__ import division

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
#   of accuracy and runtime.
#    - Erick Shepherd
N_photons = 10000

def get_absolute_error(measured_value, actual_value):
    
    return abs(measured_value - actual_value)

def get_relative_error(measured_value, actual_value):
    
    numerator   = get_absolute_error(measured_value, actual_value)
    denominator = abs(actual_value)
    
    return numerator / denominator

def get_percent_error(measured_value, actual_value):
    
    return get_relative_error(measured_value, actual_value) * 100

def get_errors(measured_value, actual_value):
    
    absolute_error = get_absolute_error(measured_value, actual_value)
    relative_error = get_relative_error(measured_value, actual_value)
    percent_error  = get_percent_error(measured_value, actual_value)
    
    return absolute_error, relative_error, percent_error

# Author's note:
#   These lambda functions are used in both problem 2 and problem 3, which is 
#   why they are outside of either function's definition.
#    - Erick Shepherd
C_0      = 0.04
k        = 0.2
P        = lambda tau: C_0 * tau * np.exp(-k * tau)
tau_mean = lambda tau: tau * P(tau)
tau_min  = 0.1
tau_max  = 50.0

# Let "analytical mean cloud optical thickness" be denoted by "AMCOT".
AMCOT = (1 / 25) * (255.05 / np.exp(0.02) - 15250 / np.exp(10))

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         30
    Weight:         1.00
    Percentage:     30.00%
    
    Description:    Define two new functions, "trapz" and "simps", which
                    numerically compute the definite integral of a given
                    function using the Trapezoidal Rule and Simpson's Rule
                    respectively, then use each function to integrate
                    f(x) = x^4 - 2x + 1 over the interval from 0 to 2.
"""

# Solution 1(a):
def trapz(func, a, b, N):
    
    """
    Numerical integration via the Trapezoidal Rule.
    """
    
    # Author's note:
    #   First attempt to integrate the numpy.ndarray directly. If that fails,
    #   integrate iteratively.
    #    - Erick Shepherd
    k = np.linspace(1, N - 1, N - 1, endpoint = True)
    h = (b - a) / N
    A = (1 / 2) * (func(a) + func(b))

    try:
        
        A += np.sum(func(a + k * h))

    except:
        
        for i in k:
            A += func(a + i * h)
            
    A *= h
    
    return A

def simps(func, a, b, N):
    
    """
    Numerical integration via Simpson's Rule.
    """
    
    k = np.linspace(1, N // 2, N // 2, endpoint = True)
    h = (b - a) / N
    A = func(a) + func(b)
    
    # Author's note:
    #   First attempt to integrate the numpy.ndarray directly. If that fails,
    #   integrate iteratively.
    #    - Erick Shepherd
    try:
        
        A += 4 * np.sum(func(a + (2 * k - 1) * h))
        A += 2 * np.sum(func(a + 2 * k[:-1] * h))
        
    except:
    
        for index, i in enumerate(k):

            A += 4 * func(a + (2 * i - 1) * h)

            if index < k.size - 1:
                A += 2 * f(unca + 2 * i * h)
                
    A *= h / 3
        
    return A

# Solution 1(b):
f = lambda x: x ** 4 - 2 * x + 1

def problem1():
    
    def get_output_fields(intervals, analytical_integral, numerical_integral):
        
        interval_string        = "Number of intervals: {}"
        analytical_area_string = "Analytical area:     {}"
        numerical_area_string  = "Numerical area:      {}"
        absolute_error_string  = "Absolute error:      {}"
        relative_error_string  = "Relative error:      {}"
        percent_error_string   = "Percent error:       {}%"
        
        errors = get_errors(numerical_integral, analytical_integral)
        
        fields = (interval_string.format(intervals),
                  analytical_area_string.format(analytical_integral),
                  numerical_area_string.format(numerical_integral),
                  absolute_error_string.format(errors[0]),
                  relative_error_string.format(errors[1]),
                  percent_error_string.format(errors[2]))
        
        return fields
    
    def indent_output_fields(fields, spaces):

        indentation = spaces * " "

        return (indentation + field for field in fields)
    
    # Let "analytical definite integral" be denoted by "ADI".
    ADI         = 4.4
    N_intervals = np.asarray([10, 100, 1000])
    
    trapz_integrals = []
    simps_integrals = []

    for index, N in enumerate(N_intervals):
        
        trapz_integrals.append(get_output_fields(N, ADI, trapz(f, 0, 2, N)))
        simps_integrals.append(get_output_fields(N, ADI, simps(f, 0, 2, N)))
        
    print("Trapezoidal rule:\n")
    
    for integral in trapz_integrals:
        
        print(*indent_output_fields(integral, 2), sep = "\n", end = "\n\n")
    
    print("Simpson's rule:\n")
    
    for integral in trapz_integrals:

        print(*indent_output_fields(integral, 2), sep = "\n", end = "\n\n")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         30
    Weight:         1.00
    Percentage:     30.00%
    
    Description:    Integrate the product of the probability density function
                    of cloud optical thickness and the cloud optical thickness
                    to compute the mean cloud optical thickness.
                    
                    See the file "midterm.pdf" for more detail.
"""

def problem2():

    trapz_intervals = []
    simps_intervals = []
    trapz_taus      = []
    simps_taus      = []
    trapz_error     = 100
    simps_error     = 100
    trapz_N         = 2
    simps_N         = 2
    
    while trapz_error > 1:
        
        trapz_N += 2
        A = trapz(tau_mean, tau_min, tau_max, trapz_N)
        trapz_error = get_percent_error(A, AMCOT)
        trapz_intervals.append(trapz_N)
        trapz_taus.append(A)
    
    while simps_error > 1:

        simps_N += 2
        A = simps(tau_mean, tau_min, tau_max, simps_N)
        simps_error = get_percent_error(A, AMCOT)
        simps_intervals.append(simps_N)
        simps_taus.append(A)

    output = "{0} converged to {1:.2f} with a {2:.2f}% error from the " + \
             "analytical solution {3:.2f} after {4} intervals."
        
    trapz_fields = ("Trapezoidal method", trapz_taus[-1], 
                    trapz_error, AMCOT, trapz_N)
    
    simps_fields = ("Simpson's method", simps_taus[-1],  
                    simps_error, AMCOT, simps_N)
    
    print(output.format(*trapz_fields))
    print(output.format(*simps_fields))

    Ns           = np.arange(4, 31, 2)
    trapz_taus   = np.zeros(Ns.size)
    simps_taus   = np.zeros(Ns.size)
    trapz_errors = np.zeros(Ns.size)
    simps_errors = np.zeros(Ns.size)
    
    # Let "analytical domain" and "analytical range" be denote by "AD" and "AR" 
    # respectively,
    AD = np.arange(0, Ns[-1] + 1)
    AR = np.asarray([AMCOT for n in AD])

    for i, N in enumerate(Ns):

        trapz_taus[i]   = trapz(tau_mean, tau_min, tau_max, N)
        simps_taus[i]   = simps(tau_mean, tau_min, tau_max, N)
        trapz_errors[i] = get_relative_error(trapz_taus[i], AMCOT)
        simps_errors[i] = get_relative_error(simps_taus[i], AMCOT)

    plt.figure()
    plt.plot(AD, AR, label = "Analytical Integral", ls = "--", c = "r")
    plt.plot(Ns, trapz_taus, label = "Trapezoidal Rule")
    plt.plot(Ns, simps_taus, label = "Simpson's Rule")
    plt.title("Mean Cloud Optical Thickness vs. Number of Intervals")
    plt.xlabel(r"Number of Intervals ($N$)")
    plt.ylabel(r"Mean Cloud Optical Thickness (${\langle}{\tau}{\rangle}$)")
    plt.xlim(0, Ns[-1])
    plt.ylim(8.5, 11)
    plt.legend()
    plt.grid()
    
    plt.figure()
    plt.plot(Ns, trapz_errors, label = "Trapezoidal Error")
    plt.plot(Ns, simps_errors, label = "Simpson's Error")
    plt.title("Relative Error vs. Number of Intervals")
    plt.xlabel(r"Number of Intervals ($N$)")
    plt.ylabel(r"Relative Error ($\eta$)")
    plt.xlim(0, Ns[-1])
    plt.ylim(0, 0.15)
    plt.legend()
    plt.grid()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    Numerically integrate the product of the Monte Carlo 
                    reflectance function and the probability density function
                    from problem 2 to compute the mean reflectance of the cloud.
                    Plot the results as a function of two parameters: The number
                    of photons used in the Monte Carlo model, and the number of
                    intervals used in the numerical integration.
                    
                    See the file "midterm.pdf" for more detail.
"""

def problem3():
    
    def mean_R(N_photons = 1000):
    
        SSA = 1.0
        SZA = 45 * np.pi / 180
    
        R = lambda COT: MCRT(COT, SSA, SZA, N_photons)
    
        return lambda COT: R(COT)["reflectance"] * P(COT)

    # Let "list of number of photons" be denoted by "LPP", let "list of number 
    # of intervals" be denoted by "LIP", and let "reflectances" be denoted by
    # "REFs".
    LPP  = np.logspace(1,  3, 10, dtype = int)
    LIP  = np.linspace(2, 20, 10, dtype = int)
    REFs = np.zeros((LPP.size, LIP.size))
    
    N_iterations = LPP.size * LIP.size
    loading_bar  = LoadingBar(N_iterations, "Problem 3")
    
    # Let "mark three thirds", "mark two thirds", and "mark one third" be
    # denoted by "M33D", "M23D", and "M13D" respectively, with the suffix "I" 
    # indicating "intervals" and the suffix "P" indicating the number of
    # photons.
    M33DI = -1
    M23DI = -LIP.size // 3
    M13DI = -LIP.size // 3 * 2
    M33DP = -1
    M23DP = -LPP.size // 3
    M13DP = -LPP.size // 3 * 2
    
    for i, N_photons in enumerate(LPP):
        
        for j, N_intervals in enumerate(LIP):

            REFs[i, j] = trapz(mean_R(N_photons), tau_min, 
                                       tau_max, N_intervals)

            loading_bar.update()
    
    # Author's note:
    #   The assignment calls for plotting mean reflectance as a function of two
    #   parameters: The number of intervals used in the intergration and the
    #   number of photons used in the Monte Carlo simulation. There are three
    #   possible ways to approach this: First, you could simply plot a contour
    #   or other color plot where the x and y-axes are the two parameters and
    #   the mean reflectance is the color intensity; second, you could plot the
    #   reflectance vs. the number of intervals for several constant numbers of 
    #   photons; third, you could plot the reflectance vs. the number of photons
    #   for several constant numbers of intervals. All three approaches are
    #   shown.
    #    - Erick Shepherd
    
    plt.figure()
    plt.suptitle("Mean Cloud Reflectance")
    plt.title("vs. Number of Photons vs. Number of Intervals")
    plt.xlabel(r"Number of Intervals ($N$)")
    plt.ylabel(r"Number of Photons ($N_{\gamma}$)")
    plt.pcolor(LIP, LPP, REFs, cmap = "hot")
    plt.clim(0, 1)
    plt.colorbar()
    
    plt.figure()
    plt.title("Mean Cloud Reflectance vs. Number of Intervals")
    plt.xlabel(r"Number of Intervals ($N$)")
    plt.ylabel(r"Mean Cloud Reflectance (${\langle}{R}{\rangle}$)")
    plt.plot(LIP, REFs[M33DP, :], label = "{} photons".format(LPP[M33DP]))
    plt.plot(LIP, REFs[M23DP, :], label = "{} photons".format(LPP[M23DP]))
    plt.plot(LIP, REFs[M13DP, :], label = "{} photons".format(LPP[M13DP]))
    plt.xlim(LIP[0], LIP[-1])
    plt.ylim(0, 1)
    plt.legend()
    plt.grid()
    
    plt.figure()
    plt.title("Mean Cloud Reflectance vs. Number of Photons")
    plt.xlabel(r"Number of Photons ($N_{\gamma}$)")
    plt.ylabel(r"Mean Cloud Reflectance (${\langle}{R}{\rangle}$)")
    plt.plot(LPP, REFs[:, M33DI], label = "{} intervals".format(LIP[M33DI]))
    plt.plot(LPP, REFs[:, M23DI], label = "{} intervals".format(LIP[M23DI]))
    plt.plot(LPP, REFs[:, M13DI], label = "{} intervals".format(LIP[M13DI]))
    plt.xlim(LPP[0], LPP[-1])
    plt.ylim(0, 1)
    plt.legend()
    plt.grid()
    
problem1()
problem2()
problem3()
plt.show()
