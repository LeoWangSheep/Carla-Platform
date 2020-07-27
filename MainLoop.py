import time

from TestScenario.TrafficLightScenario import TrafficLightScenario
from TestScenario.ObjectDetectScenario import ObjectDetectScenario
from TestScenario.LeadingVehicleScenario import LeadingVehicleScenario
from TestScenario.TurningObstacleScenario import TurningObstacleScenario

from DrivingAgent.DetectAgent import DetectAgent
from DrivingAgent import CarlaAutoAgent

from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle



def main_loop():
	try:
		
		# test traffic light scenario
		'''
		scenario = TrafficLightScenario()
		my_agent = DetectAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		'''
		
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
		
		scenario = TurningObstacleScenario()
		my_agent = CarlaAutoAgent.AutoAgent()
		scenario.set_up_scenario_start(my_agent)
		scenario.run_scenario()
		

		'''
		# find spawn point
		carla_env = CarlaEnvironment()
		my_ego_vehicle = EgoVehicle(carla_env)

		my_ego_vehicle.set_start_waypoint( _x = 105, _y = -74, _z = 10,\
									  _pitch = 0, _yaw = 180, _roll = 0)
		my_ego_vehicle.vehicle_initial()

		carla_env.follow_actor(my_ego_vehicle.get_vehicle(), 150)
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