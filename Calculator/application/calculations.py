r'''
    calculations: This file contains all the methods to calculate the formulas on the plasma formulary.
'''

from application import app
from flask import Flask, render_template, request
import plasmapy
import astropy
import astropy.units as u
import plasmapy.formulary.parameters as pfp
from ast import dump


def calculate_thermal_pressure(form):
    r''' Returns 
        --------
        Quantity 
            Thermal pressure in Pascal (Pa) 

        Parameters
        ---------- 
        `form`: The calculator form from the HTML page where the user enters data for calculation.
    '''
    num1 = form['temp']     # Get temperature
    num2 = form['density']  # Get density
    u1 = form['unitsT']
    u2 = form['unitsN']

    if num1 == "" or num2 == "" or u1 == 'select' or u2 == 'select':
        return -1

    # Convert units of temperature and density into Unit objects, and use them to make Quantity objects
    unit1 = u.Unit(u1)
    q1 = u.Quantity(num1, unit1)
    unit2 = u.Unit(u2)
    q2 = u.Quantity(num2, unit2)

    sum = pfp.thermal_pressure(q1, q2)
    return sum


def calculate_debye_length(form):
    r''' Returns 
        --------
        Quantity 
            Debye length in meters (m)

        Parameters
        ---------- 
        `form`: The calculator form from the HTML page where the user enters data for calculation.
    '''
    num1 = form['temp']
    num2 = form['density']
    u1 = form['unitsT']
    u2 = form['unitsN']

    if num1 == "" or num2 == "" or u1 == 'select' or u2 == 'select':
        return -1

    unit1 = u.Unit(u1)
    q1 = u.Quantity(num1, unit1)
    unit2 = u.Unit(u2)
    q2 = u.Quantity(num2, unit2)
    sum = pfp.Debye_length(q1, q2)
    return sum


def calculate_gyrofrequency(form):
    r''' Returns 
        --------
        Quantity 
            Gyrofrequency in units of radians per second

        Parameters
        ---------- 
        `form`: The calculator form from the HTML page where the user enters data for calculation.
    '''
    mag_fld = form['mf_mag']        # Magnetic field magnitude
    mag_unit = form['unitsB']       # Unit of magnetic field
    particle = form['particle']

    # Use MultiDict.get() to get Z as an int or None
    z = form.get('z', type=int)     # Average ionization
    signed = form['signed']

    # Boolean to convert output from angular frequency to Hz
    to_hz = form['to_hz']

    # Prompt user for required inputs
    if mag_fld == "" or mag_unit == 'select':
        return -1

    b = u.Quantity(mag_fld, u.Unit(mag_unit))
    p = plasmapy.particles.Particle(particle)

    # Form returns 'True' and 'False' as strings and not booleans

    # Gyrofrequency with only Magnetic Field and Particle
    if signed == 'False' and z == None and to_hz == 'False':
        sum = pfp.gyrofrequency(b, p)
        return sum

    # Gyrofrequency with B, particle, z
    elif signed == 'False' and z != None and to_hz == 'False':
        sum = pfp.gyrofrequency(b, p, signed=False, Z=z, to_hz=False)
        return sum

    # Output if to_hz is true, signed is false and Z is given
    elif signed == 'False' and z != None and to_hz == 'True':
        sum = pfp.gyrofrequency(b, p, signed=False, Z=z, to_hz=True)
        return sum

    # Output if to_hz is true, signed is false and Z is not given
    elif signed == 'False' and z == None and to_hz == 'True':
        sum = pfp.gyrofrequency(b, p, signed=False, Z=None, to_hz=True)
        return sum

    # Gyrofrequency with B, particle, signed
    elif signed == 'True' and z == None and to_hz == 'False':
        sum = pfp.gyrofrequency(b, p, signed=True, Z=None, to_hz=False)
        return sum

    # Output if to_hz is true, signed is true and Z is not given
    elif signed == 'True' and z == None and to_hz == 'True':
        sum = pfp.gyrofrequency(b, p, signed=True, Z=None, to_hz=True)
        return sum

    # Gyrofrequency with B, particle, z, signed
    elif signed == 'True' and z != None and to_hz == 'False':
        sum = pfp.gyrofrequency(b, p, signed=True, Z=z, to_hz=False)
        return sum

    # Output if to_hz is true, signed is true and Z is given
    elif signed == 'True' and z != None and to_hz == 'True':
        sum = pfp.gyrofrequency(b, p, signed=True, Z=z, to_hz=True)
        return sum
    return sum


def calculate_inertial_length(form):
    r''' Returns 
        --------
        Quantity 
            Inertial length in meters (m)

        Parameters
        ---------- 
        `form`: The calculator form from the HTML page where the user enters data for calculation.
    '''
    n = form['n']           # Particle number density
    p = form['particle']    # Particle
    u1 = form['unitsN']

    if n == "" or u1 == 'select':
        return -1

    n_quantity = u.Quantity(n, u.Unit(u1))
    sum = pfp.inertial_length(n_quantity, p)
    return sum
