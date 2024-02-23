# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:15:10 2024

@author: pdhum
"""
import pandas as pd
import numpy as np
import   matplotlib.pyplot as plt

def extract(filename):
    
    data = np.array(pd.read_csv(filename))[1:]
    time = np.array([float(data[i][0]) for i in range(data.shape[0])])
    volt = np.array([float(data[i][1]) for i in range(data.shape[0])])
    return time, volt


#time, volt = extract("C:/Users/pdhum/OneDrive/Documents/Group Studies/CIC_single_pulse_data/CIC_single_pulse_data_06.csv")

#time, volt = extract("C:/Users/pdhum/OneDrive/Documents/Group Studies/CIC_switch_error_data/CIC_switch_error_data_06.csv")
time, volt = extract("C:/Users/pdhum/OneDrive/Documents/Group Studies/CIC_pulse_data_for_fft.csv")

#time, volt = extract("C:/Users/pdhum/OneDrive/Documents/Group Studies/square_wave_test.csv")
time = time[::50]
volt = volt[::50]
fftvolt = np.fft.fft(volt)
n = fftvolt.shape[0]
timestep = (time[1]-time[0])*(10**-9)
freq = np.fft.fftfreq(n, d=timestep)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('Charge Injection and Noise')
ax.set_xlabel('frequency (Hz)')
#ax.set_xlabel('time (ns)')
ax.set_ylabel('Voltage (mV)')
ax.plot((freq), (fftvolt.real), label = 'Charge Injection FFT')
#ax.plot(time[::10], volt[::10], label = 'CIC')
#ax.set_xlim(-1e8, 1e8)
ax.legend()
plt.show()