import weakref
import numpy as np
import cv2
import carla

def get_actor_display_name(actor, truncate=250):
	name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
	return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

class Sensor(object):
	def __init__(self, env, sensor_item, sensor_data_container):
		self._env = env
		self._world = env.get_world()
		self._sensor = None
		self._bp_library = self._world.get_blueprint_library()
		self._cam_bp = self._bp_library.find(sensor_item['type'])
		self._sensor_type = sensor_item['id']
		self._spawn_point = carla.Transform()
		self._sensor_data_container = sensor_data_container

	def attach_to_vehicle(self, attach_vehicle):
		self._sensor = self._world.spawn_actor(self._cam_bp, self._spawn_point, attach_to = attach_vehicle)
		self._env.add_actor(self._sensor)
		weak_self = weakref.ref(self)
		self._sensor.listen(lambda data: self._on_event(weak_self, data))

	def get_sensor(self):
		return self._sensor
	# pure virtual function, we must rewrite this function
	@staticmethod
	def _on_event(weak_self, event):
 		pass

	def destory(self):
		self._sensor.clean_actors()


class CollisionSensor(Sensor):
	def __init__(self, env, sensor_data_container):
		sensor_item = {'type' : 'sensor.other.collision', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'Collision'}
		super().__init__(env, sensor_item, sensor_data_container)
		self._collision_time = 0

	@staticmethod
	def _on_event(weak_self, event):
		self = weak_self()
		if not self:
			return
		actor_type = get_actor_display_name(event.other_actor)
		self._collision_time += 1
		# print("Collision with ", actor_type)

class GnssSensor(Sensor):
	def __init__(self, env, sensor_item, sensor_data_container):
		super().__init__(env, sensor_item, sensor_data_container)
		self._sensor_location = carla.Location(x=sensor_item['x'], y=sensor_item['y'],
										 z=sensor_item['z'])
		self._sensor_rotation = carla.Rotation()
		self._spawn_point = carla.Transform(self._sensor_location, self._sensor_rotation)
		self._lat = 0.0
		self._lon = 0.0
	@staticmethod
	def _on_event(weak_self, gnss_data):
		self = weak_self()
		if not self:
			return
		array = np.array([gnss_data.latitude,
						  gnss_data.longitude,
						  gnss_data.altitude], dtype=np.float64)
		self._sensor_data_container.update_data(self._sensor_type, array, gnss_data.frame)
		# print("latitude: ", self.lat, "longitude: ", self.lon)

class RGBCamera(Sensor):
	def __init__(self, env, sensor_item, sensor_data_container):
		super().__init__(env, sensor_item, sensor_data_container)
		self._cam_bp.set_attribute('image_size_x', str(sensor_item['width']))
		self._cam_bp.set_attribute('image_size_y', str(sensor_item['height']))
		self._cam_bp.set_attribute('fov', str(sensor_item['fov']))
		self._sensor_location = carla.Location(x=sensor_item['x'], y=sensor_item['y'],
										 z=sensor_item['z'])
		self._sensor_rotation = carla.Rotation(pitch=sensor_item['pitch'],
										 roll=sensor_item['roll'],
										 yaw=sensor_item['yaw'])
		self._spawn_point = carla.Transform(self._sensor_location, self._sensor_rotation)
		self._recording = False

	@staticmethod
	def _on_event(weak_self, image):
		self = weak_self()
		if not self:
			return
		array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
		array = np.reshape(array, (image.height, image.width, 4))
		self._sensor_data_container.update_data(self._sensor_type, array, image.frame)
		i3 = array[:, :, :3]
		cv2.imshow(self._sensor_type + " Camera", i3)
		cv2.waitKey(1)
		if self._recording:
			image.save_to_disk('img_saved_HD/%06d.png' % image.frame)
		return i3/255.0

class LidarSensor(Sensor):
	def __init__(self, env, sensor_item, sensor_data_container):
		super().__init__(env, sensor_item, sensor_data_container)
		self._cam_bp.set_attribute('range', str(sensor_item['range']))
		self._cam_bp.set_attribute('rotation_frequency', str(sensor_item['rotation_frequency']))
		self._cam_bp.set_attribute('channels', str(sensor_item['channels']))
		self._cam_bp.set_attribute('upper_fov', str(sensor_item['upper_fov']))
		self._cam_bp.set_attribute('lower_fov', str(sensor_item['lower_fov']))
		self._cam_bp.set_attribute('points_per_second', str(sensor_item['points_per_second']))
		self._sensor_location = carla.Location(x=sensor_item['x'], y=sensor_item['y'],
										 z=sensor_item['z'])
		self._sensor_rotation = carla.Rotation(pitch=sensor_item['pitch'],
										 roll=sensor_item['roll'],
										 yaw=sensor_item['yaw'])

	@staticmethod
	def _on_event(weak_self, lidar_data):
		self = weak_self()
		if not self:
			return
		points = np.frombuffer(lidar_data.raw_data, dtype=np.dtype('f4'))
		points = np.reshape(points, (int(points.shape[0] / 3), 3))
		self._sensor_data_container.update_data(self._sensor_type, points, lidar_data.frame)

class SensorList():
	def __init__(self, env, agent):
		self._env = env
		self._agent = agent
		self._sensor_list = []
		self._sensor_data = SensorDataContainer()

	def setup_sensor(self, attach_vehicle):
		init_sensor_map = self._agent.initial_sensor()
		this_sensor = None
		for sensor_item in init_sensor_map:
			should_attach = False
			if sensor_item['type'].startswith('sensor.camera'):
				# set up physical camera sensor
				this_sensor = RGBCamera(self._env, sensor_item, self._sensor_data)
				should_attach = True
			elif sensor_item['type'].startswith('sensor.lidar'):
				# set up lidar sensor
				this_sensor = LidarSensor(self._env, sensor_item, self._sensor_data)
				should_attach = True
			elif sensor_item['type'].startswith('sensor.other.gnss'):
				# set up gnss sensor
				this_sensor = GnssSensor(self._env, sensor_item, self._sensor_data)
				should_attach = True
			if should_attach:
				self._sensor_data.add_sensor(sensor_item)
				this_sensor.attach_to_vehicle(attach_vehicle)
				self._sensor_list.append(this_sensor)

	def get_data(self):
		return self._sensor_data.get_data()

	def destroy_sensors(self):
		for sensor_obj in self._sensor_list:
			sensor_obj.destory()

class SensorDataContainer:
	def __init__(self):
		self._sensor_data = {}

	def add_sensor(self, sensor_item):
		self._sensor_data[sensor_item['id']] = {}
		self._sensor_data[sensor_item['id']]['sensor'] = sensor_item
		self._sensor_data[sensor_item['id']]['data'] = None
		self._sensor_data[sensor_item['id']]['timestamp'] = -1

	def update_data(self, id, data, timestamp):
		self._sensor_data[id]['data'] = data
		self._sensor_data[id]['timestamp'] = timestamp

	def get_data(self):
		return self._sensor_data




