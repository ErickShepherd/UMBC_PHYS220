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
    Assignment:         06
    Assignment name:    Final Project
    Available points:   100
    Grade percentage:   30.0%
    
    Description:        Integration of ordinary differential equations in
                        Python.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-05-14
    
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

# Physical constants:
rho = 1.25              # Density of air.           Unit(s): kg / m^3
g   = 9.807             # Earth's gravity constant. Unit(s): m / s^2

# Properties of the golf ball:
r   = 0.023             # Radius.                   Unit(s): m
A   = np.pi * (r ** 2)  # Cross-sectional area.     Unit(s): m^2
m   = 0.046             # Mass.                     Unit(s): kg
C   = 0.5               # Drag coefficient.         Unit(s): (dimensionless)

# Tedencies of the golfer:
v_mean = 50.0           # Mean ball velocity.       Unit(s): m / s
v_std  =  5.0           # Standard deviation.       Unit(s): m / s

# Properties of the golf green air:
rho_mean = 1.25         # Density of air.           Unit(s): kg / m^3
rho_std  = 0.1          # Standard deviation.       Unit(s): kg / m^3

def net_velocity(vx, vy):
    
    v     = np.sqrt(vx ** 2 + vy ** 2)
    theta = np.arctan(vy / vx)
    
    return v, theta

def component_velocity(v, theta):
    
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)
    
    return vx, vy

def gravitational_force():
    
    Fx = 0
    Fy = -m * g
    
    return Fx, Fy

def D(rho):
    
    return 0.5 * rho * C * A

def drag_force(vx, vy, rho):
    
    v, theta = net_velocity(vx, vy)
    
    Fx = -D(rho) * v * vx
    Fy = -D(rho) * v * vy
    
    return Fx, Fy

def net_force(vx, vy, rho):
    
    Fx_gravitational, Fy_gravitational = gravitational_force()
    Fx_drag,          Fy_drag          = drag_force(vx, vy, rho)
        
    Fx = Fx_gravitational + Fx_drag
    Fy = Fy_gravitational + Fy_drag
    
    return Fx, Fy

def net_acceleration(vx, vy, rho):
    
    Fx, Fy = net_force(vx, vy, rho)
    
    ax = Fx / m
    ay = Fy / m
    
    return ax, ay

def tendency_function(state_vector, t, rho):
    
    x, y, vx, vy = state_vector
    ax, ay       = net_acceleration(vx, vy, rho)
    
    return [vx, vy, ax, ay]

def trajectory(v0, theta0, rho):
    
    x0           = 0 # Unit(s): m
    y0           = 0 # Unit(s): m
    vx0, vy0     = component_velocity(v0, theta0)
    state_vector = [x0, y0, vx0, vy0]
    
    t = np.linspace(0, 10, 500)
    
    results = odeint(tendency_function, state_vector, t, args = (rho,))
    
    x  = results[:, 0]
    y  = results[:, 1]
    vx = results[:, 2]
    vy = results[:, 3]
    
    condition = np.where(y >= 0)
    
    t  = t[condition]
    x  = x[condition]
    y  = y[condition]
    vx = vx[condition]
    vy = vy[condition]
    
    return {"t":t, "x":x, "y":y, "vx":vx, "vy":vy}

def main():
    
    #problem1()
    #problem2()
    problem3()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         30
    Weight:         1.00
    Percentage:     30.00%
    
    Description:    
                    
                    See "Final Project_updated.pdf" for more information.
"""

def problem1():
    
    v0     = 50.0             # m / s
    theta0 = np.radians(35.0) # radians
    
    drag     = trajectory(v0, theta0, rho)
    dragless = trajectory(v0, theta0, 0)
    
    dx = 50
    x_lower_bound = np.floor(np.min(dragless["x"]) / dx) * dx
    x_upper_bound = np.ceil(np.max(dragless["x"]) / dx) * dx
    
    dy = 10
    y_lower_bound = np.floor(np.min(dragless["y"]) / dy) * dy
    y_upper_bound = np.ceil(np.max(dragless["y"]) / dy) * dy
    
    dt = 1
    t_lower_bound = np.floor(np.min(dragless["t"]) / dt) * dt
    t_upper_bound = np.ceil(np.max(dragless["t"]) / dt) * dt
    
    spatial_lower_bound = max([x_lower_bound, y_lower_bound])
    spatial_upper_bound = max([x_upper_bound, y_upper_bound])
    
    plt.figure()
    plt.title("Problem 1 - Figure 1")
    plt.xlabel(r"Horizontal Position [$m$]")
    plt.ylabel(r"Vertical Position [$m$]")
    plt.plot(drag["x"],     drag["y"],     c = "r", label = "With drag")
    plt.plot(dragless["x"], dragless["y"], c = "b", label = "Without drag")
    plt.xlim(x_lower_bound, x_upper_bound)
    plt.ylim(y_lower_bound, y_upper_bound)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    plt.figure()
    plt.suptitle("Problem 1 - Figure 1")
    plt.title("Scaled to Perspective")
    plt.xlabel(r"Horizontal Position [$m$]")
    plt.ylabel(r"Vertical Position [$m$]")
    plt.plot(drag["x"],     drag["y"],     c = "r", label = "With drag")
    plt.plot(dragless["x"], dragless["y"], c = "b", label = "Without drag")
    plt.xlim(spatial_lower_bound, spatial_upper_bound)
    plt.ylim(spatial_lower_bound, spatial_upper_bound)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.gca().set_aspect("equal", adjustable = "box")
    plt.grid()
    plt.legend()
    
    plt.figure()
    plt.title("Problem 1 - Figure 2")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Vertical Position [$m$]")
    plt.plot(drag["t"],     drag["y"],     c = "r", label = "With drag")
    plt.plot(dragless["t"], dragless["y"], c = "b", label = "Without drag")
    plt.xlim(t_lower_bound, t_upper_bound)
    plt.ylim(y_lower_bound, y_upper_bound)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    plt.figure()
    plt.title("Problem 1 - Figure 3")
    plt.xlabel(r"Time [$s$]")
    plt.ylabel(r"Horizontal Position [$m$]")
    plt.plot(drag["t"],     drag["x"],     c = "r", label = "With drag")
    plt.plot(dragless["t"], dragless["x"], c = "b", label = "Without drag")
    plt.xlim(t_lower_bound, t_upper_bound)
    plt.ylim(x_lower_bound, x_upper_bound)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend()
    
    final_x_with_drag    = drag["x"][-1]
    final_x_without_drag = dragless["x"][-1]
    
    output_string = "The final horizontal position {} air resistance is " + \
                    "{:.2f} meters."
        
    print("-" * 80 + "\n")
    print("Problem 1:\n")
    print(output_string.format("with",    final_x_with_drag))
    print(output_string.format("without", final_x_without_drag))
    print("\n" + "-" * 80 + "\n")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         30
    Weight:         1.00
    Percentage:     30.00%
    
    Description:    
                    
                    See "Final Project_updated.pdf" for more information.
"""

def problem2():
    
    v0      = 50.0 # m / s
    theta0s = np.linspace(1, 90, 100)
    
    x_finals_with_drag    = []
    x_finals_without_drag = []
    
    for theta0 in theta0s:
    
        theta0 = np.radians(theta0)
    
        drag     = trajectory(v0, theta0, rho)
        dragless = trajectory(v0, theta0, 0) 
        
        x_finals_with_drag.append(drag["x"][-1])
        x_finals_without_drag.append(dragless["x"][-1])
    
    max_distance_with_drag    = max(x_finals_with_drag)
    max_distance_without_drag = max(x_finals_without_drag)
    
    index_with_drag    = x_finals_with_drag.index(max_distance_with_drag)
    index_without_drag = x_finals_without_drag.index(max_distance_without_drag)
    
    optimal_theta_with_drag    = theta0s[index_with_drag]
    optimal_theta_without_drag = theta0s[index_without_drag]
    
    output_string = "The optimal elevation angle {} air resistance is " + \
                    "{:.2f} degrees, which\nyields a distance of {:.2f} " + \
                    "meters.\n"
        
    print("Problem 2:\n")
    
    print(output_string.format("with", 
                               optimal_theta_with_drag, 
                               max_distance_with_drag))
    
    print(output_string.format("without", 
                               optimal_theta_without_drag, 
                               max_distance_without_drag))
    
    print("-" * 80 + "\n")
    
    xticks = [1] + list(range(10, 90 + 1, 10))
    label_drag     = r"With drag: ${{\theta}}_{{op}}={:.2f}^{{\circ}}$"
    label_dragless = r"Without drag: ${{\theta}}_{{op}}={:.2f}^{{\circ}}$"
        
    dxf = 50
    xf_lower_limit = np.floor(np.min(x_finals_without_drag) / dxf) * dxf
    xf_upper_limit = np.ceil(np.max(x_finals_without_drag) / dxf) * dxf
        
    plt.figure()
    plt.title("Problem 2")
    plt.xlabel(r"${\theta}_{0}$ [$deg$]")
    plt.ylabel(r"${x}_{f}$ [$m$]")
    
    plt.plot(theta0s, x_finals_with_drag,    c = "r", 
             label = label_drag.format(optimal_theta_with_drag))
    
    plt.axvline(optimal_theta_with_drag, color = "r", ls = "--")
    
    plt.plot(theta0s, x_finals_without_drag, c = "b", 
             label = label_dragless.format(optimal_theta_without_drag))
    
    plt.axvline(optimal_theta_without_drag, color = "b", ls = "--")
    
    plt.xlim(np.floor(np.min(theta0s)), np.ceil(np.max(theta0s)))
    plt.ylim(xf_lower_limit, xf_upper_limit)
    plt.xticks(xticks)
    plt.axhline(0, color = "k")
    plt.axvline(0, color = "k")
    plt.grid()
    plt.legend(loc = 1)

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    
                    
                    See "Final Project_updated.pdf" for more information.
"""

def problem3():
    
    theta0 = np.radians(35.0)
    
    number_of_swings = 100000
    
    velocities    = np.random.normal(v_mean,   v_std,   number_of_swings)
    air_densities = np.random.normal(rho_mean, rho_std, number_of_swings)
    
    pairs = zip(velocities, air_densities)
    
    x_finals = []
    
    for pair in pairs:
        
        v0  = pair[0]
        rho = pair[1]
        
        results = trajectory(v0, theta0, rho)

        x_finals.append(results["x"][-1])
        
    x_finals = np.asarray(x_finals)
        
    expectation_value = np.mean(x_finals)
    x_mean = expectation_value
    x_std  = np.std(x_finals)
    
    within_1_meter = x_finals[(x_mean - 1 <= x_finals) & (x_finals <= x_mean + 1)]
    
    probability_within_1_meter = within_1_meter.size / number_of_swings
    percent_within_1_meter     = probability_within_1_meter * 100
        
    label_distribution = r"$x_f$ over ${:,}$ swings".format(number_of_swings)
    label_expectation  = r"$\^{{x_f}} = {:.2f} m$".format(expectation_value)
    label_interval     = r"$P({:.2f}\pm1 m) = {:.2f}\%$".format(expectation_value, 
                                                                percent_within_1_meter)
        
    plt.figure()
    plt.title("Problem 3")
    plt.xlabel(r"${x}_{f}$ [$m$]")
    plt.ylabel(r"Probability")
    
    plt.hist(x_finals, bins = 100, normed = True,
             color = "b", label = label_distribution)
    
    plt.axvspan(x_mean - 1, x_mean + 1, alpha = 0.5, 
                color = "r", label = label_interval)
    
    plt.axvline(expectation_value, 
                color = "r", label = label_expectation)
    
    plt.xlim(x_mean - 3 * x_std, x_mean + 3 * x_std)
    plt.grid()
    plt.legend(loc = 1)
    
    output_string_1 = "The expectation value is <x_f> = {:.2f} meters.\n"
    output_string_2 = "The probability of the ball landing within 1 meter " + \
                      "of the expectation value is\n{:.4f} ({:.2f}%).\n"
    
    print("Problem 3:\n")
    
    print(output_string_1.format(expectation_value))
    
    print(output_string_2.format(probability_within_1_meter, 
                                 percent_within_1_meter))
    
    print("-" * 80)

main()
plt.show()