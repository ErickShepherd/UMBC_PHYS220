#!/usr/bin/python
# coding=utf-8

"""
Solutions to the final project, PHYS 220, UMBC.

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
    Assignment:         08
    Assignment name:    Homework 7
    Available points:   100
    Grade percentage:   5.71%
    
    Description:        Integration of ordinary differential equations in
                        Python.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-05-18
    
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

from scipy.integrate import odeint

def main():
    
    problem1()
    problem2()
    problem3()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         30
    Weight:         0.909
    Percentage:     27.27%
    
    Description:    
                    
                    See "Homework 7.pdf" for more information.
"""

# Physical constants:
rho = 1.25   # Density of air.           Unit(s): kg / m^3
g   = 9.807  # Earth's gravity constant. Unit(s): m / s^2

# Properties of the golf ball:
A   = 0.0379 # Cross-sectional area.     Unit(s): m^2
m   = 0.043  # Mass.                     Unit(s): kg
C   = 0.25   # Drag coefficient.         Unit(s): (dimensionless)

def gravitational_force():
    
    return -m * g

def drag_force(v, rho):
    
    v_unit = abs(v) / v if v != 0 else 0 # Unit vector of velocity.
    
    return -(1 / 2) * rho * C * A * v ** 2 * v_unit

def net_force(v, rho):
    
    return gravitational_force() + drag_force(v, rho)

def net_acceleration(v, rho):
    
    return net_force(v, rho) / m

def trajectory_tendency(state_vector, t, rho):
    
    y = state_vector[0]
    v = state_vector[1]
    a = net_acceleration(v, rho)
    
    return [v, a]

def trajectory(y0, v0, rho):
    
    state_vector = [y0, v0]
    
    t = np.linspace(0, 10, 1000)
    
    results = odeint(trajectory_tendency, state_vector, t, args = (rho,))
    
    y = results[:, 0]
    v = results[:, 1]
    
    return {"t":t, "y":y, "v":v}

def terminal_velocity(v, tolerance = 1e-6):
    
    for i in range(len(v[:-1])):
        
        if abs(v[i] - v[i + 1]) < tolerance:
            
            return v[i]
        
    return None

def problem1():
    
    y0 = 0.0 # Unit(s): m
    v0 = 0.0 # Unit(s): m / s
    
    drag     = trajectory(y0, v0, rho)
    dragless = trajectory(y0, v0, 0)
    
    mask = (0 <= drag["t"]) & (drag["t"] <= 4)
    
    plt.figure()
    plt.title("Problem 1")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Vertical Position [$m$]")
    
    plt.plot(drag["t"][mask], drag["y"][mask],    
             c = "r", label = "With drag")
    
    plt.plot(dragless["t"][mask], dragless["y"][mask], 
             c = "b", label = "Without drag")
    
    plt.xlim(0, 4)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    output_string = "The terminal velocity is {:.2f} meters per second."
        
    print("-" * 80 + "\n")
    print("Problem 1:\n")
    print(output_string.format(terminal_velocity(drag["v"])))
    print("\n" + "-" * 80 + "\n")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         40
    Weight:         0.909
    Percentage:     36.36%
    
    Description:    
                    
                    See "Homework 7.pdf" for more information.
"""

def fractional_error(t, E, f):
    
    A = f(t)
    
    return np.abs(A - E) / np.abs(A)

def euler(t0, tf, h, functions, initial_conditions):
    
    if not isinstance(functions, np.ndarray):
        functions = np.array(functions, ndmin = 1)
        
    if not isinstance(initial_conditions, np.ndarray):
        initial_conditions = np.array(initial_conditions, ndmin = 1)
    
    if functions.shape != initial_conditions.shape:
        
        error_message = "functions and initial conditions must have same " + \
                        "first dimension, but have shapes {} and {}"
        
        raise ValueError(error_message.format(functions.shape, 
                                              initial_conditions.shape))
    
    t = [t0]
    N = [[N0] for N0 in initial_conditions]
    
    while t[-1] < tf:
        
        t.append(t[-1] + h)
        
        for i, f in enumerate(functions):
            
            args = [N[j][-1] for j in range(i + 1)]
            
            N[i].append(f(*args, h))
        
    return (np.asarray(t),) + tuple(np.asarray(n) for n in N)

def problem2a():
    
    # Initial conditions:
    tau = 2.0   # Mean life time.        Unit(s): s
    N0  = 100.0 # Initial concentration. Unit(s): dimensionless percentage

    # Time domain:
    t0 =  0.0 # Initial time. Unit(s): s
    tf = 15.0 # Final time.   Unit(s): s

    # Analytical solution:
    analytical_function = lambda t: N0 * np.exp(-t / tau)

    N = lambda N_n, h: N_n - (N_n / tau) * h
    
    # Results of case 1:
    h1     = 1.0  # Change in time. Unit(s): s
    t1, N1 = euler(t0, tf, h1, N, N0)
    error1 = fractional_error(t1, N1, analytical_function)
    
    # Results of case 2:
    h2     = 0.1  # Change in time. Unit(s): s
    t2, N2 = euler(t0, tf, h2, N, N0)
    error2 = fractional_error(t2, N2, analytical_function)
    
    # Results of case 3:
    h3     = 0.01 # Change in time. Unit(s): s
    t3, N3 = euler(t0, tf, h3, N, N0)
    error3 = fractional_error(t3, N3, analytical_function)
    
    plt.figure()
    plt.title("Problem 2(a) - Values")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Nuclei [$\%$]")
    plt.plot(t1, N1, label = r"$h={}$".format(h1))
    plt.plot(t2, N2, label = r"$h={}$".format(h2))
    plt.plot(t3, N3, label = r"$h={}$".format(h3))
    plt.xlim(t0, tf)
    plt.ylim(0, 100)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    plt.figure()
    plt.title("Problem 2(a) - Fractional Error")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Error [$\%$]")
    plt.plot(t1, error1, label = r"$h={}$".format(h1))
    plt.plot(t2, error2, label = r"$h={}$".format(h2))
    plt.plot(t3, error3, label = r"$h={}$".format(h3))
    plt.xlim(t0, tf)
    plt.ylim(0, 1)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
def problem2b():
    
    # Initial conditions:
    tau_P  =   2.0
    tau_Ds =   2.0 * np.logspace(-2, 2, 3, base = 10)
    P0     = 100.0
    D0     =   0.0

    # Time domain:
    t0 =  0.0  # Initial time.   Unit(s): s
    tf = 15.0  # Final time.     Unit(s): s
    h  =  0.01 # Time step size. Unit(s): s

    P = lambda N_P, h: N_P - h * (N_P / tau_P)
    
    label_parent   = r"Parent isotope: ${{\tau}}_{{P}}={}\ s$"
    label_daughter = r"Daughter isotope: ${{\tau}}_{{D}}={}\ s$"
    
    plt.figure()
    plt.title("Problem 2(b)")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Nuclei [$\%$]")
    
    for tau_D in tau_Ds:
        
        D = lambda N_P, N_D, h: N_D + h * ((N_P / tau_P) - (N_D / tau_D))
    
        t, N_P, N_D = euler(t0, tf, h, [P, D], [P0, D0])
    
        plt.plot(t, N_D, label = label_daughter.format(tau_D))
        
    plt.plot(t, N_P, label = label_parent.format(tau_P))
    plt.xlim(t0, tf)
    plt.ylim(0, 100)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()

def problem2():
    
    problem2a()
    problem2b()
    
"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         40
    Weight:         0.909
    Percentage:     36.36%
    
    Description:    
                    
                    See "Homework 7.pdf" for more information.
"""

def angular_acceleration(theta, omega, omega0, xi):
    
    return -2 * xi * omega0 * omega - omega0 ** 2 * theta

def oscillator_tendency(state_vector, t, omega0, xi):
    
    theta = state_vector[0]
    omega = state_vector[1]
    alpha = angular_acceleration(theta, omega, omega0, xi)
    
    return [omega, alpha]

def periodicity(theta0, omega0, xi):
    
    state_vector = [theta0, omega0]
    
    t = np.linspace(0, 10, 1000)
    
    results = odeint(oscillator_tendency, state_vector, t, args = (omega0, xi))
    
    theta = results[:, 0]
    omega = results[:, 1]
    
    return {"t":t, "theta":theta, "omega":omega}

def problem3():
    
    theta0 = 1.0
    omega0 = 2.0 * np.pi
    
    xis = {0.0: r"Undamped: ${{\xi}}={}$",
           0.2: r"Underdamped: ${{\xi}}={}$", 
           1.0: r"Critically damped: ${{\xi}}={}$", 
           5.0: r"Overdamped: ${{\xi}}={}$"}
    
    plt.figure()
    plt.title("Problem 3")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Displacement [$m$]")
    
    for xi in xis:
        
        data = periodicity(theta0, omega0, xi)
        
        plt.plot(data["t"], data["theta"], label = xis[xi].format(xi))
    
    plt.xlim(0, 10)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()

main()
plt.show()