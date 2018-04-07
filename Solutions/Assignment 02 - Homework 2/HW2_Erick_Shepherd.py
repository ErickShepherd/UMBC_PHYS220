#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 2, PHYS 220, UMBC.

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
    Number:             02
    Name:               Homework 2
    Due:                2018-02-27
    Available points:   90
    Grade percentage:   5.71%
    
    Description:        Python basics exercises.
    
Solutions information:
--------------------------------------------------------------------------------
    Author:             Erick Edward Shepherd, Teaching Assistant
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
    
    Redistribution of this program is prohibited without written permission from
    both copyright holders, Dr. Zhibo Zhang and Erick Edward Shepherd.
"""

# Future module imports for Python 2-3 compatibility.
from __future__ import division, print_function

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np
from netCDF4    import Dataset

def load_data_from_nc():
    
    """
    Loads air temperature data from NetCDF file.
    
    Data fields:
    
        Latitudes:
            Shape: (73,) -> (latitudes,)
            Range: -90 <= latitude <= 90
            Units: Degrees
            
        Longitudes:
            Shape: (144,) -> (longitudes,)
            Range: 0 <= longitude <= 357.5
            Units: Degrees
            
        Time:
            Shape: (829,) -> (time,)
            Range: 1297320.0 <= time <= 1902192.0
            Units: Hours since 1800-01-01 00:00:0.0 (UTC)
            Start: 1947-01-01 00:00:0.0 (UTC)
            End:   2017-01-01 00:00:0.0 (UTC)
            Notes: Each time stamp is spaced one month apart.
            
        Air temperature:
            Shape: (829, 73, 144) -> (time, latitudes, longitudes)
            Range: -73.78 <= temperature <= 41.749
            Units: Degrees centigrade
    """
    
    file_data        = Dataset("air.mon.mean.nc", "r")
    latitudes        = file_data.variables["lat"][:]  
    longitudes       = file_data.variables["lon"][:]
    times            = file_data.variables["time"][:] 
    air_temperatures = file_data.variables["air"][:]  
    file_data.close()
    
    return latitudes, longitudes, times, air_temperatures

def load_data_from_npz():
    
    """
    Loads air temperature data from NumPy savez file.
    
    Data fields:
    
        Latitudes:
            Shape: (73,) -> (latitudes,)
            Range: -90 <= latitude <= 90
            Units: Degrees
            
        Longitudes:
            Shape: (144,) -> (longitudes,)
            Range: 0 <= longitude <= 357.5
            Units: Degrees
            
        Time:
            Shape: (829,) -> (time,)
            Range: 1297320.0 <= time <= 1902192.0
            Units: Hours since 1800-01-01 00:00:0.0 (UTC)
            Start: 1947-01-01 00:00:0.0 (UTC)
            End:   2017-01-01 00:00:0.0 (UTC)
            Notes: Each time stamp is spaced one month apart.
            
        Air temperature:
            Shape: (829, 73, 144) -> (time, latitudes, longitudes)
            Range: -73.78 <= temperature <= 41.749
            Units: Degrees centigrade
    """
    
    file_data        = np.load("data.npz")
    latitudes        = file_data["lats"][:]  
    longitudes       = file_data["lons"][:]
    times            = file_data["time"][:] 
    air_temperatures = file_data["air"][:]  
    
    return latitudes, longitudes, times, air_temperatures

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         30
    Weight:         1.111
    Percentage:     33.33%
    
    Description:    Simple NumPy exercises. See Homework2.pdf for further 
                    details.
"""

def air_temp():
    
    # Author's note: 
    #   Either "load_data_from_npz()" or "load_data_from_nc()" would work
    #   equally well here; they are just two different means to the same end.
    #    - Erick Shepherd
    latitudes, longitudes, times, air_temperatures = load_data_from_npz()
    
    # Problem 1.1: 
    #   Reshape the air temperature array into a 4-dimentional array of shape 
    #   (69, 12, 73, 144) -> (years, months, latitudes, longitudes). Discard the
    #   last time value for the month of January, 2017.
    
    N_years      = times[0:-1].size // 12
    N_latitudes  = latitudes.size
    N_longitudes = longitudes.size
    
    end_year   = 2016
    start_year = end_year - N_years
    
    old_shape        = air_temperatures.shape
    new_shape        = (12, N_years, N_latitudes, N_longitudes)
    air_temperatures = air_temperatures[0:-1, :, :]
    air_temperatures = air_temperatures.reshape(new_shape, order = "F")
    
    output_fields = [old_shape, air_temperatures.shape]
    output_string = "Air temperature array reshaped from {} to {}.\n"
    
    print("Problem 1.1:")
    print(output_string.format(*output_fields))
    
    # Problem 1.2:
    #   Derive and plot the annual mean global mean temperature over the last
    #   69 years.
    #
    # Author's note:
    #   Annual mean global mean temperature is determined by first taking the 
    #   mean temperature across all latitudes and longitudes, which returns a
    #   time-series of global mean temperatures for each months; and then taking
    #   the mean of that time series for each year. In simple terms, it is the
    #   yearly average of the monthly global average temperatures.
    #    - Erick Shepherd
    
    
    
    # Problem 1.3:
    #   Derive and plot the 69-year averaged seasonal cycle of global mean 
    #   temperature.
    #
    # Author's note:
    #   A season in this instance is defined as a three month span. Note that
    #   conventional seasonal names (i.e. Spring, Summer, Autumn, Winter) are 
    #   opposite in the Northern and Southern hemispheres.
    #    - Erick Shepherd
    
    # Problem 1.4:
    #   Derive and plot the mean temperatures of the Summer months of the United
    #   States (June, July, August) over the last 69 years.
    #
    # Author's notes:
    #   For the sake of simplicity, the boundaries of the United States may be
    #   treated as its extreme points, which may be found at the following URL:
    #    - goo.gl/31cagN
    #   In this instance, in order to minimize the influence of ocean surface
    #   temperatures on the data series, we consider only the contiguous United
    #   States.
    #    
    #   180 degrees are added to the Eastern and Western boundaries, as the
    #   longitudes stored in the given data files range from 0 to 360 relative
    #   to -180 degrees from the prime meridian as opposed to the conventional 
    #   -180 to 180 degrees relative to the prime meridian.
    #    - Erick Shepherd
    northern_boundary =   49.384472
    southern_boundary =   24.520833
    eastern_boundary  =  -66.947028 + 180
    western_boundary  = -124.771694 + 180
    
    

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         20
    Weight:         1.111
    Percentage:     22.22%
    
    Description:    Line plot. See Homework2.pdf for further details.
"""

def line_plot():
    
    x      = np.linspace(-np.pi, np.pi, 30)
    cosine = np.cos(x)
    sine   = np.sin(x)
    
    xlabels = [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$']
    
    plt.plot(x, sine,   color = "red",  label = "sin")
    plt.plot(x, cosine, color = "blue", label = "cos")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-1.0, 1.0)
    plt.xticks(np.arange(-np.pi, np.pi + np.pi / 2, np.pi / 2), xlabels)
    plt.yticks(np.arange(-1.0, 1.0 + 0.5, 0.5))
    plt.legend(loc = "upper left")
    plt.grid(linestyle = "dotted")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         20
    Weight:         1.111
    Percentage:     22.22%
    
    Description:    Scatter plot. See Homework2.pdf for further details.
"""

def scatter_plot():
    
    T    = np.linspace(0,30,200)
    dRH1 = 10.0
    dRH2 = 5.0
    RH1  = 2.0 * T + 30.0 + dRH1 * np.random.randn(T.size)
    RH2  = 0.5 * T + 40.0 + dRH2 * np.random.randn(T.size)
    
    plt.figure()
    plt.scatter(T, RH1, c = "red",  marker = ".", s = 100, edgecolors = "none")
    plt.scatter(T, RH2, c = "blue", marker = ",", s = 20,  edgecolors = "none")
    plt.annotate("data 1", xy = (30, 90), color = "red")
    plt.annotate("data 2", xy = (30, 55), color = "blue")
    plt.xlim(0, 35)
    plt.ylim(0, 120)
    plt.xlabel(r"Temperature[$^oC$]",        fontsize = "large")
    plt.ylabel(r"Relative Humidity [$\%$] ", fontsize = "large")
    plt.grid(linestyle = "dotted")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        4
    Points:         20
    Weight:         1.111
    Percentage:     22.22%
    
    Description:    2D contour plot. See Homework2.pdf for further details.
"""

def contourf_plot():
    
    T = np.linspace(0, 30, 50)
    P = np.linspace(600, 1000, 50)
    
    RH = np.outer((P / 100), np.exp(12 * T / (T + 243)))
    
    plt.figure()
    plt.contourf(T, P, RH, 50, cmap = "jet")
    plt.xlabel(r"Temperature[$^oC$]", fontsize = "large")
    plt.ylabel("Pressure [Pa]",       fontsize = "large")
    plt.colorbar()

# Display output:
if __name__ == "__main__":
    
    air_temp()
    #line_plot()
    #scatter_plot()
    #contourf_plot()
    
    plt.show()