Code for analysing a Front End using the FT232H chip.

charge_injection_control.py controls the charge injection circuit, sending pulses into the Front End. See report for the circuit design.

data_analysis.py reads data from JSON files and calculates the gain and uncertainty.

data_generation.py creates simulated data of the expected output of the Front End, also able to save data to the correct formatting.

GUI.py is used to interface with data_generation.py and data_analysis, all files are required to be within the same directory.

front_end_analysis_plan.py is a variation of charge_injection_control.py, intended to actually get usable data from the charge injection circuit and Front End.

CIC_plotting.py has an effective way of extracting data from CSV files into numpy arrays.

Worksheet files contain some explanation of the theory behind the data analysis.

WARNINGS:
- Do not use either data_generation.py or GUI.py in a directory where important data in JSON files starting with 'data', these will be overwritten.
- Uses function based coding to give future developers greater control so there is no encapsulation, be careful when calling functions that might save over data.

REQUIRED LIBRARIES (for GUI.py, data_generation, data_analysis):
It's recommended to use sypder as it has all the libraries already.
- Numpy
- PyQt5
- json
- scipy
