from CarlaEnv.EnvironmentSetting import CarlaEnvironment
from CarlaEnv.EgoVehicle import EgoVehicle


class Scenario(object):
	def __init__(self, town_id):
		self._scenario_done = False
		self._carla_env = CarlaEnvironment(town_id)
		self._my_ego_vehicle = EgoVehicle(self._carla_env)
	def set_up_scenario_start(self):
		pass

	def run_scenario(self):
		pass

	def scenario_done(self):
		pass

