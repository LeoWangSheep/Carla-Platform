import time
import random
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario

from Marking.MarkingScore import Marking

import carla

class DrivingScenario(Scenario):
	def __init__(self, town_id, weather = None):
		super().__init__(town_id, weather)
		self._level_done = False
		self.dest_arrive = False

	def set_up_scenario_start(self, agent, position):
		super().set_up_scenario_start(agent, position)
		self._sensor_list.append_collision(self._physical_vehicle)
		self.marking_tool = Marking(mode='driving')

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
			try:
				control = self._agent.run_step(input_data)
			except Exception as e:
				self._scenario_done = True
				raise Exception("The Agent's run_step function has problem! Please have a check.")
			self._physical_vehicle.apply_control(control)
			if self._agent.done():
				self.dest_arrive = True
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

	def record_score(self):
		sensor_data = self._sensor_list.get_data()
		colli_times = sensor_data['Collision']['data']
		close_times = random.randint(3, 7)
		final_mark = self.marking_tool.driving_result(colli_times, self.dest_arrive, close_times)
		self.info_dataframe['close_times'] = close_times
		self.info_dataframe['is_arrive'] = self.dest_arrive
		self.info_dataframe['collision_times'] = colli_times
		self.info_dataframe['mark'] = final_mark

