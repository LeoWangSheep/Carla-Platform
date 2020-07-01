import carla
import random
import time
import numpy as np
import cv2

IM_WIDTH = 640
IM_HEIGHT = 480


sensors = [{'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
            'width': 300, 'height': 200, 'fov': 100, 'id': 'Center'},

           {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
            'yaw': -45.0, 'width': 300, 'height': 200, 'fov': 100, 'id': 'Left'},

           {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 45.0,
            'width': 300, 'height': 200, 'fov': 100, 'id': 'Right'},

           {'type': 'sensor.camera.rgb', 'x': -1.8, 'y': 0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
            'yaw': 180.0, 'width': 300, 'height': 200, 'fov': 130, 'id': 'Rear'},

           {'type': 'sensor.other.gnss', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'GPS'}
           ]

def process_img(image):
	i = np.array(image.raw_data)
	i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
	i3 = i2[:, :, :3]
	#print(i3.dtype.type)
	#i3 = i3.astype(np.uint8)
	#print(i3.dtype.type)
	#print(i3)
	cv2.imshow("Vehicle Sensor Data", i3)
	cv2.waitKey(1)
	return i3/255.0


actor_list = []

try:
	client = carla.Client('localhost', 2000)
	#print(client)
	client.set_timeout(10.0)
	world = client.get_world()
	#print(client.get_available_maps())
	#world = client.load_world('Town02')
	blueprint_library = world.get_blueprint_library()
	bp = blueprint_library.filter("model3")[0]

	#spawn_point = random.choice(world.get_map().get_spawn_points())
	#print(spawn_point)
	spawn_point = carla.Transform(carla.Location(x=25.682356, y=4.024460, z=1.843102), carla.Rotation(pitch=0.000000, yaw=-13.668415, roll=0.000000))

	vehicle = world.spawn_actor(bp, spawn_point)
	
	#vehicle.set_autopilot(True)
	actor_list.append(vehicle)

	cam_bp = blueprint_library.find("sensor.camera.rgb")
	cam_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
	cam_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
	cam_bp.set_attribute("fov", f"110")
	cam_bp.set_attribute('sensor_tick', '1.0')
	spawn_point2 = carla.Transform(carla.Location(x=2.5, z=0.7))

	sensor = world.spawn_actor(cam_bp, spawn_point2, attach_to = vehicle)
	actor_list.append(sensor)

	sensor.listen(lambda data: process_img(data))

	vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0))
	time.sleep(2)
	print("go!")
	#vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
	i = 0
	tick = 0.5
	while True:
		if i > 30:
			break
		spectator = world.get_spectator()
		transform = vehicle.get_transform()
		spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50),
    carla.Rotation(pitch=-90)))
		if vehicle.is_at_traffic_light():
			traffic_light = vehicle.get_traffic_light()
			if traffic_light.get_state() == carla.TrafficLightState.Red:
				traffic_light.set_state(carla.TrafficLightState.Green)
		vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
		vehicle.set_autopilot(True)
		print(vehicle.get_location())
		#print(vehicle.transform)
		i += tick
		time.sleep(tick)
	vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0))	
	print("Done!")
finally:
	for actor in actor_list:	
		actor.destroy()
	print("All clearned up!")



