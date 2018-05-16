#!/usr/bin/python
# coding=utf-8

"""
Solutions to homework 1, PHYS 220, UMBC.

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
    Assignment:         01
    Assignment name:    Homework 1
    Available points:   100
    Grade percentage:   5.71%
    
    Description:        Python basics exercises.
    
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
from __future__ import print_function

# Standard library imports.
from random import randint

# Standardize the input function for Python 2-3 compatibility.
try:
    input = raw_input
except NameError:
    pass

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        1
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Define a function max_of_three() which takes three numbers 
                    as arguments and returns the largest of them. To implement 
                    this, use the if/elif/else statements.
"""

# Solution:
def max_of_three(x1, x2, x3):
    
    maximum = x1
    
    if maximum < x2:
        maximum = x2
    elif maximum < x3:
        maximum = x3
    
    return maximum
    
# Test of solution:
x1, x2, x3 = 3, 2, 4
output_fields = [x1, x2, x3, max_of_three(x1, x2, x3)]
output_string = "The maximum of {}, {}, and {} is {}.\n"

print("Problem 1:")
print(output_string.format(*output_fields))

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        2
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    The function  max_of_three() will only work for three 
                    numbers, but suppose we have many more numbers, or suppose 
                    we cannot tell in advance how many numbers there will be?  
                    Write a function max_in_list() that takes a list of numbers 
                    and returns the largest one.
"""

# Solution:
def max_in_list(number_list):
    
    maximum = number_list[0]
    
    for element in number_list:
        if maximum < element:
            maximum = element
    
    return maximum
   
# Test of solution:
X = [randint(0, 100) for index in range(randint(1, 10))]
output_fields = [X, max_in_list(X)]
output_string = "The maximum of the list {} is {}.\n"

print("Problem 2:")
print(output_string.format(*output_fields))

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        3
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Define two functions sum() and a function multiply() which
                    respectively sum and multiply all numbers in a list of 
                    numbers. For example, sum([1, 2, 3, 4]) should return 10, 
                    and multiply([1, 2, 3, 4]) should return 24.
                    
    Author's notes: Be wary when implementing something like this in situations
                    outside of the classroom; "sum" is a built-in function in
                    Python, and defining another function by the same name
                    will override the built-in function by that name in the
                    scope in which it is defined. - Erick Shepherd
"""

# Solution 3.1:
def sum(number_list): 
    
    total = 0
    
    for element in number_list:
        total += element
    
    return total

# Solution 3.2:
def multiply(number_list):
    
    total = 1
    
    for element in number_list:
        total *= element
        
    return total
    
# Test of solutions:
X = [randint(0, 100) for index in range(randint(0, 10))]
output_fields_1 = [X, sum(X)]
output_fields_2 = [X, multiply(X)]
output_string_1 = "The sum of all elements of the list {} is {}."
output_string_2 = "The product of all elements of the list {} is {}.\n"

print("Problem 3:")
print(output_string_1.format(*output_fields_1))
print(output_string_2.format(*output_fields_2))

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        4
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Define a function that computes the length of a given list 
                    or string. It is true that Python has a built-in len() 
                    function but writing it yourself is nevertheless a good
                    exercise.
"""

# Solution 4:
def list_len(iterable):
    
    length = 0
    
    for element in iterable:
        length += 1
    
    return length

# Test of solution:
X = [randint(0, 100) for index in range(randint(1, 10))]
Y = "Schrodinger"
output_fields_1 = [X, list_len(X)]
output_fields_2 = [Y, list_len(Y)]
output_string_1 = "The length the list {} is {}."
output_string_2 = "The length of the string \"{}\" is \"{}\".\n"

print("Problem 4:")
print(output_string_1.format(*output_fields_1))
print(output_string_2.format(*output_fields_2))

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        5
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Define a function reverse() that computes the reversal of a 
                    list or string. For example, reverse([2,3,4]) should return 
                    [4,3,2].
"""

# Solution:
def list_reverse(x):
    
    return x[::-1]

# Test of solution:
X = [randint(0, 100) for index in range(randint(1, 10))]
Y = "Schrodinger"
output_fields_1 = [X, list_reverse(X)]
output_fields_2 = [Y, list_reverse(Y)]
output_string_1 = "The reversal of the list {} is {}."
output_string_2 = "The reversal of the string \"{}\" is \"{}\".\n"

print("Problem 5:")
print(output_string_1.format(*output_fields_1))
print(output_string_2.format(*output_fields_2))

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        6
    Points:         10
    Weight:         1.00
    Percentage:     10.00%
    
    Description:    Excerises on Python list indexing.
                        1. Print all elements of mylist.
                        2. Print the first element of mylist.
                        3. Print the last element of mylist.
                        4. Print the first three elements of mylist.
                        5. Print the last three elements of mylist.
                        6. Print the elements at odd indices: e.g., 1, 3, 5...
                        7. Print the elements at even indices in backward order:
                           e.g., 18, 16, 14...
                        8. Print the elements from indices 3 through 10.
                        
    Author's notes: "range(20)" returns a list in Python 2 but returns an
                    iterable in Python 3; however, "list(range(20))" works
                    in both Python 2 and Python 3.
"""

mylist = list(range(20))

print("Problem 6:")

# Solution 6.1:
print("6.1:", *mylist)

# Solution 6.2:
print("6.2:", *mylist[0:1])

# Solution 6.3:
print("6.3:", *mylist[-1:])

# Solution 6.4:
print("6.4:", *mylist[0:3])

# Solution 6.5:
print("6.5:", *mylist[-3:])

# Solution 6.6:
print("6.6:", *mylist[1::2])

# Solution 6.7:
print("6.7:", *mylist[-2::-2])

# Solution 6.8:
print("6.8:", *mylist[3:10], end = "\n\n")

"""
Problem information:
--------------------------------------------------------------------------------
    Problem:        7
    Points:         40
    Weight:         1.00
    Percentage:     40.00%
    
    Description:    A guess number game. Go to the following website: 
                    http://www.goobix.com/games/guess-the-number/
                    Play the game a couple of times and try to implment a
                    replica of the game using Python.
"""

# Solution:  
def guess_the_number():
    
    answer  = "1234"
    guess   = ""
    guesses = 0
    
    while guess != answer:
        
        while len(set(guess)) != len(answer):
            
            guess = input("Enter a list of four numbers between 0 and 9 " + \
                          "with no repeating numbers: ").strip()
            
            if len(set(guess)) != len(answer):
                print("Invalid input.\n")
            else:
                guesses += 1
          
        same_position      = 0
        different_position = 0
        
        for index in range(len(answer)):
            
            if guess[index] == answer[index]:
                same_position += 1
            elif guess[index] in answer:
                different_position += 1
            
        if guess != answer:
            
            print("Incorrect!")
            
            print("Right numbers in right positions: " + \
                  "{}".format(same_position))
            
            print("Right numbers in wrong positions: " + \
                  "{}\n".format(different_position))
            
            guess = ""
            
        else:
            
            print("Correct!")
            print("You won in {} moves.".format(guesses))
            
# Test of solution:
print("Problem 7:")
guess_the_number() 