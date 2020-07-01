import carla
import weakref

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
		self.__env = env
		self.__world = env.get_world()
		self.__sensor = None
		self.__bp_library = self.__world.get_blueprint_library()
		self.__cam_bp = self.__bp_library.find(SENSOR_LIST[sensor_id]['type'])
		self.__sensor_location_x = SENSOR_LIST[sensor_id]['x']
		self.__sensor_location_y = SENSOR_LIST[sensor_id]['y']
		self.__sensor_location_z = SENSOR_LIST[sensor_id]['z']
		self.__sensor_id = SENSOR_LIST[sensor_id]['id']

	def attach_to_vehicle(self, attach_vehicle):
		spawn_point = carla.Transform()
		self.__sensor = self.__world.spawn_actor(self.__cam_bp, spawn_point, attach_to = attach_vehicle)
		weak_self = weakref.ref(self)
		self.__sensor.listen(lambda data: self._on_event(weak_self, data))

	# pure virtual function, we must rewrite this function
	@staticmethod
	def _on_event(weak_self, event):
 		pass


class CollisionSensor(Sensor):
	def __init__(self, env):
		super().__init__(env, 5)
		self.__collision_time = 0

	@staticmethod
	def _on_event(weak_self, event):
		self = weak_self()
		if not self:
			return
		actor_type = get_actor_display_name(event.other_actor)
		self.__collision_time += 1
		print("Collision with ", actor_type)

		