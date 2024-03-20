# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:22:19 2024

@author: toby
"""
import data_analysis as analysis
import data_generation as gen
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
        self.height = 400
        self.title = "Error function modeling"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #create textbox for the charge value
        self.charge_label = QLabel("Input Charge:",self)
        self.charge_label.move(0,0) 
        self.charge_box = QLineEdit(self)
        self.charge_box.move(20,30)
        self.charge_box.resize(40,40)

        #create a textbox for the capacitance value
        self.gain_label = QLabel("Gain:",self)
        self.gain_label.move(100,0)
        self.gain_box = QLineEdit(self)
        self.gain_box.move(120,30)
        self.gain_box.resize(40,40)

        #create a textbox for the noise diviation
        self.uncertain_label = QLabel("Uncertainty:",self)
        self.uncertain_label.move(200,0)
        self.noise = QLineEdit(self)
        self.noise.move(200,30)
        self.noise.resize(40,40)
        
        #creates a button to find values from data
        self.data = QPushButton("Generate Data",self)
        self.data.move(100,180)
        self.data.clicked.connect(self.on_click_gen_data)
        
        #directory entry box for data load
        self.file_name_label = QLabel("File location:",self)
        self.file_name_label.move(100,120)
        self.file_name = QLineEdit(self)
        self.file_name.move(100,150)
        self.file_name.resize(200,20)
        
        self.gain_sim = QPushButton("Calculate Gain", self)
        self.gain_sim.move(150,250)
        self.gain_sim.clicked.connect(self.gain_func)

        self.gain_data = QPushButton("Gain From Data", self)
        self.gain_data.move(200,180)
        self.gain_data.clicked.connect(self.gainJson)


        self.show()
        
    def on_click_gen_data(self):
        try:
            gen.main(float(self.charge_box.text()),float(self.noise.text()),float(self.gain_box.text()))
        except:
            gen.main()

    def gainJson(self):
        self.resultWin(analysis.Gain_from_data(self.file_name.text()))
        #QMessageBox.question(self,"Gain",str(analysis.Gain_from_data(self.file_name.text())[0]))
        return 0

    def gain_func(self):
        self.on_click_gen_data()
        self.resultWin(analysis.Gain_from_data())
        return 0

    def resultWin(self,value):
        gain = str(round(value[0],2))
        div = str(round(value[1],2))
        QMessageBox.question(self,"Results","Gain: " + gain + "\nUncertainty: " + div)
        
    def errorWin(self,message):
        QMessageBox.question(self, "Error","Error: " + message)

def run_app():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    app.exec_()
run_app()
