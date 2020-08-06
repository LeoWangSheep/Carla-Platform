import time

from TestScenario.TrafficLightScenario import TrafficLightScenario
from TestScenario.ObjectDetectScenario import ObjectDetectScenario
from TestScenario.LeadingVehicleScenario import LeadingVehicleScenario
from TestScenario.TurningObstacleScenario import TurningObstacleScenario

from DrivingAgent.DetectAgent import DetectAgent
from DrivingAgent import CarlaAutoAgent

from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from CarlaEnv.CarlaWeather import Weather



def main_loop():
	try:
		# set weather
		weather_mode = None
		weather_config = None
		use_config = True # The switch for weather configuration
		use_mode = False # The switch for pre-configure weather mode
		if use_mode:
			weather_mode = {}
			# time_str
			# possible value: Noon, Sunset, Night, Sunrise
			weather_mode["time_str"] = "Noon"
			# weather
			# possible value: Clear, Rainy, Fog, Wind
			weather_mode["weather"] = "Wind"

		if use_config:
			weather_config = {}
			weather_config['clouds'] = 20
			weather_config['rain'] = 0
			weather_config['puddles'] = 0
			weather_config['wind'] = 10
			weather_config['fog'] = 0
			weather_config['wetness'] = 0
			weather_config['azimuth'] = 0
			weather_config['altitude'] = 45
		

		carla_weather = Weather(mode = weather_mode, weather_config = weather_config)
		
		# test traffic light scenario
		
		scenario = TrafficLightScenario(weather = carla_weather)
		my_agent = DetectAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		
		
		# test object detect scenario
		'''
		scenario = ObjectDetectScenario()
		my_agent = DetectAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''

		# test leading vehicle scenario
		'''
		scenario = LeadingVehicleScenario()
		my_agent = CarlaAutoAgent.AutoAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''

		# test turning obstacle scenario
		'''
		scenario = TurningObstacleScenario()
		my_agent = CarlaAutoAgent.AutoAgent()
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

if __name__ == '__main__':
	main_loop()