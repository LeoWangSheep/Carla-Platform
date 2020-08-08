import time
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from TestScenario.DrivingScenario import DrivingScenario

import carla

b_p_position = [{ 'start' : { 'x' : 165, 'y' : 196, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1}, 
					'destination' : { 'x' : 100, 'y' : 196, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
					'description' : "The walker appear behind the stop stuck",
					'enemy_vehicle' : { 'start' : { 'x' : 120, 'y' : 193, 'z' : 3, 'pitch' : 0, 'yaw' : 180, 'roll' : 0, 'id' : 1},
				  					    'mode' : 'StraightAndWalker' },
					},
				]

actor_blueprint_categories = {
			'car1' : 'vehicle.tesla.model3',
			'truck': 'vehicle.tesla.cybertruck'
		}

class BlindPointScenario(DrivingScenario):
	def __init__(self, weather = None):
		super().__init__(3, weather)

	def set_up_scenario_start(self, agent):
		init_position = b_p_position[0]['start']
		# setting up ego vehicle
		super().set_up_scenario_start(agent, init_position)
		self._agent.bind_vehicle(self._physical_vehicle, target_speed = 40)
		


	def run_scenario(self):
		for position in b_p_position:
			if self._scenario_done:
				break
			self.change_next_position(position, 0)
			self._level_done = False
			self.run_instance(position)
			time.sleep(10)
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
		self._leading_vehicle = Scenario._carla_env.spawn_new_actor(actor_blueprint_categories['truck'], enemy_vehicle_location, enemy_vehicle_rotation, False)

		if self._leading_vehicle is None:
			print("Error Spawn Position")
			return
		self.tmp_actor.append(self._leading_vehicle)
		self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, hand_brake = True))
		self._enemy_mode = enemy_vehicle_map['mode']
		time.sleep(2)

	def run_instance(self, position):
		follow_thread = Thread(target = self.follow_ego_vehicle, args = (position['start']['yaw'],))
		blind_point_thread = Thread(target = self.blind_point_setting, args = (position['enemy_vehicle']['mode'],))
		ego_driving_thread = Thread(target = self.ego_driving, args = (position['destination'],))

		self.start_thread(follow_thread)
		self.start_thread(blind_point_thread)
		self.start_thread(ego_driving_thread)

		blind_point_thread.join()
		ego_driving_thread.join()
		follow_thread.join()
		time.sleep(2)

	def blind_point_setting(self, control):
		leading_transform = self._leading_vehicle.get_transform()
		trigger = False
		if control == "StraightAndWalker":
			walker_location = leading_transform.location
			walker_location.x += -5
			walker_location.z += 1
			walker_rotation = leading_transform.rotation
			walker_rotation.yaw = walker_rotation.yaw - 90
			dangerous_walker = Scenario._carla_env.spawn_new_actor(bp_str = 'walker.pedestrian.0001',
									  location = walker_location,
									  rotation = walker_rotation)
			self.tmp_actor.append(dangerous_walker)
			# self.tmp_actor.append(ai_controller)
		while True:
			if self._scenario_done:
				break
			if self._level_done:
				break
			distance = self.get_distance(self._physical_vehicle, self._leading_vehicle)
			if not trigger:
				if control == "StraightAndWalker":
					if distance <= 14:
						# ai walker start to walk
						if dangerous_walker is not None:
							direction_vec = carla.Vector3D(y = 1, x = 0, z = 0)
							walker_control = carla.WalkerControl(direction = direction_vec, 
																 speed = 1)
							dangerous_walker.apply_control(walker_control)
							# walker_destination = dangerous_walker.get_transform().location
							# walker_destination.y = 205
							# ai_controller.start()
							# ai_controller.go_to_location(walker_destination)
							# trigger = True
		# dangerous_walker.destroy()
		self.release_tmp_actor()
		self._leading_vehicle = None

