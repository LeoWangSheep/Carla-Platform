from CommonTool.agents.navigation.basic_agent import BasicAgent
from DrivingAgent.Agent import Agent


# agent adapter
class AutoAgent(Agent):
	def __init__(self, vehicle, target_speed=20):
		self._agent = BasicAgent(vehicle, target_speed)

	def initial_sensor(self):
		sensors = [
			{'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
 			'width': 640, 'height': 480, 'fov': 110, 'id': 'Center'}

 			# {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
			# 'yaw': -45.0, 'width': 300, 'height': 200, 'fov': 100, 'id': 'Left'},

			# {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 45.0,
			# 'width': 300, 'height': 200, 'fov': 100, 'id': 'Right'},

			# {'type': 'sensor.camera.rgb', 'x': -1.8, 'y': 0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
			# 	'yaw': 180.0, 'width': 300, 'height': 200, 'fov': 130, 'id': 'Rear'},

			# {'type': 'sensor.lidar.ray_cast', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0,
			#	'id': 'LIDAR'},

			# {'type': 'sensor.other.gnss', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'GPS'},

			# {'type' : 'sensor.other.collision', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'Collision'},

			# {'type' : 'sensor.other.lane_invasion', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'LaneInvasion'}
           
		]

		return sensors 

	def set_destination(self, target_waypoint):
		self._agent.set_destination(target_waypoint)

	def run_step(self, input_data = {}, debug = False):
		control = self._agent.run_step(debug)
		return control

	def done(self):
		return self._agent.done()

