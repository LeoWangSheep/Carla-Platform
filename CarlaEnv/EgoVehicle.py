import carla
from DrivingAgent import CarlaAutoAgent
from CommonTool.agents.tools import misc

import time
from CarlaEnv import CarlaSensor

class EgoVehicle(object):
	def __init__(self, env):
		self.__env = env
		self.__world = env.get_world()
		self.__vehicle_blueprint = None
		self.__vehicle = None
		self.__start_ptr = None
		self.__end_ptr = None
		self.__blueprint_library = self.__world.get_blueprint_library()
		self.__collision_sensor = None
		self.__gnss_sensor = None
		self.__rear_camera = None
		self.__agent = None

	def set_start_waypoint(self, _x = 0.000000, _y = 0.000000, _z = 0.000000,\
		_pitch = 0.000000, _yaw = 0.000000, _roll = 0.000000):
		if _x == 0.000000 and _y == 0.000000 and _z == 0.000000 \
		and _pitch == 0.000000 and _yaw == 0.000000 and _roll == 0.000000:
			raise Exception("Empty Waypoint, Please Retry.")

		self.__start_ptr = carla.Transform(carla.Location(x = _x, y = _y, z = _z), \
			carla.Rotation(pitch = _pitch, yaw = _yaw, roll = _roll))

	def set_end_waypoint(self, _x = 0.000000, _y = 0.000000, _z = 0.000000,\
		_pitch = 0.000000, _yaw = 0.000000, _roll = 0.000000):
		if _x == 0.000000 and _y == 0.000000 and _z == 0.000000 \
		and _pitch == 0.000000 and _yaw == 0.000000 and _roll == 0.000000:
			raise Exception("Empty Waypoint, Please Retry.")

		self.__end_ptr = carla.Transform(carla.Location(x = _x, y = _y, z = _z), \
			carla.Rotation(pitch = _pitch, yaw = _yaw, roll = _roll))

	def __set_vehicle_blueprint(self, _filter = "model3", _id = 0, is_ego = True):
		self.__vehicle_blueprint = self.__blueprint_library.filter(_filter)[_id]
		if is_ego:
			self.__vehicle_blueprint.set_attribute('color', '0,0,0')
		elif not is_ego:
			self.__vehicle_blueprint.set_attribute('color', '255,255,255')


	def vehicle_initial(self, v_filter = "model3", v_id = 0, is_ego = True):
		self.__set_vehicle_blueprint(v_filter, v_id, is_ego)
		# print(self.__vehicle_blueprint)
		# print(self.__start_ptr)
		self.__vehicle = self.__world.spawn_actor(self.__vehicle_blueprint, self.__start_ptr)
		self.__env.add_actor(self.__vehicle)
		

	def get_vehicle(self):
		return self.__vehicle

	def drive(self):
		#self.__vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
		self.__vehicle.set_autopilot(True)
		tick = 0.05
		all_time = 0
		while all_time < 50:
			# speed = misc.get_speed(self.__vehicle)
			# print("vehicle speed: ", speed, " : time: ", all_time)
			# ego_vehicle_location = self.__vehicle.get_location()
			# ego_vehicle_waypoint = self.__vehicle.get_world().get_map().get_waypoint(ego_vehicle_location)
			# driving_waypoints.append(ego_vehicle_waypoint)
			self.__env.follow_actor(self.__vehicle)
			time.sleep(tick)
			all_time += tick
		self.__vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0))

	def stop(self):
		self.__vehicle.apply_control(carla.VehicleControl(hand_brake = True))


	def stop_agent(self):
		self.__agent = CarlaAutoAgent.AutoAgent(self.__vehicle)
		self.__sensor_list = CarlaSensor.SensorList(self.__env, self.__agent)
		self.__sensor_list.setup_sensor(self.__vehicle)
		
	def apply_default_agent(self):
		self.__agent = CarlaAutoAgent.AutoAgent(self.__vehicle)
		self.__sensor_list = CarlaSensor.SensorList(self.__env, self.__agent)
		self.__sensor_list.setup_sensor(self.__vehicle)

		target = self.__end_ptr.location
		self.__agent.set_destination((target.x,
									  target.y,
									  target.z,))
		print("start!")
		start_time = 0
		threshold = 5000
		while True:
			start_time += 1
			if start_time >= threshold:
				print("time out")
				break
			# input_data = self.__sensor_list.get_data()
			# print(input_data['Center']['data'])
			control = self.__agent.run_step()
			self.__vehicle.apply_control(control)
			self.__env.follow_actor(self.__vehicle, 100)
			current_pos = self.__vehicle.get_location()
			print(current_pos)
			if self.__agent.done():
				print("done!")
				break
		# self.__sensor_list.destroy_sensors()

	def bind_agent(self, agent):
		self.__agent = agent