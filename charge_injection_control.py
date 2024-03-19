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

class dac:
    '''
    A class to setup and control Digital to Analogue Converters.
    '''
    def __init__(self, max_out, pin, spi):
        '''
        Sets up a DAC.
        
        Parameters
            max_out: integer or float
                The maximum possible output of the DAC.
            pin: object
                The pin on the board that will output the chip select.
            spi: object
                Controls the data transmission using spi protocols.
        '''
        self.max_out = max_out
        self.cs0 = digitalio.DigitalInOut(pin)
        self.cs0.direction = digitalio.Direction.OUTPUT
        self.cs0.value = True
        self.spi = spi
    
    def output(self, out):
        '''
        Commands the DAC to output the desired voltage

        Parameters
            out: integer or float
                The desired output voltage.
        '''
        p = out/self.max_out # <-- Calculates the desired output as a fraction of the max output
        hexcode = hex((0b01<<22)|(int((p*65535))<<6)) # <-- Creates the binary string to send to the DAC
        cmd = [int(hexcode[2:4], 16), int(hexcode[4:6], 16), int(hexcode[6:8], 16)] # <-- Converts the binary code to hexadecimal digits
        self.cs0.value=False
        self.spi.write(cmd) # <-- Sends the data using kkblinka
        self.cs0.value=True
        
    def max_test(self):
        '''
        Commands the DAC to output its maximum voltage,
            independent of the maximum voltage used in the constructor.
        '''
        hexcode = hex((0b01<<22)|(int((65535))<<6))
        cmd = [int(hexcode[2:4], 16), int(hexcode[4:6], 16), int(hexcode[6:8], 16)]
        self.cs0.value=False
        self.spi.write(cmd)
        self.cs0.value=True


def charge_setup():
    '''
    Sets up the various objects needed to control the Charge Injection Circuit. 
    '''
    clk = digitalio.DigitalInOut(board.C0)
    mosi = digitalio.DigitalInOut(board.C2)
    miso = digitalio.DigitalInOut(board.C1)
    spi=kkblinka.SPIBitBanger(clk, mosi, miso)
    
    charge = digitalio.DigitalInOut(board.D7)
    charge.direction = digitalio.Direction.OUTPUT
    button = digitalio.DigitalInOut(board.D6)
    button.direction = digitalio.Direction.INPUT
    
    
    
    return spi, charge, button 

def count_setup():
    '''
    Sets up the pins needed to control and read the counter.
    '''
    count_on = digitalio.DigitalInOut(board.D4)
    count_on.direction = digitalio.Direction.OUTPUT

    digit_1 = digitalio.DigitalInOut(board.C4)
    digit_1.direction = digitalio.Direction.INPUT

    digit_2 = digitalio.DigitalInOut(board.C6)
    digit_2.direction = digitalio.Direction.INPUT

    digit_4 = digitalio.DigitalInOut(board.C7)
    digit_4.direction = digitalio.Direction.INPUT

    digit_8 = digitalio.DigitalInOut(board.C5)
    digit_8.direction = digitalio.Direction.INPUT
    count_on.value=True
    return count_on, digit_1, digit_2, digit_4, digit_8

def main():
    
    spi, charge, button = charge_setup()
    count_on, digit_1, digit_2, digit_4, digit_8 = count_setup()
    
    charge_volt = 2
    thresh_volt = 0.5
    
    charge_dac = dac(2.5, board.C3, spi)
    charge_dac.output(charge_volt)
    
    thresh_dac = dac(2.5, board.D5, spi)
    thresh_dac.output(thresh_volt)
    
    data = []
    thresh_list = np.linspace(0,2.5,501)
    count=0
    count_on.value=False
    count_on.value=True
    
    
    try:
        while not button.value:
            total = 0
            for i in range(1):
                #thresh_dac.output(thresh_volt)
                
                count = digit_1.value + digit_2.value*2 + digit_4.value*4 + digit_8.value*8
                
                data.append(count)    
                
                if count >= 1:
                    total+=count
                    count_on.value=False
                    count_on.value=True
                
                charge_dac.output(0)
                charge.value=True
                charge_dac.output(charge_volt)
                charge.value=False
            print(total)
            
        print("Button Pressed")
    except KeyboardInterrupt:
        charge_dac.max_test()
        
    return data, charge_dac, thresh_dac

if __name__ == "__main__":
    data, charge_dac, thresh_dac = main()
