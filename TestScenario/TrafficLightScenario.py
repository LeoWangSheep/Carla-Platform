import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from DrivingAgent import CarlaAutoAgent
from CarlaEnv import CarlaSensor
from DrivingAgent.DetectAgent import DetectAgent

import carla

t_l_position = [{ 'x' : 69, 'y' : -133, 'z' : 10, 'pitch' : 0, 'yaw' : 0, 'roll' : 0, 'id' : 1}, 
				{ 'x' : 140, 'y' : -194, 'z' : 1, 'pitch' : 0, 'yaw' : 0, 'roll' : 0, 'id' : 2},
				{ 'x' : 97, 'y' : -136, 'z' : 10, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 3},
				{ 'x' : 11, 'y' : -182, 'z' : 5, 'pitch' : 0, 'yaw' : -90, 'roll' : 0, 'id' : 4}]

class TrafficLightScenario(Scenario):
	def __init__(self):
		super().__init__(3)

	def set_up_scenario_start(self, agent):
		self._agent = agent
		if not isinstance(self._agent, DetectAgent):
			raise Exception("This agent is not a detect agent")
		self._my_ego_vehicle.bind_agent(self._agent)
		self._my_ego_vehicle.set_start_waypoint( _x = 69, _y = -133, _z = 10,\
									  _pitch = 0, _yaw = 0, _roll = 0)
		self._my_ego_vehicle.vehicle_initial()
		self._physical_vehicle = self._my_ego_vehicle.get_vehicle()
		# self._carla_env.follow_actor(self._physical_vehicle)
		self._my_ego_vehicle.stop()
		self._sensor_list = CarlaSensor.SensorList(self._carla_env, self._agent)
		self._sensor_list.setup_sensor(self._physical_vehicle)
		print("setting up vehicle...")
		time.sleep(1)
		self._traffic_light_lock = Lock()

	def run_scenario(self):

		for position in t_l_position:
			# change the traffic light position first
			self.change_next_position(position)
			# set the flag to false
			self._scenario_done = False
			# run the detect thread
			self.run_instance()

	def change_next_position(self, position):
		print("Get to next Traffic light position...: Position" , position['id'])
		next_transform = carla.Transform(carla.Location(x = position['x'], y = position['y'], z = position['z']), \
			carla.Rotation(pitch = position['pitch'], yaw = position['yaw'], roll = position['roll']))
		self._physical_vehicle.set_transform(next_transform)
		self._my_ego_vehicle.stop()
		print("setting up vehicle...")
		time.sleep(2)
		self._carla_env.follow_actor(self._physical_vehicle)
		self._traffic_light = self._carla_env.get_next_traffic_light(self._physical_vehicle)
		if not isinstance(self._traffic_light, carla.TrafficLight):
			print(self._traffic_light)
			raise Exception("Get error traffic sign")

	def run_instance(self):
		detect_thread = Thread(target = self.agent_detect)
		traffic_thread = Thread(target = self.traffic_light_change)
		detect_thread.setDaemon(True)
		traffic_thread.setDaemon(True)
		traffic_thread.start()
		detect_thread.start()
		traffic_thread.join()
		detect_thread.join()
		# print("done")

	def traffic_light_change(self):
		# red light
		self.set_traffic_light(0, 20)
		time.sleep(10)
		# yellow light
		self.set_traffic_light(1, 20)
		time.sleep(10)
		# green light
		self.set_traffic_light(2, 20)
		time.sleep(10)
		self._scenario_done = True

	def agent_detect(self):
		while True:
			input_data = self._sensor_list.get_data()
			detect_result = self._agent.detect(input_data)
			self._traffic_light_lock.acquire()
			print("Detect Result: " , detect_result, " : Actual Result: " , self.get_actual_traffic_state())
			self._traffic_light_lock.release()
			time.sleep(1)
			if self.scenario_done():
				break
		# print("detect ends")

	def set_traffic_light(self, color, timeout):
		#if vehicle.is_at_traffic_light():
		self._traffic_light_lock.acquire()
		traffic_light = self._traffic_light
		# print(self._traffic_light)
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
