import time

from TestScenario.TrafficLightScenario import TrafficLightScenario
from DrivingAgent.DetectAgent import DetectAgent



def main_loop():
	try:
		traffic_scenario = TrafficLightScenario()
		my_agent = DetectAgent()
		traffic_scenario.set_up_scenario_start(my_agent)
		traffic_scenario.run_scenario()
		'''
		my_ego_vehicle = EgoVehicle(carla_env)

		my_ego_vehicle.set_start_waypoint( _x = 70, _y = -133, _z = 10,\
									  _pitch = 0, _yaw = 0, _roll = 0)
		my_ego_vehicle.set_end_waypoint( _x = 100, _y = -133, _z = 5,\
									  _pitch = 0, _yaw = 0, _roll = 0)
		my_ego_vehicle.vehicle_initial()

		carla_env.follow_actor(my_ego_vehicle.get_vehicle())
		my_ego_vehicle.stop()

		my_ego_vehicle.apply_default_agent()
		'''
		time.sleep(10)
	except Exception as e:
		print("Error Occur :", e)
	finally:
		traffic_scenario.scenario_end()


if __name__ == '__main__':
	main_loop()