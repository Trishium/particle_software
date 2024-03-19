import random as rand#pylint: disable=import-error
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sp
import scipy
import json
from os import listdir
from os.path import isfile, join
#voltage = v_in * charge * gain

def cycle(length,v_thresh,voltage,noise_div):
    #returns the hit ratio for a set voltage threshold by iterating through pulses
    volt_rand = np.random.normal(voltage, noise_div, length)
    hitCounter = sum([i>v_thresh for i in volt_rand])
    return hitCounter/length

def saveToJson(values,file_name = "example.json"):
    #Saves data in a JSON formatting for data analysis software
    #Will replace 
    threshold_list = values[0].tolist()
    hitChance_list = values[1].tolist()
    x = {
        "threshold": threshold_list,
        "hitChance": hitChance_list,
        "charge": values[2]
    } 
    json_object = json.dumps(x, indent = 2)
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
    return 0

def trial(charge,gain,uncertainty,index):
  voltage = charge * gain
  threshold_array = np.linespace(0,voltage * 2,100)
  hit_chance_array = hitChance_array = [cycle(1000,threshold_array[i],voltage,uncertainty) for i in range(0,100)]
  

def main(charge_max = 10, capacitance = 1, uncertainty = 5, gain = 1.2):
  charge_array = np.linespace(0,charge,100)
  for 
  
