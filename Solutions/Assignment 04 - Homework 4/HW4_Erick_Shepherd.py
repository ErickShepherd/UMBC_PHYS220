#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 4, PHYS 220, UMBC.

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
    Assignment name:    Homework 4
    Available points:   100
    Grade percentage:   5.71%
    
    Description:        Simulating radiative transfer in clouds using the Monte
                        Carlo method.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
    E-mail:             ErickShepherd@UMBC.edu
    Date:               2018-04-09
    
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

# Local application imports.
# Let "Monte Carlo radiative transfer" be denoted by "MCRT".
from MCRT_Erick_Shepherd import MCRT_OOP, MCRT_procedural

# Author's note:
#   In the file MCRT.py, I have included both a procedural and an object
#   oriented approach to solving the Monte Carlo radiative transfer problem.
#   This MCRT variable is an alias for whichever function you whish to use in
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
#   results.
#    - Erick Shepherd
N_photons = 10000

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         50
    Weight:         1.00
    Percentage:     50.00%
    
    Description:    
"""

def question1():

    COTs = np.linspace(0.1, 20, 50)
    SSAs = [1.0, 0.9, 0.8]
    SZA  = np.pi / 3

    plt.figure()

    for SSA in SSAs:

        P_reflected = []

        for COT in COTs:

            P_reflected.append(MCRT(COT, SSA, SZA, N_photons)["reflectance"])

        plt.plot(COTs, P_reflected, label = r"$\omega = {}$".format(SSA))
        
    xlabel = r"Cloud Optical Thickness ($\tau$)"
    ylabel = r"Cloud Reflectance ($R$)"
        
    plt.suptitle(r"{} vs. {}".format(xlabel, ylabel))
    plt.title("Simulated with {} Photons".format(N_photons))
    plt.xlabel(xlabel, fontsize = "large")
    plt.ylabel(ylabel, fontsize = "large")
    plt.xlim(COTs[0], COTs[-1])
    plt.ylim(0, 1)
    plt.grid()

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         50
    Weight:         1.00
    Percentage:     50.00%
    
    Description:    
"""

def question2():
    
    COT  = 10
    SSAs = [0.88, 0.92, 0.96, 1.0]
    SZA  = 0
    
    plt.figure()
    
    for index, SSA in enumerate(SSAs):
        
        label = r"$\omega = {}$".format(SSA)
        
        MDR_reflected = MCRT(COT, SSA, SZA, N_photons)["MDR reflected"]
        plt.hist(MDR_reflected, bins = 50, label = label, zorder = -index)
        
    xlabel = r"Deepest Photon Depth (${\tau}^{*}$)"
    ylabel = r"Cloud Reflectance ($R$)"
        
    plt.suptitle(r"{} vs. {}".format(xlabel, ylabel))
    plt.title("Simulated with {} Photons".format(N_photons))
    plt.xlabel(xlabel, fontsize = "large")
    plt.ylabel(ylabel, fontsize = "large")
    plt.xlim(0, COT)
    plt.grid()
  
# Test of solutions.
question1()
question2()
plt.show()