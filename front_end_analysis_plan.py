# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:41:54 2024

@author: pdhum
"""

import os
import time
os.environ["BLINKA_FT232H"]="1"
import board
import digitalio
import kkblinka
import numpy as np
from charge_injection_control import dac, charge_setup, count_setup


def main():
    
    spi, charge, button = charge_setup()
    count_on, digit_1, digit_2, digit_4, digit_8 = count_setup()
    
    charge_dac = dac(2.5, board.C3, spi)
    charge_dac.output(1.5)
    
    thresh_dac = dac(2.5, board.D5, spi)
    thresh_dac.output(0.2)
    
    data = []
    thresh_list = np.linspace(0,2.5,501)
    count=0
    count_on.value=False
    count_on.value=True
    
    out_list = np.zeros(501)
    for k in range(501):
        thresh_dac.output(thresh_list[k])
        total = 0
        for i in range(1000):
            for j in range(2):
                data.append(count)
                    
                count = digit_1.value + digit_2.value*2 + digit_4.value*4 + digit_8.value*8
                if count >= 1:
                    total+=1
                    count_on.value=False
                    count_on.value=True
                
            charge_dac.output(0)
            charge.value=True
            charge_dac.output(1.5)
            charge.value=False
        print(total)
        out_list[k] = total
    
    return data, charge_dac, thresh_dac

if __name__ == "__main__":
    data, charge_dac, thresh_dac = main()

