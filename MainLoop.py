import time

from EnvironmentSetting import CarlaEnvironment
from EgoVehicle import EgoVehicle



def main_loop():
	try:
		carla_env = CarlaEnvironment()
		my_ego_vehicle = EgoVehicle(carla_env)

		my_ego_vehicle.set_start_waypoint( _x = 25, _y = 8, _z = 1,\
									  _pitch = 0, _yaw = 0, _roll = 0)
		my_ego_vehicle.set_end_waypoint( _x = 50, _y = 4, _z = 1,\
									  _pitch = 0, _yaw = 0, _roll = 0)
		my_ego_vehicle.vehicle_initial()
		my_ego_vehicle.bind_collision_sensor()
		my_ego_vehicle.bind_gnss_sensor()
		my_ego_vehicle.bind_center_camera()
		my_ego_vehicle.bind_rear_camera()
		my_ego_vehicle.bind_left_camera()
		my_ego_vehicle.bind_right_camera()
		carla_env.follow_actor(my_ego_vehicle.get_vehicle())
		'''
		carla_env.spawn_stop_vehicle( x = 50, y = 4, z = 1,\
									  pitch = 0, yaw = 0, roll = 0)
		'''
		my_ego_vehicle.drive()
	except Exception as e:
		print("Error Occur :", e)
	finally:
		carla_env.clean_actors()


if __name__ == '__main__':
	main_loop()