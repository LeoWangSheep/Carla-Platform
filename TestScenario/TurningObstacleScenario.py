import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from TestScenario.DrivingScenario import DrivingScenario

import carla

t_o_position = [ {'start' : { 'x' : 105, 'y' : -77, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				  'destination' : { 'x' : 76, 'y' : -50, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1}},
				  {'start' : { 'x' : 105, 'y' : -77, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				  'destination' : { 'x' : 76, 'y' : -50, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1}},
				  {'start' : { 'x' : 105, 'y' : -77, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				  'destination' : { 'x' : 76, 'y' : -50, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1}}, ]

actor_blueprint_categories = {
			'car1' : 'vehicle.tesla.model3',
			'car2' : 'vehicle.audi.a2'
		}

class TurningObstacleScenario(DrivingScenario):
	def __init__(self):
		super().__init__(3)

	def set_up_scenario_start(self, agent):
		init_position = t_o_position[0]['start']
		# setting up ego vehicle
		super().set_up_scenario_start(agent, init_position)
		self._agent.bind_vehicle(self._physical_vehicle)
		# time.sleep(10)

	def run_scenario(self):
		for position in t_o_position:
			if self._scenario_done:
				break
			self.change_next_position(position['start'], 0)
			self._level_done = False
			# run the detect thread
			self.run_instance(position)
		self._scenario_done = True

	def run_instance(self, position):
		follow_thread = Thread(target = self.follow_ego_vehicle, args = (position['start']['yaw'],))
		turning_driving_thread = Thread(target = self.ego_driving, args = (position['destination'],))
		self.start_thread(follow_thread)
		self.start_thread(turning_driving_thread)

		follow_thread.join()
		turning_driving_thread.join()
