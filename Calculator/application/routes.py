r'''
    routes: This file determines the methods to invoke for specific URLs, and the methods return the next HTML page to render.
'''

from application import app
from flask import Flask, render_template, request
from application import calculations as cal


@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    r''' 
        Renders the home page. Any of the three urls above will invoke this method. 
    '''
    return render_template('index.html')


@app.route('/go', methods=['POST'])
def go_to_calc():
    r''' 
        Returns the page to render depending on the option the user picks. 
    '''
    if request.method == 'POST':
        # Get the user option from the form
        page = request.form['calculate_options']

        if page == 'debye_length':
            return render_template('debye_length.html')
        elif page == 'gyrofrequency':
            return render_template('gyrofrequency.html')
        elif page == 'inertial_length':
            return render_template('inertial_length.html')
        elif page == 'thermal_pressure':
            return render_template('thermal_pressure.html')
        else:
            return render_template('index.html')


@app.route('/thermal_pressure', methods=['POST'])
def thermal_pressure(sum=sum):
    r''' 
        Calculates the Thermal Pressure and displays the answer on the same HTML page. 
    '''
    sum = cal.calculate_thermal_pressure(request.form)
    return render_template('thermal_pressure.html', sum=sum)


@app.route('/debye_length', methods=['POST'])
def debye_length(sum=sum):
    r''' 
        Calculates the Debye Length and displays the answer on the same HTML page. 
    '''
    sum = cal.calculate_debye_length(request.form)
    return render_template('debye_length.html', sum=sum)


@app.route('/gyrofrequency', methods=['POST'])
def gyrofrequency(sum=sum):
    r''' 
        Calculates the Gyrofrequency and displays the answer on the same HTML page. 
    '''
    sum = cal.calculate_gyrofrequency(request.form)
    return render_template('gyrofrequency.html', sum=sum)


@app.route('/inertial_length', methods=['POST'])
def inertial_length(sum=sum):
    r''' 
        Calculates the Inertial Length and displays the answer on the same HTML page. 
    '''
    sum = cal.calculate_inertial_length(request.form)
    return render_template('inertial_length.html', sum=sum)
