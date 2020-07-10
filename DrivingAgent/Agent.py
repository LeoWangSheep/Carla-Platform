

class Agent(object):
	def __init__(self, vehicle, target_speed = 20):
		raise NotImplementedError(
			"The user-defined agent's constructor function should be implemented")

	def set_destination(self, target_waypoint):
		raise NotImplementedError(
			"The user-defined agent's set_destination function should be implemented")

	def initial_sensor(self):
		raise NotImplementedError(
			"The user-defined agent's initial_sensor function should be implemented")

	def run_step(self, input_data = {}, debug = False):
		raise NotImplementedError(
			"The user-defined agent's run_step function should be implemented")

	def done(self):
		raise NotImplementedError(
			"The user-defined agent's done function should be implemented")
