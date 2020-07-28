import time

from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario

import carla

class DrivingScenario(Scenario):
	def __init__(self, town_id):
		super().__init__(town_id)
		self._level_done = False

	def follow_ego_vehicle(self, ego_yaw):
		while True:
			if self._scenario_done:
				break
			if self._level_done:
				break
			Scenario._carla_env.follow_actor(self._physical_vehicle, 50, a_yaw = ego_yaw)

	def ego_driving(self, destination):
		self._agent.set_destination((destination['x'],
									  destination['y'],
									  destination['z']))
		print("Ego Vehicle Driving...")
		while True:
			if self._scenario_done:
				break
			input_data = self._sensor_list.get_data()
			control = self._agent.run_step(input_data)
			self._physical_vehicle.apply_control(control)
			if self._agent.done():
				self._physical_vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake = 1.0))
				break
		self._level_done = True

	def get_distance(self, ego_v, enemy_e):
		leading_x = enemy_e.get_location().x
		ego_x = ego_v.get_location().x
		leading_y = enemy_e.get_location().y
		ego_y = ego_v.get_location().y
		distance_x = abs(leading_x - ego_x)
		distance_y = abs(leading_y - ego_y)
		distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
		return distance
