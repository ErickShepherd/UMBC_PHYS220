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

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         50
    Weight:         1.00
    Percentage:     50.00%
    
    Description:    How does the cloud reflectance vary with cloud optical
                    thickness and cloud single scattering albedo? To address 
                    this question, you need to simulate the reflectance for a 
                    variety of cloud optical thicknesses (0.1 to 20.0) and
                    single scattering albedos (e.g., 1.0, 0.9 and 0.8). Plot the
                    relation between reflectance and cloud optical thickness for
                    different value of single scattering albedo in the same 
                    plot. Write a short paragraph to explain your results.
"""

def question1():

    COTs = np.linspace(0.1, 20, 50)
    SSAs = np.asarray([1.0, 0.9, 0.8])
    SZA  = np.pi / 3

    plt.figure()

    loading_bar = LoadingBar(COTs.size * SSAs.size, "Question 1")
    
    for SSA in SSAs:

        P_reflected = []

        for COT in COTs:

            P_reflected.append(MCRT(COT, SSA, SZA, N_photons)["reflectance"])
            
            loading_bar.update()

        plt.plot(COTs, P_reflected, label = r"$\omega = {}$".format(SSA))
        
    xlabel = r"Cloud Optical Thickness ($\tau$)"
    ylabel = r"Cloud Reflectance ($R$)"
        
    plt.suptitle(r"{} vs. {}".format(ylabel, xlabel))
    plt.title("Simulated with {:,} Photons".format(N_photons))
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
    
    Description:    How deep can a photon travel into the cloud before it is
                    reflected assuming the sun is overhead (i.e., the solar 
                    zenith angle is zero) and cloud optical thickness is 10?
                    Track the path of every photon and record the deepest depth 
                    it descends into the cloud before it dies in the code. 
                    Analyze and plot the histogram of the max depth reached by 
                    those photons that are reflected for different single 
                    scattering albedo (1.0, 0.96, 0.92 and 0.88). Write a short
                    paragraph to explain your results.
"""

def question2():
    
    COT  = 10
    SSAs = np.asarray([0.88, 0.92, 0.96, 1.0])
    SZA  = 0
    
    # Author's note:
    #   The number of bins to use for the histogram. For a lower number of
    #   photons, I recommend using fewer bins.
    #    - Erick Shepherd
    bins = 50
    
    plt.figure()
    
    loading_bar = LoadingBar(SSAs.size, "Question 2")
    
    for index, SSA in enumerate(SSAs):
        
        label = r"$\omega = {}$".format(SSA)
        
        MDR_reflected = MCRT(COT, SSA, SZA, N_photons)["MDR reflected"]
        plt.hist(MDR_reflected, bins = bins, label = label, zorder = -index)
        
        loading_bar.update()
        
    xlabel = r"Deepest Depth Reached (${\tau}^{*}$)"
    ylabel = r"Photons Reflected (${N}_{ref}$)"
        
    plt.suptitle(r"{} vs. {}".format(ylabel, xlabel))
    plt.title("Simulated with {:,} Photons".format(N_photons))
    plt.xlabel(xlabel, fontsize = "large")
    plt.ylabel(ylabel, fontsize = "large")
    plt.xlim(0, COT)
    plt.grid()
  
# Test of solutions.
question1()
question2()
plt.show()