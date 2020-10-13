import time
import random
import operator
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from DrivingAgent import CarlaAutoAgent
from CarlaEnv import CarlaSensor
from DrivingAgent.DetectAgent import DetectAgent

import carla

o_d_position = [ { 'location' : { 'x' : 165, 'y' : 196, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				   'control' : { 'z_offset' : 0, 'physical_stop' : True },
				   'description' : "Object Detect Scenario in broaden and clear area."
					},
				 { 'location' : { 'x' : 71, 'y' : -197, 'z' : 1, 'pitch' : 0, 'yaw' : 0, 'roll' : 0, 'id' : 2},
				   'control' : { 'z_offset' : 0.5, 'physical_stop' : False },
				   'description' : "Object Detect Scenario in complex environment."
					}, 
				 ]


actor_blueprint_categories = {
			'car': 'vehicle.tesla.model3',
			 # 'van': 'vehicle.volkswagen.t2',
			 # 'truck': 'vehicle.carlamotors.carlacola',
			'bus': 'vehicle.volkswagen.t2',
			'motorbike': 'vehicle.kawasaki.ninja',
			'bicycle': 'vehicle.diamondback.century',
			'pedestrian': 'walker.pedestrian.0001'
		}


class ObjectDetectScenario(Scenario):
	def __init__(self, weather=None):
		super().__init__(3, weather)
		self._level_done = False

	def set_up_scenario_start(self, agent):
		self._correct_answer = []
		self.time_out = False
		init_position = o_d_position[0]['location']
		super().set_up_scenario_start(agent, init_position)

	def run_scenario(self):
		for position in o_d_position:
			if self._scenario_done:
				break
			# change the object detect position first
			self.change_next_position(position)
			# set the flag to false
			self._level_done = False
			# run the detect thread
			self.run_instance(position)
		self._scenario_done = True

	def change_next_position(self, position):
		print("Scenario: " , position['description'])
		super().change_next_position(position['location'], 1)

		'''
	let the detect function and object generate scenario run concurrently
	'''
	def run_instance(self, position):
		for x in range(3):
			self.object_generator(position)
			sleep_thread = Thread(target = self.counting_time)
			detect_thread = Thread(target = self.agent_detect)
			self.start_thread(sleep_thread)
			self.start_thread(detect_thread)
			sleep_thread.join()
			detect_thread.join()
			self.release_object()

	'''
	call the agent detect function
	and compare with actual result
	'''
	def agent_detect(self):
		if self._scenario_done:
			return
		input_data = self._sensor_list.get_data()
		start_time = time.time()
		detect_result = self._agent.detect(input_data)
		if self.time_out:
			print("Time ran out, detect failed")
		end_time = time.time()
		print("Detect Result: ", detect_result, ", Actual Result: ", self._correct_answer)
		duration = end_time - start_time
		print("Detect Time Cost: ", duration, "s")
		time.sleep(1)
			


	def object_generator(self, position):
		vehicle_transform = self._physical_vehicle.get_transform()
		vehicle_location = vehicle_transform.location
		this_yaw = position['location']['yaw']
		control_arg = position['control']
		physical_stop = control_arg['physical_stop']
		# print(this_yaw)
		if this_yaw == 0:
			# wirte a triangle
			area_x = 18
			area_y = -9
			dim = area_y / area_x
			re_dim = area_y / -area_x
			distance_from_v = 4
			low_bound = distance_from_v
			up_bound = area_x
			reverse = False
		elif this_yaw == 180:
			# wirte a triangle
			area_x = -18
			area_y = -9
			dim = area_y / area_x
			re_dim = area_y / -area_x
			distance_from_v = -4
			low_bound = area_x
			up_bound = distance_from_v
			physical_stop = True
			spawn_z = vehicle_location.z
			reverse = True
		else:
			raise Exception("Bad yaw, please re-spawn a good position")
		self.object_actor_list = []
		current_correct_ans = []
		for x in range(3):
			if self._scenario_done:
				break
			new_actor = None
			bp_str = random.sample(actor_blueprint_categories.keys(), 1)
			# print(bp_str[0])
			while new_actor is None:
				if self._scenario_done:
					break
				# 此处考虑下yaw
				rand_x = random.uniform(low_bound, up_bound)
				max_y = rand_x * re_dim
				min_y = rand_x * dim
				rand_y = random.uniform(min_y, max_y)
				spawn_x = vehicle_location.x + rand_x
				spawn_y = vehicle_location.y + rand_y
				spawn_z = vehicle_location.z + control_arg['z_offset']
				# print("(x: ", spawn_x, ", y: ", spawn_y, ", z: ", spawn_z, ")" )
				spawn_location = carla.Location(x = spawn_x, y = spawn_y, z = spawn_z)
				# print(bp_str[0], spawn_location)
				new_actor = Scenario._carla_env.spawn_new_actor(actor_blueprint_categories[bp_str[0]], spawn_location, stop = physical_stop)
			this_set = {'actor' : new_actor, 'actor_name': bp_str[0], 'y' : spawn_y}
			self.object_actor_list.append(this_set)
			# print(object_actor_list)
		self.object_actor_list.sort(key = operator.itemgetter('y'), reverse = reverse)
		for actor_set in self.object_actor_list:
			current_correct_ans.append(actor_set['actor_name'])
		self._correct_answer = current_correct_ans
		time.sleep(2.5)

	def counting_time(self):
		tick = 0.5
		stop_time = 0
		threshold = 10
		while True:
			if self._scenario_done:
				break
			if stop_time >= threshold:
				break
			time.sleep(tick)
			stop_time += tick
		self.time_out = True

	def release_object(self):
		for actor_set in self.object_actor_list:
			actor_set['actor'].destroy()
		time.sleep(1)
		self.time_out = False
