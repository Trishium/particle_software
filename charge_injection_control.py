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
        p = out/self.max_out
        hexcode = hex((0b01<<22)|(int((p*65535))<<6))
        cmd = [int(hexcode[2:4], 16), int(hexcode[4:6], 16), int(hexcode[6:8], 16)]
        self.cs0.value=False
        self.spi.write(cmd)
        self.cs0.value=True
        
    def max_test(self):
        hexcode = hex((0b01<<22)|(int((65535))<<6))
        cmd = [int(hexcode[2:4], 16), int(hexcode[4:6], 16), int(hexcode[6:8], 16)]
        self.cs0.value=False
        self.spi.write(cmd)
        self.cs0.value=True


def charge_setup():
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
    
    charge_dac = dac(2.5, board.C3, spi)
    charge_dac.output(2)
    
    thresh_dac = dac(2.5, board.D5, spi)
    thresh_dac.output(0.2)
    
    data = []
    count=0
    count_on.value=False
    count_on.value=True
    
    
    try:
        while not button.value:
            '''
            for i in range(10):
                data.append(count)
                
                count = digit_1.value + digit_2.value*2 + digit_4.value*4 + digit_8.value*8
                    
                print(count)
                if count >= 1:
                    count_on.value=False
                    count_on.value=True
            '''
            charge_dac.output(0)
            charge.value=True
            charge_dac.output(2)
            charge.value=False
                
            
        print("Button Pressed")
    except KeyboardInterrupt:
        pass
    return data, charge_dac, thresh_dac

if __name__ == "__main__":
    data, charge_dac, thresh_dac = main()
