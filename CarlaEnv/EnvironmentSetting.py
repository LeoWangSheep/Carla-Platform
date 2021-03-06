import carla
import time
from CarlaEnv.EgoVehicle import EgoVehicle

class CarlaEnvironment(object):
	_traffic_light_map = dict()
	_world = None
	_map = None
	_client = None
	_blueprint_library = None
	_weather = None

	def __init__(self, town_id = 3,  _host = 'localhost', _port = 2000, _expired_time = 10.0, weather = None):
		CarlaEnvironment._client = carla.Client(_host, _port)
		try:
			CarlaEnvironment._client.set_timeout(_expired_time)
			town_str = 'Town0' + str(town_id)
			CarlaEnvironment._world = CarlaEnvironment._client.get_world()
		except Exception as e:
			raise Exception("Cannot connect the Carla Server, Please launch your CarlaUE4.exe/.sh.")
		# self.__world = self.__client.load_world(town_str)
		if weather != None:
			CarlaEnvironment.set_weather(weather)
		else:
			CarlaEnvironment._weather = carla.WeatherParameters()
			CarlaEnvironment._world.set_weather(CarlaEnvironment._weather)

		CarlaEnvironment._blueprint_library = CarlaEnvironment._world.get_blueprint_library()
		self.__actor_list = []
		CarlaEnvironment.prepare_map()

	def get_world(self):
		return CarlaEnvironment._world

	def spawn_stop_vehicle(self, x = 0.000000, y = 0.000000, z = 0.000000,\
		pitch = 0.000000, yaw = 0.000000, roll = 0.000000):
		stop_vehicle = EgoVehicle(self)
		stop_vehicle.set_start_waypoint( _x = x, _y = y, _z = z,\
									  _pitch = pitch, _yaw = yaw, _roll = roll)
		stop_vehicle.vehicle_initial()

	def add_actor(self, _actor):
		self.__actor_list.append(_actor)

	def clean_actors(self):
		for actor in self.__actor_list:
			if actor is not None:
				actor.destroy()
		print("All clearned up!")
	'''
	mode:
		0: from up to down
		1: from back to front
		2: from the vehicle to the front
	'''
	def follow_actor(self, actor, height = 50, a_yaw = 0, mode = 0):
		spectator = CarlaEnvironment._world.get_spectator()
		transform = actor.get_transform()
		if mode == 0:
			spectator.set_transform(carla.Transform(transform.location + carla.Location(z = height), \
			carla.Rotation(pitch=-90, yaw = a_yaw)))
		elif mode == 1:
			offset = carla.Location()
			if a_yaw == 180:
				offset = carla.Location(x=8, y=-3, z=3)
			elif a_yaw == 0:
				offset = carla.Location(x=-8, y=3, z=3)
			spectator.set_transform(carla.Transform(transform.location + offset, \
			carla.Rotation(yaw = a_yaw)))
		elif mode == 2:
			offset = carla.Location(x=0, y=0, z=2)
			spectator.set_transform(carla.Transform(transform.location + offset,
													transform.rotation))


	def spawn_new_actor(self, bp_str, location, rotation = None, stop = False):
		t_transform = None
		if rotation is None:
			t_transform = carla.Transform(location, carla.Rotation())
		else:
			t_transform = carla.Transform(location, rotation)
		bp = CarlaEnvironment._blueprint_library.filter(bp_str)[0]
		spawn_rst = CarlaEnvironment._world.try_spawn_actor(bp, t_transform)
		if spawn_rst is not None and stop:
			spawn_rst.set_simulate_physics(False)
		return spawn_rst


	def set_town(self, town_id):
		town_str = 'Town0' + str(town_id)
		print(town_str)
		CarlaEnvironment._client.load_world(town_str)

	def spawn_dangerous_walker(self, location, rotation = None):
		percentagePedestriansCrossing = 1
		walker_controller_bp = CarlaEnvironment._world.get_blueprint_library().find('controller.ai.walker')
		print(walker_controller_bp)
		walker = self.spawn_new_actor(bp_str = 'walker.pedestrian.0001',
									  location = location,
									  rotation = rotation)
		CarlaEnvironment._world.set_pedestrians_cross_factor(percentagePedestriansCrossing)
		ai_controller = None
		if walker is not None:
			walker_controller_bp = CarlaEnvironment._blueprint_library.find('controller.ai.walker')
			ai_controller = CarlaEnvironment._world.try_spawn_actor(walker_controller_bp, carla.Transform(), walker)
			print(ai_controller)
		return walker, ai_controller

	@staticmethod
	def set_weather(weather_arg):
		CarlaEnvironment._weather = carla.WeatherParameters()
		CarlaEnvironment._weather.cloudiness = weather_arg.clouds
		CarlaEnvironment._weather.precipitation = weather_arg.rain
		CarlaEnvironment._weather.precipitation_deposits = weather_arg.puddles
		CarlaEnvironment._weather.wind_intensity = weather_arg.wind
		CarlaEnvironment._weather.fog_density = weather_arg.fog
		CarlaEnvironment._weather.wetness = weather_arg.wetness
		CarlaEnvironment._weather.sun_azimuth_angle = weather_arg.azimuth
		CarlaEnvironment._weather.sun_altitude_angle = weather_arg.altitude
		CarlaEnvironment._world.set_weather(CarlaEnvironment._weather)
		# print(CarlaEnvironment._world.get_weather())


	@staticmethod
	def prepare_map():
		"""
		This function set the current map and loads all traffic lights for this map to
		_traffic_light_map
		"""
		if CarlaEnvironment._map is None:
			CarlaEnvironment._map = CarlaEnvironment._world.get_map()

		# Parse all traffic lights
		CarlaEnvironment._traffic_light_map.clear()
		for traffic_light in CarlaEnvironment._world.get_actors().filter('*traffic_light*'):
			# print("register:", traffic_light)
			if traffic_light not in CarlaEnvironment._traffic_light_map.keys():
				CarlaEnvironment._traffic_light_map[traffic_light] = traffic_light.get_transform()
			else:
				raise KeyError(
					"Traffic light '{}' already registered. Cannot register twice!".format(traffic_light.id))

	def set_traffic_light(self, vehicle, color):
		if vehicle.is_at_traffic_light():
			traffic_light = vehicle.get_traffic_light()
			if color == 0:
				traffic_light.set_state(carla.TrafficLightState.Red)
			if color == 1:
				traffic_light.set_state(carla.TrafficLightState.Yellow)
			if color == 2:
				traffic_light.set_state(carla.TrafficLightState.Green)

	@staticmethod
	def get_next_traffic_light(actor):
		"""
		returns the next relevant traffic light for the provided actor
		"""
		location = actor.get_transform().location
		waypoint = CarlaEnvironment._map.get_waypoint(location)
		# Create list of all waypoints until next intersection
		list_of_waypoints = []
		while waypoint and not waypoint.is_intersection:
			list_of_waypoints.append(waypoint)
			waypoint = waypoint.next(2.0)[0]

		# If the list is empty, the actor is in an intersection
		if not list_of_waypoints:
			return None

		relevant_traffic_light = None
		distance_to_relevant_traffic_light = float("inf")

		for traffic_light in CarlaEnvironment._traffic_light_map:
			if hasattr(traffic_light, 'trigger_volume'):
				tl_t = CarlaEnvironment._traffic_light_map[traffic_light]
				transformed_tv = tl_t.transform(traffic_light.trigger_volume.location)
				distance = carla.Location(transformed_tv).distance(list_of_waypoints[-1].transform.location)

				if distance < distance_to_relevant_traffic_light:
					relevant_traffic_light = traffic_light
					distance_to_relevant_traffic_light = distance

		return relevant_traffic_light


if __name__ == '__main__':
	try:
		carla_env = CarlaEnvironment()
	except Exception as e:
		print("Error Occur :", e)
	finally:
		carla_env.clean_actors()
