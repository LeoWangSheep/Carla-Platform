import time
import os
import importlib
import sys

from TestScenario.TrafficLightScenario import TrafficLightScenario
from TestScenario.ObjectDetectScenario import ObjectDetectScenario
from TestScenario.LeadingVehicleScenario import LeadingVehicleScenario
from TestScenario.TurningObstacleScenario import TurningObstacleScenario
from TestScenario.BlindPointScenario import BlindPointScenario

from DrivingAgent.DetectAgent import DetectAgent
from DrivingAgent import CarlaAutoAgent

from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from CarlaEnv.CarlaWeather import Weather

from DataOperation import data_operation


def get_agent(path_str, agent_name):
	# print('path name: ', path_str)
	module_name = os.path.basename(path_str).split('.')[0]
	# print(module_name)
	dir_path = os.path.dirname(path_str)
	# print(dir_path)
	sys.path.insert(0, dir_path)
	module_agent = importlib.import_module(module_name)
	agent_instance = getattr(module_agent, agent_name)
	return agent_instance


def main_loop(data_frame, err_queue):
	try:
		# set weather
		weather_mode = None
		weather_config = None
		use_config = data_frame['if_custom']  # The switch for weather configuration
		# print(use_config)
		print(data_frame)
		if use_config:
			weather_config = {}
			weather_config['clouds'] = data_frame['custom_cloud']
			weather_config['rain'] = data_frame['custom_rainfall']
			weather_config['puddles'] = data_frame['custom_ground_humidity']
			weather_config['wind'] = data_frame['custom_wind']
			weather_config['fog'] = data_frame['custom_fog']
			weather_config['wetness'] = data_frame['custom_air_humidity']
			weather_config['altitude'] = data_frame['custom_time']
			weather_config['azimuth'] = 0
		else:
			# time_str
			# possible value: Noon, Sunset, Night, Sunrise
			# weather
			# possible value: Clear, Rainy, Fog, Wind
			weather_mode = {"time_str": data_frame['preset_time'], "weather": data_frame['preset_weather']}

		carla_weather = Weather(mode=weather_mode, weather_config=weather_config)

		scenario = None
		scenario_str = data_frame['scenario']

		# possible value: TrafficLight, ObjectDetection, LeadingVehicle,
		# 		 		  TurningObstacle, BlindPoint
		if scenario_str == 'Traffic Light Detection Scenario':
			scenario = TrafficLightScenario(weather=carla_weather)
			# scenario_str = "TrafficLight"
		elif scenario_str == 'Object Detection Scenario':
			scenario = ObjectDetectScenario(weather=carla_weather)
			# scenario_str = "ObjectDetection"
		elif scenario_str == 'Leading Vehicle Scenario':
			scenario = LeadingVehicleScenario(weather=carla_weather)
			# scenario_str = "LeadingVehicle"
		elif scenario_str == 'Turning Obstacle Scenario':
			scenario = TurningObstacleScenario(weather=carla_weather)
			# scenario_str = "TurningObstacle"
		elif scenario_str == 'Blind Point Scenario':
			scenario = BlindPointScenario(weather=carla_weather)
			# scenario_str = "BlindPoint"

		if scenario is None:
			raise Exception("Wrong Name of Scenario, please check: ", scenario_str)

		agent_class = get_agent(data_frame['agent_path'], data_frame['agent_name'])
		my_agent = agent_class()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()

		record_data = scenario.get_data_frame()
		record_data['agent_path'] = data_frame['agent_path']
		record_data['agent_name'] = data_frame['agent_name']

		data_operation.insert(record_data)

	except Exception as e:
		err_queue.put("Runtime Error: " + str(e))
		# raise Exception("Runtime Error: " + str(e))
	finally:
		try:
			scenario.scenario_end()
		except Exception as e:
			pass



'''
if __name__ == '__main__':
	main_loop()
'''