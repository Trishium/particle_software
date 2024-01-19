# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:22:19 2024

@author: toby
"""
import Particle_physics_emulation as code
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import json
import numpy as np

class HelloWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 100
        self.width = 400
        self.height = 250
        self.title = "Error function modeling"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #create textbox for the charge value
        self.label = QLabel("Voltage In:",self)
        self.label.move(0,0) 
        self.textbox = QLineEdit(self)
        self.textbox.move(20,30)
        self.textbox.resize(40,40)

        #create a textbox for the capacitance value
        self.label2 = QLabel("Gain:",self)
        self.label2.move(100,0)
        self.duck = QLineEdit(self)
        self.duck.move(120,30)
        self.duck.resize(40,40)

        #create a textbox for the noise deviation
        self.label3 = QLabel("Noise Deviation:",self)
        self.label3.move(200,0)
        self.noise = QLineEdit(self)
        self.noise.move(200,30)
        self.noise.resize(40,40)
        
        #create a button in the window
        self.button = QPushButton("Run simulation", self)
        self.button.move(20,80)

        #connect button to function on click
        self.button.clicked.connect(self.on_click)
        
        #create default button
        self.default = QPushButton("Run default sim",self)
        self.default.move(200,80)
        self.default.clicked.connect(self.run_defualt)
        
        #creates a button to find values from data
        self.data = QPushButton("Run from data",self)
        self.data.move(150,180)
        self.data.clicked.connect(self.on_click2)
        
        #directory entry box for data load
        self.file_name_label = QLabel("File location:",self)
        self.file_name_label.move(100,120)
        self.file_name = QLineEdit(self)
        self.file_name.move(100,150)
        self.file_name.resize(200,20)


        self.show()
    def run_defualt(self):
        #runs the simulation without changing the values
        values = code.main()
        self.resultWin(values)
        
    def on_click2(self):
        file_path = self.file_name.text() + "\data.json"
        f = None
        try:
            f = open("data.json")
        except:
            try:
                f = open(file_path)
            except:
                f= open("example.json")
        if f != None:
            data = json.load(f)
            hit_array = np.array(data["hitChance"])
            threshold_array = np.array(data["threshold"])
            voltage_value = data["Voltage"]
            self.resultWin([code.plot(threshold_array, hit_array),voltage_value])
            return 0
        self.errorWin()

    def on_click(self):
        #runs the simulation with new values given
        capacitance = float(self.duck.text())
        noise = int(self.noise.text())
        charge = int(self.textbox.text())
        values = code.main(charge,capacitance,noise)
        self.resultWin(values)
    
    def resultWin(self,value):
        mean = str(round(value[0][0],2))
        div = str(round(value[0][1],2))
        gain = str(round(value[0][0] / value[1],2))
        QMessageBox.question(self,"Results","Voltage Out: " + mean + "\nNoise Mean: " + div + "\nGain: " + gain)
        
    def errorWin(self,message):
        QMessageBox.question(self, "Error","Error: " + message)

def run_app():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    app.exec_()
run_app()
