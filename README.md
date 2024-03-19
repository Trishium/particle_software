Code for analysing a Front End using the FT232H chip.

charge_injection_control.py controls the charge injection circuit, sending pulses into the Front End. See report for the circuit design.

new_emulation.py creates simulated data of the expected output of the Front End and analyses either that data or real data from the Front End.

GUI.py is used to interface with new_emulation.

front_end_analysis_plan.py is a variation of charge_injection_control.py, intended to actually get usable data from the charge injection circuit and Front End.

CIC_plotting.py has an effective way of extracting data from CSV files into numpy arrays.

Worksheet files contain some explanation of the theory behind the data analysis.
