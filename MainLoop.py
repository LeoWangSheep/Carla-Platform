import time

from EnvironmentSetting import CarlaEnvironment
from EgoVehicle import EgoVehicle
import CarlaSensor
def main_loop():
	try:
		carla_env = CarlaEnvironment()
		my_ego_vehicle = EgoVehicle(carla_env)

		my_ego_vehicle.set_start_waypoint( _x = 25, _y = 4, _z = 1,\
									  _pitch = 0, _yaw = -13.668415, _roll = 0)
		my_ego_vehicle.set_end_waypoint( _x = 50, _y = 4, _z = 1,\
									  _pitch = 0, _yaw = -13.668415, _roll = 0)
		my_ego_vehicle.vehicle_initial()
		my_ego_vehicle.follow_ego()

		carla_env.spawn_stop_vehicle( x = 50, y = 4, z = 1,\
									  pitch = 0, yaw = -13.668415, roll = 0)

		my_collison_sensor = CarlaSensor.CollisionSensor(carla_env)
		my_collison_sensor.attach_to_vehicle(my_ego_vehicle.get_vehicle())

		my_ego_vehicle.drive()
	except Exception as e:
		print("Error Occur :", e)
	finally:
		carla_env.clean_actors()


if __name__ == '__main__':
	main_loop()