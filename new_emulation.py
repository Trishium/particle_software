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
from os import listdir
from os.path import isfile, join
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

def fit_calc(x_array,y_array):
    return sp.curve_fit(my_erf, x_array, y_array)

def saveToJson(values,file_name = "example.json"):
    #Saves data in a JSON formatting for data analysis software
    #Will replace 
    threshold_list = values[0].tolist()
    hitChance_list = values[1].tolist()
    x = {
        "threshold": threshold_list,
        "hitChance": hitChance_list,
        "Voltage": values[2],
        "Capacitance": values[3]
    } 
    json_object = json.dumps(x, indent = 3)
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
    return 0

def Find_data_files(file_path):
    #Attempts to find the JSON data files
    count = 0
    array = listdir(file_path)
    for i in range(len(array)):
    #Sees if data in the given directory
        if array[i][3:] == "data"
            count += 1
    if count > 0:
        return [1,count]
    array = listdir()
    for i in range(len(array)):
    #Sees if data is in local directory
        if array[i][3:] == "data"
            count += 1
    if count > 0:
        return [2,count]
    return [0,count]
    #If no data found returns 0

def Gain_from_data_final(file_path):
    #Final version of retrieving data from JSON files
    check = Find_data_files(file_path)
    if check[0] == 0:
        return 0
    voltage_array = np.zeros(check[1])
    charge_array = np.zeros(check[1])
    if check[0] == 2:
        file_path = "/"
    for i in range(check[1]):
        values = readJson_Gain(file_path,"data" + str(i) + ".json")
        voltage_array[i] = values[1]
        charge_array[i] = values[0]
    return sum(voltage_array) / sum(charge_array)


def trial(capacitance = 1, voltage_in = 10, noise = 5,gain = 1.2):
    #returns the pass rate for given intial charge and threshold voltage
    voltage_front = gain* capacitance * voltage_in
    threshold_array = np.linspace(0, 2*voltage_in,1000)
    hitChance_array = [cycle(1000,threshold_array[i],voltage_front,noise) for i in range(0,1000)]
    return fit_calc(threshold_array,hitChance_array)

def main(volt_in = 10,capacitance = 1,noise = 5,gain = 1.2):
    #Finds the gain by iterating through trails for multiple input charges to find the pass rate
    charge = volt_in * capacitance
    charge_arry = np.linspace(0,charge * 2,100)
    voltage_out = [trial(capacitance,charge_arry[i]/capacitance,noise,gain)[0][0] for i in range(0,100)]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(charge_arry,voltage_out)
    plt.show()
    gain = sum(voltage_out) / sum(charge_arry)
    return gain
