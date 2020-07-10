import carla
import time
from CarlaEnv.EgoVehicle import EgoVehicle

class CarlaEnvironment(object):
	def __init__(self, town_id = 3,  _host = 'localhost', _port = 2000, _expired_time = 90.0):
		self.__client = carla.Client(_host, _port)
		self.__client.set_timeout(_expired_time)
		town_str = 'Town0' + str(town_id)
		self.__world = self.__client.get_world()
		# self.__world = self.__client.load_world(town_str)
		self.__blueprint_library = self.__world.get_blueprint_library()
		self.__actor_list = []
		

	def add_actor(self, _actor):
		self.__actor_list.append(_actor)

	def get_world(self):
		return self.__world

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
		spectator = self.__world.get_spectator()
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
		self.__client.load_world(town_str)

if __name__ == '__main__':
	try:
		carla_env = CarlaEnvironment()
	except Exception as e:
		print("Error Occur :", e)
	finally:
		carla_env.clean_actors()