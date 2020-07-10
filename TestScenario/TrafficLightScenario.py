import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from DrivingAgent import CarlaAutoAgent
from CarlaEnv import CarlaSensor

import carla

class TrafficLightScenario(Scenario):
	def __init__(self):
		super().__init__(3)

	def set_up_scenario_start(self, agent):
		self._agent = agent
		# 检测下agent是否detect

		self._my_ego_vehicle.bind_agent(self._agent)
		self._my_ego_vehicle.set_start_waypoint( _x = 69, _y = -133, _z = 10,\
									  _pitch = 0, _yaw = 0, _roll = 0)
		self._my_ego_vehicle.vehicle_initial()
		self._carla_env.follow_actor(self._my_ego_vehicle.get_vehicle())
		self._my_ego_vehicle.stop()
		self._sensor_list = CarlaSensor.SensorList(self._carla_env, self._agent)
		self._sensor_list.setup_sensor(self._my_ego_vehicle.get_vehicle())
		time.sleep(1)
		self._traffic_light = self._my_ego_vehicle.get_vehicle().get_traffic_light()
		self._traffic_light_lock = Lock()

	def run_scenario(self):
		detect_thread = Thread(target = self.agent_detect)
		traffic_thread = Thread(target = self.traffic_light_change)
		detect_thread.setDaemon(True)
		traffic_thread.setDaemon(True)
		traffic_thread.start()
		detect_thread.start()
		detect_thread.join()
		traffic_thread.join()
		print("done")

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
		print("detect ends")

	def scenario_done(self):
		return self._scenario_done

	def scenario_end(self):
		self._carla_env.clean_actors()

	def set_traffic_light(self, color, timeout):
		#if vehicle.is_at_traffic_light():
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
