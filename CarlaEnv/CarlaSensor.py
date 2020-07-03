import weakref
import numpy as np
import cv2
import carla


def parse_img(image, img_height, img_width, sensor_type):
	i = np.array(image.raw_data)
	i2 = i.reshape((img_height, img_width, 4))
	i3 = i2[:, :, :3]
	cv2.imshow(sensor_type + " Camera", i3)
	cv2.waitKey(1)
	return i3/255.0

SENSOR_LIST = [
			{'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 300, 'height': 200, 'fov': 100, 'id': 'Center'},

            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
             'yaw': -45.0, 'width': 300, 'height': 200, 'fov': 100, 'id': 'Left'},

            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 45.0,
             'width': 300, 'height': 200, 'fov': 100, 'id': 'Right'},

            {'type': 'sensor.camera.rgb', 'x': -1.8, 'y': 0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
             'yaw': 180.0, 'width': 300, 'height': 200, 'fov': 130, 'id': 'Rear'},

            {'type': 'sensor.other.gnss', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'GPS'},

            {'type' : 'sensor.other.collision', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'Collision'},

            {'type' : 'sensor.other.lane_invasion', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'LaneInvasion'}
           
           ]

def get_actor_display_name(actor, truncate=250):
	name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
	return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

class Sensor(object):
	def __init__(self, env, sensor_id):
		self._env = env
		self._world = env.get_world()
		self._sensor = None
		self._bp_library = self._world.get_blueprint_library()
		self._cam_bp = self._bp_library.find(SENSOR_LIST[sensor_id]['type'])
		self._sensor_id = SENSOR_LIST[sensor_id]['id']
		self._spawn_point = carla.Transform()

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


class CollisionSensor(Sensor):
	def __init__(self, env):
		sensor_id = 5
		super().__init__(env, sensor_id)
		self.__collision_time = 0

	@staticmethod
	def _on_event(weak_self, event):
		self = weak_self()
		if not self:
			return
		actor_type = get_actor_display_name(event.other_actor)
		self.__collision_time += 1
		# print("Collision with ", actor_type)

class GnssSensor(Sensor):
	def __init__(self, env):
		sensor_id = 4
		super().__init__(env, sensor_id)
		self.__sensor_location_x = SENSOR_LIST[sensor_id]['x']
		self.__sensor_location_y = SENSOR_LIST[sensor_id]['y']
		self.__sensor_location_z = SENSOR_LIST[sensor_id]['z']
		self.__spawn_point = carla.Transform(carla.Location( x = self.__sensor_location_x, \
		 													 y = self.__sensor_location_y, \
		 													 z = self.__sensor_location_z))
		self.__lat = 0.0
		self.__lon = 0.0

	@staticmethod
	def _on_event(weak_self, event):
		self = weak_self()
		if not self:
			return
		self.lat = event.latitude
		self.lon = event.longitude
		# print("latitude: ", self.lat, "longitude: ", self.lon)

class RGBCamera(Sensor):
	def __init__(self, env, sensor_id):
		super().__init__(env, sensor_id)
		self._sensor_location_x = SENSOR_LIST[sensor_id]['x']
		self._sensor_location_y = SENSOR_LIST[sensor_id]['y']
		self._sensor_location_z = SENSOR_LIST[sensor_id]['z']
		self._roll = SENSOR_LIST[sensor_id]['roll']
		self._pitch = SENSOR_LIST[sensor_id]['pitch']
		self._yaw = SENSOR_LIST[sensor_id]['yaw']
		self._sensor_type = SENSOR_LIST[sensor_id]['id']
		self._img_width = SENSOR_LIST[sensor_id]['width']
		self._img_height = SENSOR_LIST[sensor_id]['height']
		self._img_fov = SENSOR_LIST[sensor_id]['fov']
		self._spawn_point = carla.Transform(carla.Location( x = self._sensor_location_x, \
		 													 y = self._sensor_location_y, \
		 													 z = self._sensor_location_z), 
							 				 carla.Rotation( pitch = self._pitch, \
							 				 				 yaw = self._yaw, \
							 				 				 roll = self._roll))
		self._cam_bp.set_attribute("image_size_x", f"{self._img_width}")
		self._cam_bp.set_attribute("image_size_y", f"{self._img_height}")
		self._cam_bp.set_attribute("fov", f"{self._img_fov}")
		self._cam_bp.set_attribute('sensor_tick', '0.2')

	def attach_to_vehicle(self, attach_vehicle):
		# print(self._spawn_point)
		self._sensor = self._world.spawn_actor(self._cam_bp, self._spawn_point, attach_to = attach_vehicle)
		self._env.add_actor(self._sensor)
		weak_self = weakref.ref(self)

		self._sensor.listen(lambda image: self._parse_img(weak_self, image))
	
	@staticmethod
	def _parse_img(weak_self, image):
		self = weak_self()
		if not self:
			return
		i = np.array(image.raw_data)
		i2 = i.reshape((self._img_height, self._img_width, 4))
		i3 = i2[:, :, :3]
		cv2.imshow(self._sensor_type + " Camera", i3)
		cv2.waitKey(1)
		return i3/255.0
