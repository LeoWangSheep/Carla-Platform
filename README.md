# Carla-Based Autonomous Driving Testing Platform Documentation

STEP 1 download python 3.7+

STEP 2 download Carla Simulator https://carla.readthedocs.io/en/latest/start_quickstart/
	   follow the quick start tutorial to install the pre-built version of Carla (It makes life easier)
	   my project is developed in Windows Carla 0.9.8

STEP 3 set environment variable (PYTHONPATH) PYTHONPATH = \your-carla-path\PythonAPI\carla\dist\your-carla-egg.egg

STEP 4 modify the ./DrivingAgent/DetectAgent.py 's detect function, then you can test your traffic light detection algorithm by using our tool. (Maybe you should MODIFY the MainLoop.py yourself to test this module in current stage)

STEP 5 run CarlaUE4.exe (Windows) / CarlaUE4.sh (Linux) (KEEP RUNNING) 

STEP 6 run message_send.py (The parameters and contents can be set in that file)

If you want to exit during operation, please press Ctrl + C
