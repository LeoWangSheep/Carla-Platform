# Welcome to Carla-Based Autonomous Driving Testing Platform

This platform is design for the autonomous driving testing. Users can import their autonomous driving algorithm into 
the agent file and execute the program to test the algorithm into the Carla Driving Simulator. 
Currently, this platform provides the scenario as follows:

## Scenario Provided
1. Traffic Light Detection Scenario
2. Object Detection Scenario
3. Leading Vehicle Driving Scenario
4. Turning Obstacle Driving Scenario
5. Blind Point Driving Scenario

After the algorithm is tested in these scenarios, the system will generate a report and give a mark based on the performance. 

## How to use the program
### STEP 1 
download python 3.7+

### STEP 2 
download Carla Simulator https://carla.readthedocs.io/en/latest/start_quickstart/ follow the quick start tutorial to 
install the pre-built version of Carla (It makes life easier) my project is developed in Windows Carla 0.9.8

### STEP 3 
set environment variable (PYTHONPATH) PYTHONPATH = \your-carla-path\PythonAPI\carla\dist\your-carla-egg.egg

### STEP 4 
configure all the necessary library or setting. The mysql database is necessary for storing the test result.
To connect your local database, you should configure the database name, host, username and password in the
beginning of the DataOperation/data_operation.py. For creating the necessary data table, the create_table.sql should
be execute in your database. 

### STEP 5 
Inherit the Agent class (In DrivingAgent/Agent.py) and rewrite the necessary function  
5.1 __init__() : Constructor, initialize your necessary members.  
5.2 initial_sensor() : declare the sensor you need to install on your vehicle. we provide RGB camera, GNSS sensor.  
The direction and position of the sensors can also be specified.  
For Driving Scenario:  
5.3 set_destination() : this function will provide a waypoint in the Carla world and its GPS position. Users can
use this information to set a goal.  
5.4 run_step() : this function will provide all the information obtained from the sensors. Users can use these
information to let the vehicle make some driving decision.  
5.5 done() : should return true if the vehicle arrive to the destination or complete the given mission.  
For Detect Scenario:  
5.6 detect() : should return a list contain all the necessary things in the detection task.  

### STEP 6 
run CarlaUE4.exe (Windows) / CarlaUE4.sh (Linux) (KEEP RUNNING) 

### STEP 7 
run Auto_Driving_Testing_Platform_v1.bat directly. or run the python script by using: 
py -3.7 user_interface.py

### STEP 8
Configure the weather and time in the user interface panel. (pre-define or user customize)
Configure the agent's file path and class name in the Agent Selection.
Select the scenario you want to test.

### STEP 9
Launch the test by clicking the RUN button!


If you want to exit during operation, please press Ctrl + C
