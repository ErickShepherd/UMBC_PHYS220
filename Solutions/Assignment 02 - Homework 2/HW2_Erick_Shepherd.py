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
    E-mail:             Zhibo.Zhang@UMBC.edu
    Date:               2017-01-30
    Assignment:         02
    Assignment name:    Homework 2
    Available points:   90
    Grade percentage:   5.71%
    
    Description:        Basic exercises with numpy as matplotlib.
    
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
    (UMBC). Use of the contents of this repository by students of UMBC is 
    restricted by the academic integrity policies and principles of UMBC.
    
    All of the contents of this document are protected from copying under U.S. 
    and international copyright laws and treatises. Any unauthorized copying, 
    alteration, distribution, transmission, performance, display, or other use 
    of this material is prohibited.
"""

# Future module imports for Python 2-3 compatibility.
from __future__ import division, print_function

# Standard library imports.
import datetime

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

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
            Start: 1948-01-01 00:00:0.0 (UTC)
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
            Start: 1948-01-01 00:00:0.0 (UTC)
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
    #
    #   Author's note:
    #       Dr. Zhang originally indicated in the document that the shape was to
    #       be (12, 69, 73, 144); however, he later corrected this in class.
    
    # Solution:
    # Convert timestamps to an ndarray of datetime objects.
    reference_date = datetime.datetime(1800, 1, 1)
    
    dates  = [reference_date + datetime.timedelta(hours = x) for x in times]
    dates  = np.asarray(dates[:-1]) # Discard 2017-01-01 from the time array.
    years  = np.asarray(list(set(date.year for date in dates)))
    months = np.arange(1, 12 + 1)
    
    get_month_name = lambda index: datetime.date(2000, index, 1).strftime("%B")
    month_strings  = [get_month_name(month)[0:3] for month in months]
        
    # Extract the starting and ending years.
    start_year = years[0]
    end_year   = years[-1]
    
    # Extract the number of years, latitudes, and longitudes for the new shape.
    N_years      = years.size
    N_latitudes  = latitudes.size
    N_longitudes = longitudes.size
        
    # Reshape the air temperature array.
    #
    # Author's note:
    #   Many students expressed some confusion about this exercise. Since the 
    #   time stamps are given on the first of every month, the objective of this
    #   exercise was to reshape the time dimension of the air temperature array
    #   from 1 group of 829 months to 69 groups of 12 months each.
    #    - Erick Shepherd
    old_shape        = air_temperatures.shape
    new_shape        = (N_years, 12, N_latitudes, N_longitudes)
    air_temperatures = air_temperatures[0:-1, :, :].reshape(new_shape)
    
    # Test of solution:
    output_fields = [old_shape, air_temperatures.shape]
    output_string = "Air temperature array reshaped from {} to {}."
    
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
    
    # Let "annual mean global mean temperatures" be denoted as "AMGMT".
    AMGMT = air_temperatures.mean(axis = (1, 2, 3))
    
    find_upper_limit = lambda a, b, delta: a + (b - a) // delta * delta + delta
    
    x_delta       = 10
    x_lower_limit = start_year
    x_upper_limit = find_upper_limit(start_year, end_year, x_delta)
    
    decade_spaced_labels = np.arange(x_lower_limit, x_upper_limit + 1, x_delta)
    
    y_lower_limit = np.floor(np.min(AMGMT))
    y_upper_limit = np.ceil(np.max(AMGMT))
    
    plt.figure()
    plt.plot(years, AMGMT)
    plt.title("Annual Mean Global Mean Temperature vs. Time")
    plt.xlabel("Year",                fontsize = "large")
    plt.ylabel("Temperature [$^oC$]", fontsize = "large")
    plt.xticks(decade_spaced_labels)
    plt.xlim(x_lower_limit, x_upper_limit)
    plt.ylim(y_lower_limit, y_upper_limit)
    plt.grid()
    
    # Problem 1.3:
    #   Derive and plot the 69-year averaged seasonal cycle of global mean 
    #   temperature.
    #
    # Author's note:
    #   Students expressed some confusion over this problem as well, as the way
    #   it was asked is somewhat ambiguous. To clarify, the seasonal cycle may
    #   be shown through either the monthly mean global mean temperatures or by
    #   taking it a step further and computing the three month mean global mean
    #   temperatures. Both approaches are shown.
    #   
    #   As an aside based on a mistake several students made, please note that
    #   conventional seasonal names (i.e. Spring, Summer, Autumn, Winter) are 
    #   opposite in the Northern and Southern hemispheres, and so using that
    #   naming convention is ambiguous on a global scale.
    #    - Erick Shepherd
    
    # Let "seasonal mean global mean temperatures" be denoted by "SMGMT".
    SMGMT = air_temperatures.mean(axis = (0, 2, 3))
    
    # Let "three month mean global mean temperatures" be denoted by "TMMGMT".
    TMMGMT  = np.mean(SMGMT.reshape(-1, 3), axis = 1)
    seasons = months[0::3]

    y_lower_limit = np.floor(np.min(SMGMT))
    y_upper_limit = np.ceil(np.max(SMGMT))
    
    # Month values have 1 subtracted in order to index from 0.
    plt.figure()
    plt.bar(seasons, TMMGMT, label = "Seasonal", width = 2, color = "red")
    plt.plot(months - 1, SMGMT, label = "Monthly", linewidth = 2, c = "k")
    plt.title("69-year Averaged Seasonal Cycle of Global Mean Temperature")
    plt.xlabel("Month",               fontsize = "large")
    plt.ylabel("Temperature [$^oC$]", fontsize = "large")
    plt.xticks(months - 1, month_strings)
    plt.xlim(months[0] - 1, months[-1] - 1)
    plt.ylim(y_lower_limit, y_upper_limit)
    plt.legend()
    plt.grid()
    
    # Problem 1.4:
    #   Derive and plot the temperatures of the Summer months of the United 
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
    
    northernmost =   49.384472
    southernmost =   24.520833
    easternmost  =  -66.947028 + 180
    westernmost  = -124.771694 + 180
    
    # Month values have 1 subtracted in order to index from 0.
    summer_mask    = np.arange(5, 8)
    latitude_mask  = (southernmost <= latitudes)  & (latitudes  <= northernmost)
    longitude_mask = (westernmost  <= longitudes) & (longitudes <= easternmost)
    
    us_latitudes    = latitudes[latitude_mask]
    us_longitudes   = longitudes[longitude_mask]
    N_us_latitudes  = us_latitudes.size
    N_us_longitudes = us_longitudes.size
    
    # Let "U.S. mean summer temeratures" be denoted by "USMST".
    USMST     = air_temperatures[:, summer_mask]
    USMST     = USMST[:, :, latitude_mask]
    USMST     = USMST[:, :, :, longitude_mask]
    new_shape = (N_years * summer_mask.size, N_us_latitudes, N_us_longitudes)
    USMST     = USMST.reshape(new_shape).mean(axis = (1, 2))
    
    summers = [month for month in range(years.size * summer_mask.size)]
        
    x_delta       = 30
    x_lower_limit = summers[0]
    x_upper_limit = find_upper_limit(summers[0], summers[-1], x_delta)
    
    y_lower_limit = np.floor(np.min(USMST))
    y_upper_limit = np.ceil(np.max(USMST))
    
    x_ticks = summers[0::x_delta] + [x_upper_limit]
    
    plt.figure()
    plt.plot(summers, USMST)
    plt.title("Summertime Temperatures of the U.S. over 69 Years")
    plt.xlabel("Summer Month",        fontsize = "large")
    plt.ylabel("Temperature [$^oC$]", fontsize = "large")
    plt.xticks(x_ticks, decade_spaced_labels)
    plt.xlim(x_lower_limit, x_upper_limit)
    plt.ylim(y_lower_limit, y_upper_limit)
    plt.grid()

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
    
    x_labels = [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$']
    
    plt.figure()
    plt.plot(x, sine,   color = "red",  label = "sin")
    plt.plot(x, cosine, color = "blue", label = "cos")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.xticks(np.arange(-np.pi, np.pi + np.pi / 2, np.pi / 2), x_labels)
    plt.yticks(np.arange(-1.0, 1.0 + 0.5, 0.5))
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-1.0, 1.0)
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
    plt.xlabel(r"Temperature[$^oC$]",        fontsize = "large")
    plt.ylabel(r"Relative Humidity [$\%$] ", fontsize = "large")
    plt.xlim(0, 35)
    plt.ylim(0, 120)
    plt.annotate("data 1", xy = (30, 90), color = "red")
    plt.annotate("data 2", xy = (30, 55), color = "blue")
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
    line_plot()
    scatter_plot()
    contourf_plot()
    
    plt.show()