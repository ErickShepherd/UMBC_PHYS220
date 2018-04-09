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
import numpy as np
import matplotlib.pyplot as plt

# Author's note:
#   This is the photon class for the object oriented programming (OOP) approach
#   to solving this problem. There is also a procedural solution near the bottom
#   of this document.
#    - Erick Shepherd
class Photon:
    
    """
    An energy packet of light.
    """
    
    created   = 0
    
    count     = {"absorbed"    : 0,
                 "reflected"   : 0,
                 "transmitted" : 0}
    
    max_depth = {"absorbed"    : [],
                 "reflected"   : [],
                 "transmitted" : []}
    
    def __init__(self, COT = 0, SSA = 0, SZA = 0):
        
        """
        The constructor for Photon objects.
        """
        
        Photon.created += 1
        
        self.COT     = COT   # Cloud optical thickness.
        self.SSA     = SSA   # Single scattering albedo.
        self.theta   = SZA   # Scattering angle; initially solar zenith angle.
        self.tau     = 0     # Position relative to the top of the cloud.
        self.tau_max = 0     # Maximum depth reached by the photon.
        self.dead    = False # Whether the photon has been terminated.
        
        self.enter_cloud() # Photon enters the cloud.
        
        # Photon scatters until termination.
        while not self.dead:
            self.scatter()
        
    @staticmethod
    def absorbance():
        
        return Photon.count["absorbed"] / Photon.created
            
    def die(self, fate):
        
        Photon.count[fate] += 1
        Photon.max_depth[fate].append(self.tau_max)
        self.dead = True
            
    def enter_cloud(self):
        
        """
        The photon initially enters the cloud at the solar zenith angle to some
        random depth.
        """
        
        xi =  np.random.random()
        L  = -np.log(1 - xi)
        
        self.tau     = L * np.cos(self.theta)
        self.tau_max = self.tau
        
    @staticmethod
    def reflectance():
        
        return Photon.count["reflected"] / Photon.created
        
    @staticmethod
    def reset():
        
        """
        Resets the class variables.
        """
        
        Photon.created = 0
        
        Photon.count["absorbed"]    = 0
        Photon.count["reflected"]   = 0
        Photon.count["transmitted"] = 0
        
        Photon.max_depth["absorbed"]    = []
        Photon.max_depth["reflected"]   = []
        Photon.max_depth["transmitted"] = []
        
    def scatter(self):
        
        """
        The photon has struck a particle in the cloud.
        """
        
        xi        =  np.random.random() # Random walk variable.
        L         = -np.log(1 - xi)     # Scattering length.
        mu        = 2 * xi - 1         
        theta_new = np.arccos(mu)       # Scattering angle from path.
        
        self.theta += theta_new # New direction of motion.
        
        if xi <= self.SSA:
                
            tau_new = self.tau + L * np.cos(self.theta)

            if tau_new > self.tau_max and tau_new <= self.COT:
                self.tau_max = tau_new

            self.tau = tau_new

            if self.tau < 0:
                self.die("reflected")
            elif self.tau > self.COT:
                self.die("transmitted")

        else:

            self.die("absorbed")
        
    @staticmethod
    def transmittance():
        
        return Photon.count["transmitted"] / Photon.created
            
def MCRT_OOP(COT, SSA, SZA, N_photons):
    
    """
    An object oriented Monte Carlo radiative transfer model.
    """
    
    for photon in range(N_photons):
                
        Photon(COT, SSA, SZA)
        
    N_reflected     = Photon.count["reflected"]
    N_absorbed      = Photon.count["absorbed"]
    N_transmitted   = Photon.count["transmitted"]
    reflectance     = Photon.reflectance()
    absorbance      = Photon.absorbance()
    transmittance   = Photon.transmittance()
    MDR_reflected   = Photon.max_depth["reflected"]
    MDR_absorbed    = Photon.max_depth["absorbed"]
    MDR_transmitted = Photon.max_depth["transmitted"]
        
    Photon.reset()
    
    return {"reflected"       : N_reflected,
            "absorbed"        : N_absorbed,
            "transmitted"     : N_transmitted,
            "reflectance"     : reflectance,
            "absorbance"      : absorbance,
            "transmittance"   : transmittance,
            "MDR reflected"   : MDR_reflected,
            "MDR absorbed"    : MDR_absorbed,
            "MDR transmitted" : MDR_transmitted}
    
def MCRT_procedural(COT, SSA, SZA, N_photons):
    
    """
    A procedural Monte Carlo radiative transfer model.
    
    Arguments:
    ----------
        COT:        int/float,  cloud optical thickness.
        SZA:        int/float,  solar zenith angle.
        SSA:        int/float,  single scattering albedo.
        N_photons:  int,        number of photons.
        
    Returns:
    --------
        A dictionary of values from which the desired physical quantity may be
        extracted by name.
    """
    
    N_reflected   = 0
    N_absorbed    = 0
    N_transmitted = 0
    
    # Let "max depth reached" be denoted by "MDR".
    MDR_reflected   = []
    MDR_absorbed    = []
    MDR_transmitted = []
    
    for photon in range(N_photons):
        
        # Initial descension.
        xi =  np.random.random()
        L  = -np.log(1 - xi)
        
        theta   = SZA
        tau     = L * np.cos(theta)
        tau_max = tau
        
        terminated = False
        
        while not terminated:
            
            xi        = np.random.random()
            L         = -np.log(1 - xi)
            mu        = 2 * xi - 1
            theta_new = np.arccos(mu)
            theta    += theta_new
            
            if xi <= SSA:
                
                tau_new = tau + L * np.cos(theta)

                if tau_new > tau_max and tau_new <= COT:
                    tau_max = tau_new

                tau = tau_new
            
                if tau < 0:
                    
                    N_reflected += 1
                    terminated   = True
                    MDR_reflected.append(tau_max)
                    
                elif tau > COT:
                    
                    N_transmitted += 1
                    terminated     = True
                    MDR_transmitted.append(tau_max)
                    
            else:
                
                N_absorbed += 1
                terminated  = True
                MDR_absorbed.append(tau_max)
        
    reflectance   = N_reflected   / N_photons
    absorbance    = N_absorbed    / N_photons
    transmittance = N_transmitted / N_photons
        
    return {"reflected"       : N_reflected,
            "absorbed"        : N_absorbed,
            "transmitted"     : N_transmitted,
            "reflectance"     : reflectance,
            "absorbance"      : absorbance,
            "transmittance"   : transmittance,
            "MDR reflected"   : MDR_reflected,
            "MDR absorbed"    : MDR_absorbed,
            "MDR transmitted" : MDR_transmitted}