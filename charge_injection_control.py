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

def volt2cmd(v):
    '''
    Converts a desired voltage for the DAC into hexadecimal code to control the DAC
    
    Parameters
        v: float or int
            The voltage to be output by the DAC.
    
    Returns
        array
            List of bytes to control the 
    
    '''
    p = v/2.5
    if p>1 or p<0:
        print("voltage out of range")
        return
    hexcode = hex((0b01<<22)|(int((p*65535))<<6))
    return [int(hexcode[2:4], 16), int(hexcode[4:6], 16), int(hexcode[6:8], 16)]


def main():
    v_in = 2
    resistance_in = 1
    resistance_out = 2
    capacitance = 1
    
    clk = digitalio.DigitalInOut(board.C0)
    mosi = digitalio.DigitalInOut(board.C2)
    miso = digitalio.DigitalInOut(board.C1)
    cs0 = digitalio.DigitalInOut(board.C3)
    cs0.direction = digitalio.Direction.OUTPUT
    spi=kkblinka.SPIBitBanger(clk, mosi, miso)
    
    charge = digitalio.DigitalInOut(board.C0)
    charge.direction = digitalio.Direction.OUTPUT
    button = digitalio.DigitalInOut(board.C1)
    button.direction = digitalio.Direction.INPUT
    
    cs0.value=True
    try:
        while not button.value: 
            charge.value=True
            cs0.value=False
            spi.write(volt2cmd(v_in))
            time.sleep(5*resistance_in*capacitance)
            
            charge.value=False
            cs0.value=True
            time.sleep(5*resistance_out*capacitance)
        print("Button Pressed")
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    main()