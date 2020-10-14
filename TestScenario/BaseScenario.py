import time
import pygame
from threading import Thread

from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle
from CarlaEnv import CarlaSensor

import carla

class Scenario(object):
	_carla_env = None
	def __init__(self, town_id, weather = None):
		pygame.display.init()
		'''
		The _scenario_done flag can be used to decide that the scenario should be stopped
		All the thread in this scenarios should stop when this flag is set to True 
		'''
		self._scenario_done = False
		Scenario._carla_env = CarlaEnvironment(town_id, weather = weather)
		self._my_ego_vehicle = EgoVehicle(Scenario._carla_env)
		self.tmp_actor = []
		self.info_dataframe = {}
		if weather is not None:
			self.info_dataframe = weather.get_weather_dict()
		self.info_dataframe['time_stamp'] = time.time()
		self.info_dataframe['date_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


	def set_up_scenario_start(self, agent, position):
		self._set_scenario_pause_ready()
		self._agent = agent
		self._my_ego_vehicle.bind_agent(self._agent)
		self._my_ego_vehicle.set_start_waypoint( _x = position['x'], _y = position['y'], _z = position['z'],\
									  _pitch = position['pitch'], _yaw = position['yaw'], _roll = position['roll'])
		self._my_ego_vehicle.vehicle_initial()
		self._physical_vehicle = self._my_ego_vehicle.get_vehicle()
		self._my_ego_vehicle.stop()
		self._sensor_list = CarlaSensor.SensorList(Scenario._carla_env, self._agent)
		self._sensor_list.setup_sensor(self._physical_vehicle)
		time.sleep(1)

	def run_scenario(self):
		self._scenario_done = True

	def scenario_done(self):
		return self._scenario_done

	def scenario_end(self):
		self._jump_out_thread.join()
		pygame.quit()
		Scenario._carla_env.clean_actors()

	def _set_scenario_pause_ready(self):
		self._jump_out_thread = Thread(target = self._scenario_jump_out)
		self.start_thread(self._jump_out_thread)


	def _scenario_jump_out(self):
		while True:
			if self._scenario_done:
					break
			for event_type in pygame.event.get():
				if self._scenario_done:
					break
				if event_type.type == pygame.QUIT:
					print("KeyBoard Interrupt, quiting...please wait...")
					self._scenario_done = True
					break
					

	def start_thread(self, new_thread):
		new_thread.setDaemon(True)
		new_thread.start()

	def change_next_position(self, position, mode):
		next_transform = carla.Transform(carla.Location(x = position['x'], y = position['y'], z = position['z']), \
			carla.Rotation(pitch = position['pitch'], yaw = position['yaw'], roll = position['roll']))
		self._physical_vehicle.set_transform(next_transform)
		self._my_ego_vehicle.stop()
		print("setting up ego vehicle...")
		time.sleep(2)
		if mode == 1:
			Scenario._carla_env.follow_actor(self._physical_vehicle, mode = 1, a_yaw = position['yaw'])
		elif mode == 0:
			Scenario._carla_env.follow_actor(self._physical_vehicle, mode = 0, a_yaw = position['yaw'])

	def release_tmp_actor(self):
		for actor in self.tmp_actor:
			if actor is not None:
				actor.destroy()

	def get_data_frame(self):
		return self.info_dataframe

