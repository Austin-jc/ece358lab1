# ece358lab1
This program was written in python 3.  
Most output comes in the form of a csv or printed output. 

Required Packages
matplotlib 3.5.3
scipy

ECEUbuntu Terminal
Clone or download the project https://github.com/Austin-jc/ece358lab1.git
Change the current working directory to the project folder ("ece358lab1" by default) 

to simulate for the finite case, run 
$ python lab1simulator.py finite T lambda transmissionRate AvgPacketLength K name.csv
for example:
$ python3 lab1simulator.py finite 1000 250 1000000 2000 10 output.csv

to simulate for the infintite case, run
$ python lab1simulator.py infinite T lambda transmissionRate AvgPacketLength name.csv
for example
$ python3 lab1simulator.py infinite 1000 250 1000000 2000 output.csv

TO JUST GET THE RESULTS FOR Q1, Q3 and Q6:
run the q1.py q3.py and q6.py files using:
$ python3 <q#>.py
for example
$ python3 q1.py

q1, q3 and q6 will return csv files with the data


IF IT DOESNT WORK MAKE SURE ECEUbuntu HAS PYTHON3
