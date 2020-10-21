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
		raise Exception("The detect agent don't have set_destination function")

	def run_step(self, input_data = {}, debug = False):
		raise Exception("The detect agent don't have run step function")

	def done(self):
		print("done!!")
		pass

	def detect(self, input_data):
		'''
		please put all your answer in the "detect_result" list

		In traffic light detect scenario, the possible answers are: Green, Yellow, Red
		
		In object detect scenario, the possible answers are: car, truck, bus, motorbike, bicycle, pedestrian
		The order of your results in the list should follow the order of the entities in the image from left to right
		'''
		# detect_result = ['car']
		detect_result = ['Red']
		front_camera = input_data['Center']['data']
		# print(front_camera)
		'''
		please implement or call your object-detect function here
		'''
		return detect_result
