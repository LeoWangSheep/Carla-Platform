import time
import random
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from DrivingAgent import CarlaAutoAgent
from CarlaEnv import CarlaSensor
from DrivingAgent.DetectAgent import DetectAgent

import carla

o_d_position = [{ 'x' : 165, 'y' : 196, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1}]

actor_blueprint_categories = {
			'car': 'vehicle.tesla.model3',
			'van': 'vehicle.volkswagen.t2',
			'truck': 'vehicle.carlamotors.carlacola',
			'bus': 'vehicle.volkswagen.t2',
			'motorbike': 'vehicle.kawasaki.ninja',
			'bicycle': 'vehicle.diamondback.century',
			'pedestrian': 'walker.pedestrian.0001'
		}


class ObjectDetectScenario(Scenario):
	def __init__(self):
		super().__init__(3)
		self._level_done = False

	def set_up_scenario_start(self, agent):
		init_position = o_d_position[0]
		super().set_up_scenario_start(agent, init_position)
		time.sleep(10)

	def run_scenario(self):
		for position in o_d_position:
			if self._scenario_done:
				break
			# change the object detect position first
			self.change_next_position(position)
			# set the flag to false
			self._level_done = False
			# run the detect thread
			self.run_instance()
		self._scenario_done = True

	def change_next_position(self, position):
		print("Get to next Object Detect position...: Position" , position['id'])
		super().change_next_position(position)

		'''
	let the detect function and object generate scenario run concurrently
	'''
	def run_instance(self):
		detect_thread = Thread(target = self.object_generator)
		self.start_thread(detect_thread)
		detect_thread.join()

	'''
	call the agent detect function
	and compare with actual result
	'''
	def agent_detect(self):
		while True:
			if self._scenario_done:
				break
			input_data = self._sensor_list.get_data()
			detect_result = self._agent.detect(input_data)



			time.sleep(1)
			if self._level_done:
				break


	def object_generator(self):
		vehicle_transform = self._physical_vehicle.get_transform()
		vehicle_location = vehicle_transform.location
		# wirte a triangle
		area_x = -18
		area_y = -10
		dim = area_y / area_x
		re_dim = area_y / -area_x
		object_actor_list = []
		for x in range(3):
			if self._scenario_done:
				break
			new_actor = None
			bp_str = random.sample(actor_blueprint_categories.keys(), 1)
			print(bp_str[0])
			while new_actor is None:
				if self._scenario_done:
					break
				# 此处考虑下yaw
				rand_x = random.uniform(area_x, -4)
				max_y = rand_x * re_dim
				min_y = rand_x * dim
				rand_y = random.uniform(min_y, max_y)
				spawn_x = vehicle_location.x + rand_x
				spawn_y = vehicle_location.y + rand_y
				spawn_z = vehicle_location.z
				print("(x: ", spawn_x, ", y: ", spawn_y, ", z: ", spawn_z, ")" )
				spawn_location = carla.Location(x = spawn_x, y = spawn_y, z = spawn_z)
				new_actor = Scenario._carla_env.spawn_new_actor(actor_blueprint_categories[bp_str[0]], spawn_location)
			object_actor_list.append(new_actor)

		time.sleep(15)

		for actor in object_actor_list:
			actor.destroy()