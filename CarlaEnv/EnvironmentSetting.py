import carla
import time
from CarlaEnv.EgoVehicle import EgoVehicle

class CarlaEnvironment(object):
	_traffic_light_map = dict()
	_world = None
	_map = None
	_client = None
	_blueprint_library = None

	def __init__(self, town_id = 3,  _host = 'localhost', _port = 2000, _expired_time = 90.0):
		CarlaEnvironment._client = carla.Client(_host, _port)
		CarlaEnvironment._client.set_timeout(_expired_time)
		town_str = 'Town0' + str(town_id)
		CarlaEnvironment._world = CarlaEnvironment._client.get_world()
		# self.__world = self.__client.load_world(town_str)
		CarlaEnvironment._blueprint_library = CarlaEnvironment._world.get_blueprint_library()
		self.__actor_list = []
		CarlaEnvironment.prepare_map()

	def add_actor(self, _actor):
		self.__actor_list.append(_actor)

	def get_world(self):
		return CarlaEnvironment._world

	def clean_actors(self):
		for actor in self.__actor_list:	
			actor.destroy()
		print("All clearned up!")

	def spawn_stop_vehicle(self, x = 0.000000, y = 0.000000, z = 0.000000,\
		pitch = 0.000000, yaw = 0.000000, roll = 0.000000):
		stop_vehicle = EgoVehicle(self)
		stop_vehicle.set_start_waypoint( _x = x, _y = y, _z = z,\
									  _pitch = pitch, _yaw = yaw, _roll = roll)
		stop_vehicle.vehicle_initial()

	def follow_actor(self, actor):
		spectator = CarlaEnvironment._world.get_spectator()
		transform = actor.get_transform()
		spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50), \
		carla.Rotation(pitch=-90)))

	def set_traffic_light(self, vehicle, color):
		if vehicle.is_at_traffic_light():
			traffic_light = vehicle.get_traffic_light()
			if color == 0:
				traffic_light.set_state(carla.TrafficLightState.Red)
			if color == 1:
				traffic_light.set_state(carla.TrafficLightState.Yellow)
			if color == 2:
				traffic_light.set_state(carla.TrafficLightState.Green)

	def set_town(self, town_id):
		town_str = 'Town0' + str(town_id)
		print(town_str)
		CarlaEnvironment._client.load_world(town_str)

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