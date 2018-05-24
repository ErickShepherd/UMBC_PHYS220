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
    
Problem 2 Sample Output:
========================
::

    Question 2 progress: [==================================================100%] (|)

.. image:: Sample%20Output/Problem%202.png
   
Analysis:
=========

From figures 1 and 2, we observe two distinct cases in the Monte Carlo simulation of radiative transfer in clouds: 

- Case 1: |Equation 01|
- Case 2: |Equation 02|

Let us then treat this piecewise and address each in turn.

Case 1: |Equation 01|
---------------------

From figure 2, we observe that for a single scattering albedo (|Single Scattering Albedo|) such that |Equation 01|, the number of photons reflected off of the cloud (|Number of Photons Reflected|) approaches zero much more slowly than for the other cases tested where |Equation 02|. This can be explained from the definition of single scattering albedo as the likelihood of scattering over absorption of a photon upon collision with a cloud particle: If |Equation 01|, then the likelihood of the photon being absorbed during any scattering event is 0. Consequently, this completely eliminates one of the three possible end scenarios for a photon in the simulation, and so photons can only either be transmitted through the cloud or reflected off of it. Any photons that would have been absorbed for lower |Single Scattering Albedo| then must be reflected or transmitted, and so both values go up. However, as the depth (|Depth|) of the photon in the cloud increases, so too does the likelihood of the photon, having reached that depth, continuing on to transmit through the cloud as opposed to climbing back out to be reflected. 

This explanation from the definition of |Single Scattering Albedo| also explains why in figure 1, we see that for |Equation 01|, as the cloud optical thickness |Cloud Optical Thickness| increases, |Equation 04|: As the total thickness of the cloud increases, in a situation where only transmission and reflection are possible, the likelihood of the photon reflecting out of the cloud also increases, approaching a probability of 1 (100%) as |Equation 05|.

Case 2: |Equation 02|
---------------------

From figure 2, we observe that for all values of single scattering albedo |Equation 02|, the number of photons reflected off of the cloud (|Number of Photons Reflected|) approaches zero very quickly relative to case 1 where |Equation 01|. In other words, for a single scattering albedo less than 1, the maximum depth able to be reached by photons entering the cloud from which they are still able to be reflected back out of the top of the cloud is substantially less than an ideal case where the single scattering albedo equals 1. As with case 1, this too circles back to the definition of |Single Scattering Albedo|: In this case, for all |Equation 02|, there is some nonzero probability of the photon being absorbed upon collision with a cloud particle. This possibility for absorption substantially detracts from both the number of photons transmitted through and reflected off of the cloud, as photons may now be terminated during any collision event, as opposed to only when their position is above or below the cloud. Consequently, even for cases where |Single Scattering Albedo| is very close to 1 (i.e., 0.96), absorption events dominate over reflection events.

This is corroborated in figure 1: For |Equation 02|, as the |Equation 05|, the reflectance (|Reflectance|) of the cloud quickly plateaus out to some constant value proportional to |Single Scattering Albedo|. As the likelihood of scattering decreases and absorption increases, those photons which descend deeply into the cloud are more likely to be either absorbed or transmitted, and the probability of being reflected as a function of |Depth| approaches zero.

.. |Cloud Optical Thickness|        image:: LaTeX/Cloud%20Optical%20Thickness.png
.. |Depth|                          image:: LaTeX/Depth.png
.. |Equation 01|                    image:: LaTeX/Equation%2001.png
.. |Equation 02|                    image:: LaTeX/Equation%2002.png
.. |Equation 03|                    image:: LaTeX/Equation%2003.png
.. |Equation 04|                    image:: LaTeX/Equation%2004.png
.. |Equation 05|                    image:: LaTeX/Equation%2005.png
.. |Max Depth Reached|              image:: LaTeX/Max%20Depth%20Reached.png
.. |Number of Photons Reflected|    image:: LaTeX/Number%20of%20Photons%20Reflected.png
.. |Reflectance|                    image:: LaTeX/Reflectance.png
.. |Single Scattering Albedo|       image:: LaTeX/Single%20Scattering%20Albedo.png
