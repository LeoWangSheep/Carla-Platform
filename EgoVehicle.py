import carla
import time
from CommonTool import misc
import CarlaSensor

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

	def __set_vehicle_blueprint(self, _filter = "model3", _id = 0):
		self.__vehicle_blueprint = self.__blueprint_library.filter(_filter)[_id]


	def vehicle_initial(self):
		self.__set_vehicle_blueprint()
		# print(self.__vehicle_blueprint)
		# print(self.__start_ptr)
		self.__vehicle = self.__world.spawn_actor(self.__vehicle_blueprint, self.__start_ptr)
		self.__env.add_actor(self.__vehicle)
		

	def get_vehicle(self):
		return self.__vehicle

	def bind_collision_sensor(self):
		self.__collision_sensor = CarlaSensor.CollisionSensor(self.__env)
		self.__collision_sensor.attach_to_vehicle(self.__vehicle)

	def bind_gnss_sensor(self):
		self.__gnss_sensor = CarlaSensor.GnssSensor(self.__env)
		self.__gnss_sensor.attach_to_vehicle(self.__vehicle)

	def bind_center_camera(self):
		self.__rear_camera = CarlaSensor.RGBCamera(self.__env, 0)
		self.__rear_camera.attach_to_vehicle(self.__vehicle)

	def bind_left_camera(self):
		self.__rear_camera = CarlaSensor.RGBCamera(self.__env, 1)
		self.__rear_camera.attach_to_vehicle(self.__vehicle)

	def bind_right_camera(self):
		self.__rear_camera = CarlaSensor.RGBCamera(self.__env, 2)
		self.__rear_camera.attach_to_vehicle(self.__vehicle)

	def bind_rear_camera(self):
		self.__rear_camera = CarlaSensor.RGBCamera(self.__env, 3)
		self.__rear_camera.attach_to_vehicle(self.__vehicle)

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