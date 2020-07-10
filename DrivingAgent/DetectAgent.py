from DrivingAgent.Agent import Agent


# agent adapter
class DetectAgent(Agent):
	def __init__(self, vehicle = None, target_speed=20):
		self._agent = None

	def initial_sensor(self):
		sensors = [
			{'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
 			'width': 640, 'height': 480, 'fov': 110, 'id': 'Center'}
		]

		return sensors 

	def set_destination(self, target_waypoint):
		pass

	def run_step(self, input_data = {}, debug = False):
		pass

	def done(self):
		return self._agent.done()

	def detect(self, input_data):
		detect_result = 'Green'
		front_camera = input_data['Center']['data']
		# data_timestamp = input_data['Center']['timestamp']
		# print(front_camera)
		'''
		please implement or call your object-detect function here
		'''
		return detect_result
