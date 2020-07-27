import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from DrivingAgent import CarlaAutoAgent
from CarlaEnv import CarlaSensor
from DrivingAgent.DetectAgent import DetectAgent

import carla

'''
Traffic light position list
containing map which has the variable needed to locate a position
'''
t_l_position = [{ 'x' : 69, 'y' : -133, 'z' : 9, 'pitch' : 0, 'yaw' : 0, 'roll' : 0, 'id' : 1}, 
				{ 'x' : 140, 'y' : -194, 'z' : 1, 'pitch' : 0, 'yaw' : 0, 'roll' : 0, 'id' : 2},
				{ 'x' : 97, 'y' : -136, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 3},
				{ 'x' : 11, 'y' : -182, 'z' : 5, 'pitch' : 0, 'yaw' : -90, 'roll' : 0, 'id' : 4}]

class TrafficLightScenario(Scenario):
	def __init__(self):
		super().__init__(3)
		self._level_done = False

	def set_up_scenario_start(self, agent):
		init_position = t_l_position[0]
		super().set_up_scenario_start(agent, init_position)
		self._traffic_light_lock = Lock()

	def run_scenario(self):
		for position in t_l_position:
			if self._scenario_done:
				break
			# change the traffic light position first
			self.change_next_position(position)
			# set the flag to false
			self._level_done = False
			# run the detect thread
			self.run_instance()
		self._scenario_done = True

	def change_next_position(self, position):
		print("Get to next Traffic light position...: Position" , position['id'])
		super().change_next_position(position, 1)
		self._traffic_light = Scenario._carla_env.get_next_traffic_light(self._physical_vehicle)
		if not isinstance(self._traffic_light, carla.TrafficLight):
			print(self._traffic_light)
			raise Exception("Get error traffic sign")

	'''
	let the detect function and traffic light scenario run concurrently
	'''
	def run_instance(self):
		detect_thread = Thread(target = self.agent_detect)
		traffic_thread = Thread(target = self.traffic_light_change)
		self.start_thread(traffic_thread)
		self.start_thread(detect_thread)
		traffic_thread.join()
		detect_thread.join()

	def traffic_light_change(self):
		tick = 1
		sleep_time = 10
		traffic_light_sign = -1
		while True:
			if self._scenario_done:
				break
			if traffic_light_sign >= 3:
				break
			if sleep_time >= 10:
				traffic_light_sign += 1
				sleep_time = 0
				self.set_traffic_light(traffic_light_sign, 20)
			sleep_time += tick
			time.sleep(tick)
		self._level_done = True

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
			self._traffic_light_lock.acquire()
			print("Detect Result: " , detect_result, " : Actual Result: " , self.get_actual_traffic_state())
			self._traffic_light_lock.release()
			time.sleep(1)
			if self._level_done:
				break

	def set_traffic_light(self, color, timeout):
		self._traffic_light_lock.acquire()
		traffic_light = self._traffic_light
		if color == 0:
			print("set traffic light to Red")
			traffic_light.set_state(carla.TrafficLightState.Red)
			traffic_light.set_red_time(timeout)
		if color == 1:
			print("set traffic light to Yellow")
			traffic_light.set_state(carla.TrafficLightState.Yellow)
			traffic_light.set_yellow_time(timeout)
		if color == 2:
			print("set traffic light to Green")
			traffic_light.set_state(carla.TrafficLightState.Green)
			traffic_light.set_green_time(timeout)
		time.sleep(1)
		self._traffic_light_lock.release()

	def get_actual_traffic_state(self):
		traffic_light = self._traffic_light
		return traffic_light.get_state()
