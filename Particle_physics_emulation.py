# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 17:20:06 2024

@author: pdhum
"""
import random as rand#pylint: disable=import-error
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sp
import scipy
import json

#voltage = v_in * charge * gain

def my_erf(x, m, s):
    #error function
    return 0.5+0.5*scipy.special.erf((m-x)/(s*(2**0.5)))#pylint: disable=no-member

def cycle(length,v_thresh,voltage,noise_div):
    #returns the hit ratio for a set voltage threshold by iterating through pulses
    volt_rand = np.random.normal(voltage, noise_div, length)
    hitCounter = sum([i>v_thresh for i in volt_rand])
    return hitCounter/length

def plot(x_array,y_array):
    #plots the results in the form of an error function
    fit, var = sp.curve_fit(my_erf, x_array, y_array)
    y_fit = my_erf(x_array, fit[0], fit[1])

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x_array, y_array, "y+", markersize = 4)
    ax.plot(x_array, y_fit)
    ax.text(0.75, 0.95, f'Mean = {round(fit[0],4)}', transform=ax.transAxes, horizontalalignment='left', fontsize=9)
    ax.text(0.75, 0.90, f'St. Dev = {round(fit[1],4)}', transform=ax.transAxes,
             horizontalalignment='left', fontsize=9)
    ax.set_title("Hit detection vs Threshold Voltage")
    ax.set_xlabel("Threshold Voltage")
    ax.set_ylabel("Fraction of hits detected")
    plt.show()
    return fit

def saveToJson(values):
    threshold_list = values[0].tolist()
    hitChance_list = values[1].tolist()
    x = {
        "threshold": threshold_list,
        "hitChance": hitChance_list,
        "Voltage": values[2]
    }
    json_object = json.dumps(x, indent = 3)
    with open("example.json", "w") as outfile:
        outfile.write(json_object)
    return 0

def main(volt_in = 10,gain = 1.2, noise = 5):
    volt_out = volt_in * gain
    x_array = np.linspace(0, 2*volt_out,1000) #array of voltage threshold as a percentage of diode voltage
    y_array = [cycle(1000,i,volt_out,noise) for i in x_array] #saves the hit ratio values to y_array
    return [plot(x_array,y_array),volt_in, x_array, y_array]
