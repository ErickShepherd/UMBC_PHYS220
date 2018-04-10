=====================================
Sample Output of Homework 4 Solutions
=====================================

The source code which produces these solutions may be found in HW4_Erick_Shepherd.py_ and MCRT_Erick_Shepherd.py_.

    .. _HW4_Erick_Shepherd.py: HW4_Erick_Shepherd.py
    .. _MCRT_Erick_Shepherd.py: MCRT_Erick_Shepherd.py

Problem 1 Sample Output:
========================
::

    Question 1 progress: [==================================================100%] (-)

.. image:: Sample%20Output/Problem%201.png
   :width: 40pt
    
Problem 2 Sample Output:
========================
::

    Question 2 progress: [==================================================100%] (|)

.. image:: Sample%20Output/Problem%202.png
   :width: 40pt
   
Analysis:
=========

From figure 2, we observe that for all single scattering albedo (|Single Scattering Albedo|) values such that |Equation 01|, the reflectance |Reflectance| approaches zero very quickly; however, for |Equation 02|, |Equation 03| considerably more slowly. In other words, for a single scattering albedo less than 1, the maximum depth able to be reached by photons entering the cloud from which they are still able to be reflected back out of the top of the cloud is substantially less than an ideal case where the single scattering albedo equals 1. This makes sense when one considers the definition of single scattering albedo as the likelihood of scattering over absorbtion of a photon upon collision with a cloud particle: If |Equation 02|, then the likelihood of the photon being absorbed during any scattering event is 0. Consequently, this completely eliminates one of the three possible end scenarios for a photon in the simulation, and so photons can only either be transmitted through the cloud or reflected off of it. This also explains why in figure 1, we see that for |Equation 02|, as the cloud optical thickness

.. |Cloud Optical Thickness|    image:: LaTeX/Cloud%20Optical%20Thickness.png
.. |Depth|                      image:: LaTeX/Depth.png
.. |Equation 01|                image:: LaTeX/Equation%2001.png
.. |Equation 02|                image:: LaTeX/Equation%2002.png
.. |Equation 03|                image:: LaTeX/Equation%2003.png
.. |Max Depth Reached|          image:: LaTeX/Max%20Depth%20Reached.png
.. |Reflectance|                image:: LaTeX/Reflectance.png
.. |Single Scattering Albedo|   image:: LaTeX/Single%20Scattering%20Albedo.png
