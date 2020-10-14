import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from Marking.MarkingScore import Marking
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
				{ 'x' : 11, 'y' : -182, 'z' : 5, 'pitch' : 0, 'yaw' : -90, 'roll' : 0, 'id' : 4}
				]

class TrafficLightScenario(Scenario):
	def __init__(self, weather = None):
		super().__init__(3, weather)
		self.info_dataframe['Scenario'] = 'Traffic Light Detection'
		self._level_done = False

	def set_up_scenario_start(self, agent):
		init_position = t_l_position[0]
		super().set_up_scenario_start(agent, init_position)
		self._traffic_light_lock = Lock()
		self._correct_answer = []
		self.marking_tool = Marking(mode='detect')

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
		accuracy, avg_time, mark, detects, answers = self.marking_tool.detect_result()
		self.info_dataframe['accuracy'] = accuracy
		self.info_dataframe['avg_time'] = avg_time
		self.info_dataframe['mark'] = mark
		self.info_dataframe['detects'] = detects
		self.info_dataframe['answers'] = answers

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
			self._traffic_light_lock.acquire()
			input_data = self._sensor_list.get_data()
			start_time = time.time()
			self._correct_answer = self.get_actual_traffic_state()
			detect_result = self._agent.detect(input_data)
			end_time = time.time()
			print("Detect Result: " , detect_result, " : Actual Result: " , self._correct_answer)
			self._traffic_light_lock.release()
			duration = end_time - start_time
			self.marking_tool.detect_marking(detecteds=detect_result, targets=self._correct_answer, cost_time=duration)
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
		answer_str = traffic_light.get_state()
		correct_answer = [str(answer_str)]
		return correct_answer
