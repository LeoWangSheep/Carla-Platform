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


def get_agent(path_str, agent_name):
	module_name = os.path.basename(path_str).split('.')[0]
	# print(module_name)
	dir_path = os.path.dirname(path_str)
	# print(dir_path)
	sys.path.insert(0, dir_path)
	module_agent = importlib.import_module(module_name)
	agent_instance = getattr(module_agent, agent_name)
	return agent_instance


def main_loop(data_frame):
	try:
		# set weather
		weather_mode = None
		weather_config = None
		use_config = data_frame['if_custom']  # The switch for weather configuration

		if use_config:
			weather_config = {}
			weather_config['clouds'] = 20
			weather_config['rain'] = 0
			weather_config['puddles'] = 0
			weather_config['wind'] = 10
			weather_config['fog'] = 0
			weather_config['wetness'] = 0
			weather_config['azimuth'] = 0
			weather_config['altitude'] = 90
		else:
			# time_str
			# possible value: Noon, Sunset, Night, Sunrise
			# weather
			# possible value: Clear, Rainy, Fog, Wind
			weather_mode = {"time_str": data_frame['preset_time'], "weather": data_frame['preset_weather']}

		carla_weather = Weather(mode=weather_mode, weather_config=weather_config)

		scenario = None
		scenario_str = data_frame['scenario']
		# possible value: TrafficLight, TurningObstacle, LeadingVehicle,
		# 		 		  TurningObstacle, BlindPoint
		if scenario_str == 'TrafficLight':
			scenario = TrafficLightScenario(weather=carla_weather)
		elif scenario_str == 'ObjectDetect':
			scenario = ObjectDetectScenario(weather=carla_weather)
		elif scenario_str == 'LeadingVehicle':
			scenario = LeadingVehicleScenario(weather=carla_weather)
		elif scenario_str == 'TurningObstacle':
			scenario = TurningObstacleScenario(weather=carla_weather)
		elif scenario_str == 'BlindPoint':
			scenario = BlindPointScenario(weather=carla_weather)

		if scenario is None:
			raise Exception("Wrong Name of Scenario, please check: ", scenario_str)

		agent_class = get_agent(data_frame['agent_path'], data_frame['agent_name'])
		my_agent = agent_class()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()

		record_data = scenario.get_data_frame()
		record_data['agent_path'] = data_frame['agent_path']
		record_data['agent_name'] = data_frame['agent_name']
		print(record_data)

		# test traffic light scenario
		'''
		scenario = TrafficLightScenario(weather = carla_weather)
		my_agent = DetectAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''
		
		# test object detect scenario
		'''
		scenario = ObjectDetectScenario(weather=carla_weather)
		my_agent = DetectAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''

		# test leading vehicle scenario
		'''	
		scenario = LeadingVehicleScenario(weather=carla_weather)
		my_agent = CarlaAutoAgent.AutoAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''

		# test turning obstacle scenario
		'''
		scenario = TurningObstacleScenario(weather=carla_weather)
		my_agent = CarlaAutoAgent.AutoAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''

		# test blind point scenario

		# scenario = BlindPointScenario(weather=carla_weather)
		# my_agent = CarlaAutoAgent.AutoAgent()
		'''
		agent_class = get_agent(data_frame['agent_path'], data_frame['agent_name'])
		my_agent = agent_class()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''
		
		# find spawn point
		'''
		carla_env = CarlaEnvironment()
		my_ego_vehicle = EgoVehicle(carla_env)

		my_ego_vehicle.set_start_waypoint( _x = 70, _y = -195, _z = 10,\
									  _pitch = 0, _yaw = 180, _roll = 0)
		my_ego_vehicle.vehicle_initial()

		carla_env.follow_actor(my_ego_vehicle.get_vehicle(), 50)
		my_ego_vehicle.stop()
		time.sleep(10)
		'''
		'''
		carla_env = CarlaEnvironment()
		my_ego_vehicle = EgoVehicle(carla_env)

		my_ego_vehicle.set_start_waypoint( _x = 165, _y = 196, _z = 3,\
									  _pitch = 0, _yaw = 180, _roll = 0)
		
		my_ego_vehicle.set_end_waypoint(_x = -45, _y = 195, _z = 5,\
									  _pitch = 0, _yaw = 180, _roll = 0)
		
		my_ego_vehicle.vehicle_initial()

		carla_env.follow_actor(my_ego_vehicle.get_vehicle(), 150)
		my_ego_vehicle.stop()
		# time.sleep(10)
		my_ego_vehicle.apply_default_agent()
		# time.sleep(10)
		'''
	except Exception as e:
		print("Error Occur :", e)
	finally:
		scenario.scenario_end()

		# carla_env.clean_actors()


'''
if __name__ == '__main__':
	main_loop()
'''