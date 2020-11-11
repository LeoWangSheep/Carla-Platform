from DrivingAgent.Agent import Agent
from DrivingAgent.Detect.ColorDetect_v2 import yolo_detect
import cv2


# agent adapter


class DetectAgent(Agent):
    def __init__(self, vehicle=None, target_speed=20):
        self._agent = None

    def initial_sensor(self):
        sensors = [
            {'type': 'sensor.camera.rgb', 'x': 8, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 1024, 'height': 768, 'fov': 110, 'id': 'Center'}
        ]
        # Recommend Resolution:[800*600] [1024*768] [1280*1024] [1440*900] [1680*1050] [1980*1080]
        return sensors

    def set_destination(self, target_waypoint):
        raise Exception("The detect agent don't have set_destination function")

    def run_step(self, input_data={}, debug=False):
        raise Exception("The detect agent don't have run step function")

    def done(self):
        pass

    def detect(self, input_data):
        '''
		please put all your answer in the "detect_result" list

		In traffic light detect scenario, the possible answers are: Green, Yellow, Red
		
		In object detect scenario, the possible answers are: car, truck, bus, motorbike, bicycle, pedestrian
		The order of your results in the list should follow the order of the entities in the image from left to right
		'''
        # print('------------------------')
        # detect_result = ['car']
        front_camera = input_data['Center']['data']

        detect_mode = "light"
        # detect_mode = "Obj"
        detect_result = yolo_detect(front_camera, detect_mode=detect_mode)

        '''
   	 	confidence_thre：0-1，confidence（probability/mark)threshold，retain vaule greater than this value
    	nms_thre：Threshold for non-maximum suppression
    	jpg_quality：Output image quality，greater value represent better quality
    	'''

        return detect_result
