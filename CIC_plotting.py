# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:15:10 2024

@author: pdhum
"""
import pandas as pd
import numpy as np
import   matplotlib.pyplot as plt

def extract(filename, n):
    '''
    Converts CSV files into numpy arrays
    
    Parameters
        filename: string
            The path of the file to be loaded
        
        n: integer
            The number of dependent variables being loaded
    
    
    '''
    data = np.array(pd.read_csv(filename))[1:]
    if n == 1:
        time = np.array([float(data[i][0]) for i in range(data.shape[0])])
        volt = np.array([float(data[i][1]) for i in range(data.shape[0])])
        return time, volt
    elif n==2:
        time = np.array([float(data[i][0]) for i in range(data.shape[0])])
        volt1 = np.array([float(data[i][1]) for i in range(data.shape[0])])
        volt2 = np.array([float(data[i][2]) for i in range(data.shape[0])])
        return time, volt1, volt2

file1 = ''
file2 = ''

time1, volt1, volt2 = extract(file2,2)
time0, volt0 = extract(file1,1)
'''
time = time[::3]
volt = volt[::3]
fftvolt = np.fft.fft(volt)
newvolt = np.fft.ifft(fftvolt)
n = fftvolt.shape[0]
timestep = (time[1]-time[0])*(10**-9)
freq = np.fft.fftfreq(n, d=timestep)
'''
fig = plt.figure()
#fig.set_size_inches(12, 9)
ax = fig.add_subplot(1,1,1)
ax.set_title('Output Pulse')
#ax.set_xlabel('log frequency (Hz)')
ax.set_xlabel('time (ns)')
ax.set_ylabel('Voltage (mV)')
#ax.plot(np.log10(freq), np.log10(fftvolt), label = 'Charge Injection FFT')
ax.plot(time0, volt0, label = "CIC Pulse")
#ax.plot(time, volt, label = "Unwanted Pulse")
#ax.plot(time1, volt1/1000, label = 'CIC', color = "#0096ff")
#ax.plot(time1, volt2-0.2608268, label = 'counter', color = "#37013f")
#ax.plot(time2-2.8, volt3, label = 'front end', color = "#228B22")
#ax.plot(time2-2.8, volt4-0.3031189, label = 'comparator', color ="#ff0000")
ax.set_xlim(-150, 150)
ax.set_ylim(-30,140)
ax.legend()
plt.show()
