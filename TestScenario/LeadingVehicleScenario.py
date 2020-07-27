import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from TestScenario.DrivingScenario import DrivingScenario

import carla

l_v_position = [ { 'x' : 165, 'y' : 196, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1} ]

l_v_destination = [{ 'x' : -45, 'y' : 196, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1}]

actor_blueprint_categories = {
			'car1' : 'vehicle.tesla.model3',
			'car2' : 'vehicle.audi.a2'
		}

class LeadingVehicleScenario(DrivingScenario):
	def __init__(self):
		super().__init__(3)

	def set_up_scenario_start(self, agent):
		init_position = l_v_position[0]
		# setting up ego vehicle
		super().set_up_scenario_start(agent, init_position)
		self._agent.bind_vehicle(self._physical_vehicle)
		time.sleep(1)
		enemy_vehicle_location = carla.Location(x = init_position['x'] - 10, y = init_position['y'], z = init_position['z'])
		enemy_vehicle_rotation = carla.Rotation(pitch = init_position['pitch'], yaw = init_position['yaw'], roll = init_position['roll'])
		self._leading_vehicle = Scenario._carla_env.spawn_new_actor(bp_str = actor_blueprint_categories['car2'], 
											location = enemy_vehicle_location, 
											rotation = enemy_vehicle_rotation,
											stop = False)

	def run_scenario(self):
		for position in l_v_position:
			if self._scenario_done:
				break
			# run the detect thread
			self.run_instance()
		self._scenario_done = True


	def run_instance(self):
		follow_thread = Thread(target = self.follow_ego_vehicle, args = (l_v_position[0]['yaw'],))
		leading_driving_thread = Thread(target = self.leading_driving)
		ego_driving_thread = Thread(target = self.ego_driving, args = (l_v_destination[0],))

		self.start_thread(follow_thread)
		self.start_thread(leading_driving_thread)
		self.start_thread(ego_driving_thread)

		leading_driving_thread.join()
		ego_driving_thread.join()
		follow_thread.join()

	def leading_driving(self):
		print("Leading Vehicle Driving...")
		while True:
			if self._scenario_done:
				break
			if self._level_done:
				break
			leading_v = self._leading_vehicle.get_location().x
			ego_v = self._physical_vehicle.get_location().x
			distance = abs(leading_v - ego_v)
			if distance > 14:
				self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake = 1.0, steer=0.0))
				time.sleep(6)
			elif distance <= 14:
				self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.8, steer=0.0))

	def scenario_end(self):
		self._leading_vehicle.destroy()
		super().scenario_end()