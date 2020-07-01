import carla
import time

class EgoVehicle(object):
	def __init__(self, env):
		self.__env = env
		self.__world = env.get_world()
		self.__vehicle_blueprint = None
		self.__vehicle = None
		self.__start_ptr = None
		self.__end_ptr = None
		self.__blueprint_library = self.__world.get_blueprint_library()

	def set_start_waypoint(self, _x = 0.000000, _y = 0.000000, _z = 0.000000,\
		_pitch = 0.000000, _yaw = 0.000000, _roll = 0.000000):
		if _x == 0.000000 and _y == 0.000000 and _z == 0.000000 \
		and _pitch == 0.000000 and _yaw == 0.000000 and _roll == 0.000000:
			raise Exception("Empty Waypoint, Please Retry.")

		self.__start_ptr = carla.Transform(carla.Location(x = _x, y = _y, z = _z), \
			carla.Rotation(pitch = _pitch, yaw = _pitch, roll = _roll))

	def set_end_waypoint(self, _x = 0.000000, _y = 0.000000, _z = 0.000000,\
		_pitch = 0.000000, _yaw = 0.000000, _roll = 0.000000):
		if _x == 0.000000 and _y == 0.000000 and _z == 0.000000 \
		and _pitch == 0.000000 and _yaw == 0.000000 and _roll == 0.000000:
			raise Exception("Empty Waypoint, Please Retry.")

		self.__end_ptr = carla.Transform(carla.Location(x = _x, y = _y, z = _z), \
			carla.Rotation(pitch = _pitch, yaw = _pitch, roll = _roll))

	def __set_vehicle_blueprint(self, _filter = "model3", _id = 0):
		self.__vehicle_blueprint = self.__blueprint_library.filter(_filter)[_id]


	def vehicle_initial(self):
		self.__set_vehicle_blueprint()
		# print(self.__vehicle_blueprint)
		# print(self.__start_ptr)
		self.__vehicle = self.__world.spawn_actor(self.__vehicle_blueprint, self.__start_ptr)
		self.__env.add_actor(self.__vehicle)
		

	def follow_ego(self):
		spectator = self.__world.get_spectator()
		transform = self.__vehicle.get_transform()
		spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50), \
		carla.Rotation(pitch=-90)))

	def get_vehicle(self):
		return self.__vehicle

	def drive(self):
		self.__vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
		time.sleep(10)