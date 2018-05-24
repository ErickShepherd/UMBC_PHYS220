==========================================
Sample Output of Midterm Project Solutions
==========================================

The source code which produces these solutions may be found in Midterm_Project_Erick_Shepherd.py_ and MCRT_Erick_Shepherd.py_.

    .. _Midterm_Project_Erick_Shepherd.py: Miterm_Project_Erick_Shepherd.py
    .. _MCRT_Erick_Shepherd.py: MCRT_Erick_Shepherd.py

Problem 1 Sample Output:
========================
::

    Trapezoidal rule:
    
      Number of intervals: 10
      Analytical area:     4.4
      Numerical area:      4.50656
      Absolute error:      0.10655999999999999
      Relative error:      0.024218181818181812
      Percent error:       2.4218181818181814%

      Number of intervals: 100
      Analytical area:     4.4
      Numerical area:      4.401066656
      Absolute error:      0.0010666559999998881
      Relative error:      0.00024242181818179273
      Percent error:       0.024242181818179272%

      Number of intervals: 1000
      Analytical area:     4.4
      Numerical area:      4.400010666665601
      Absolute error:      1.0666665600567171e-05
      Relative error:      2.424242181947084e-06
      Percent error:       0.0002424242181947084%

    Simpson's rule:

      Number of intervals: 10
      Analytical area:     4.4
      Numerical area:      4.50656
      Absolute error:      0.10655999999999999
      Relative error:      0.024218181818181812
      Percent error:       2.4218181818181814%

      Number of intervals: 100
      Analytical area:     4.4
      Numerical area:      4.401066656
      Absolute error:      0.0010666559999998881
      Relative error:      0.00024242181818179273
      Percent error:       0.024242181818179272%

      Number of intervals: 1000
      Analytical area:     4.4
      Numerical area:      4.400010666665601
      Absolute error:      1.0666665600567171e-05
      Relative error:      2.424242181947084e-06
      Percent error:       0.0002424242181947084%

Problem 2 Sample Output:
========================

To compute the error of each method, we must also solve this problem analytically. We are given the following integral:

|Equation 1|

We can then substitute in known values an solve:

|Equation 2|

::

    Trapezoidal method converged to 9.92 with a 0.54% error from the analytical solution 9.97 after 10 intervals.
    Simpson's method converged to 10.03 with a 0.58% error from the analytical solution 9.97 after 12 intervals.

Integrals
---------

.. image:: Sample%20Output/Problem%202.1.png
   :width: 40pt
   
Errors
------

.. image:: Sample%20Output/Problem%202.2.png
   :width: 40pt
    
Problem 3 Sample Output:
========================
::

    Problem 3 progress: [==================================================100%] (|)

Approach 1:
-----------

.. image:: Sample%20Output/Problem%203%2C%20Approach%201.png
   :width: 40pt
   
Approach 2:
-----------

.. image:: Sample%20Output/Problem%203%2C%20Approach%202.png
   :width: 40pt

Approach 3:
-----------

.. image:: Sample%20Output/Problem%203%2C%20Approach%203.png
   :width: 40pt
   
.. |Equation 1| image:: LaTeX/Problem%202%20Analytical%20Solution%201.png
   :width: 40pt
.. |Equation 2| image:: LaTeX/Problem%202%20Analytical%20Solution%202.png
   :width: 40pt
