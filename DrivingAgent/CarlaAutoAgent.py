from CommonTool.agents.navigation.basic_agent import BasicAgent
from DrivingAgent.Agent import Agent


# agent adapter
class AutoAgent(Agent):
	def __init__(self, vehicle, target_speed=20):
		self._agent = BasicAgent(vehicle, target_speed)

	def set_destination(self, target_waypoint):
		self._agent.set_destination(target_waypoint)

	def run_step(self, debug=False):
		return self._agent.run_step(debug)

	def done(self):
		return self._agent.done()

