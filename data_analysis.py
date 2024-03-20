import numpy as np
import scipy.optimize as sp
import scipy
import json
from os import listdir
#voltage = v_in * charge * gain

def my_erf(x, m, s):
    #error function
    return 0.5+0.5*scipy.special.erf((m-x)/(s*(2**0.5)))#pylint: disable=no-member

def fit_calc(x_array,y_array):
    return sp.curve_fit(my_erf, x_array, y_array)

def Find_data_files(file_path):
    #Attempts to find the JSON data files
    count = 0
    try:
        array = listdir(file_path)
    except:
        array = listdir("/")
    for i in range(len(array)):
    #Sees if data in the given directory
        if array[i][:4] == "data":
            count += 1
    if count > 0:
        return [1,count]
    array = listdir()
    for i in range(len(array)):
    #Sees if data is in local directory
        if array[i][:4] == "data":
            count += 1
    if count > 0:
        return [2,count]
    print("failed to find data")
    return [0,count]
    #If no data found returns 0
    
def readJson_Gain(file_path,file_name = "data.json"):
    #No longer applicable
        f = None
        try:
            f = open(file_name)
        except:
            try:
                f = open(file_path + file_name)
            except:
                f= open("example.js")
        if f != None:
            data = json.load(f)
            hit_array = np.array(data["hitChance"])
            threshold_array = np.array(data["threshold"])
            charge = float(data["charge"])
            values = fit_calc(threshold_array,hit_array)
            return [charge,values[0][0],values[0][1]]
        return None

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def Gain_from_data(file_path = "/"):
    #Final version of retrieving data from JSON files
    uncertainty = 0
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
        uncertainty += values[2]
    array = reject_outliers(voltage_array/charge_array)
    return [(sum(array)/len(array)),uncertainty/len(charge_array)]
