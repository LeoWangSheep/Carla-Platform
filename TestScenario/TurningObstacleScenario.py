import time
import random
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from TestScenario.DrivingScenario import DrivingScenario

import carla

t_o_position = [    {'start' : { 'x' : 105, 'y' : -73, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				     'destination' : { 'x' : 76, 'y' : -50, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1},
				     'enemy_vehicle' : None ,
				     'description' : "Turning Scenario with no other vehicle." },
				    {'start' : { 'x' : 105, 'y' : -73, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				     'destination' : { 'x' : 76, 'y' : -50, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1},
				     'enemy_vehicle' : { 'start' : { 'x' : 79, 'y' : -65, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1},
				   					   'mode' : 'Stop' },
				     'description' : "Turning Scenario with one stop vehicle." },
				   {'start' : { 'x' : 105, 'y' : -73, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				    'destination' : { 'x' : 76, 'y' : -50, 'z' : 10, 'pitch' : 0, 'yaw' : 90, 'roll' : 0, 'id' : 1},
				    'enemy_vehicle' : { 'start' : { 'x' : 83, 'y' : -65, 'z' : 10, 'pitch' : 0, 'yaw' : -90, 'roll' : 0, 'id' : 1},
				   					   'mode' : 'Fast' },
				     'description' : "Turning Scenario with one rush vehicle." }, 
				]

actor_blueprint_categories = {
			'car1' : 'vehicle.tesla.model3',
			'car2' : 'vehicle.audi.a2'
		}

class TurningObstacleScenario(DrivingScenario):
	def __init__(self, weather = None):
		super().__init__(3, weather)
		self._enemy_vehicle = None
		self._enemy_mode = ""

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
			self.change_next_position(position, 0)
			time.sleep(2)
			self._level_done = False
			# run the detect thread
			self.run_instance(position)
			time.sleep(2)
		self._scenario_done = True

	def change_next_position(self, position, mode):
		print("Scenario: " , position['description'])
		super().change_next_position(position['start'], mode)
		enemy_vehicle_map = position['enemy_vehicle']
		if enemy_vehicle_map is None or enemy_vehicle_map['start'] is None:
			self._enemy_vehicle = None
			self._enemy_mode = ""
			return
		enemy_position = enemy_vehicle_map['start']
		enemy_vehicle_location = carla.Location(x = enemy_position['x'], y = enemy_position['y'], z = enemy_position['z'])
		enemy_vehicle_rotation = carla.Rotation(pitch = enemy_position['pitch'], yaw = enemy_position['yaw'], roll = enemy_position['roll'])
		self._enemy_vehicle = Scenario._carla_env.spawn_new_actor(actor_blueprint_categories['car2'], enemy_vehicle_location, enemy_vehicle_rotation, False)

		if self._enemy_vehicle is None:
			print("Error Spawn Position")
			return
		self._enemy_vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, hand_brake = True))
		self._enemy_mode = enemy_vehicle_map['mode']


	def run_instance(self, position):
		follow_thread = Thread(target = self.follow_ego_vehicle, args = (position['start']['yaw'],))
		turning_driving_thread = Thread(target = self.ego_driving, args = (position['destination'],))
		enemy_vehicle_thread = Thread(target = self.enemy_vehicle_operation)
		self.start_thread(follow_thread)
		self.start_thread(enemy_vehicle_thread)
		self.start_thread(turning_driving_thread)
		enemy_vehicle_thread.join()
		follow_thread.join()
		turning_driving_thread.join()

	def enemy_vehicle_operation(self):
		if self._enemy_vehicle is None:
			return
		if self._enemy_mode == "":
			return
		tick = 0.5
		while True:
			if self._scenario_done:
				break
			# time.sleep(tick)
			distance = self.get_distance(self._physical_vehicle, self._enemy_vehicle)
			if self._enemy_mode == "Stop":
				# print("distance: ", distance)
				if distance < 10:
					time.sleep(10)
					for i in range(20):
						self._enemy_vehicle.apply_control(carla.VehicleControl(throttle=1, steer=0.0))
						time.sleep(1)
					break

			if self._enemy_mode == "Fast":
				rush_time = random.randint(17, 20)
				if distance < rush_time:
					# print(distance , " : ", rush_time)
					for i in range(20):
						self._enemy_vehicle.apply_control(carla.VehicleControl(throttle=1, steer=0.0))
						time.sleep(1)
					break

		self._enemy_vehicle.destroy()
		self._enemy_vehicle = None
		self._enemy_mode = ""
