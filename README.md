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
python lab1simulator.py finite T lambda transmissionRate AvgPacketLength K name.csv
for example:
python lab1simulator.py finite 1000 250 1000000 2000 10 output.csv

to simulate for the infintite case, run
python lab1simulator.py infinite T lambda transmissionRate AvgPacketLength name.csv
for example
python lab1simulator.py infinite 1000 250 1000000 2000 output.csv

alternatively, you can get the answers to the questions by adding a call to one of the question methods in the files.  
in simulator.py you can add q3(<outputfilename>), q4(), or stability_test() to the bottom of the file and just run it to get the results.
in finiteSimulator.py you can add q5() or stability_test()

IF IT DOESNT WORK MAKE SURE ECEUbuntu HAS PYTHON3
