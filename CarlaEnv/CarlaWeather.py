import carla

class Weather:
	carla_weather = None
	clouds = 0.0
	rain = 0.0
	puddles = 0.0
	wind = 0.0
	fog = 0.0
	wetness = 0.0
	azimuth = 0.0
	altitude = 0.0
	def __init__(self, mode = None, weather_arguments = None):
		if mode != None:
			if "time_str" in mode.keys():
				Weather.set_time_frame(mode["time_str"])
			if "weather" in mode.keys():
				Weather.set_weather_scenario(mode["weather"])
		if weather_arguments != None:
			pass

	@staticmethod
	def set_time_frame(time_str):
		if time_str == "Noon":
			Weather.altitude = 90
		elif time_str == "Sunset":
			Weather.altitude = 0
		elif time_str == "Night":
			Weather.altitude = -90
		elif time_str == "Sunrise":
			Weather.altitude = 180

	@staticmethod
	def set_weather_scenario(weather_str):
		if weather_str == "Rainy":
			Weather.rainy_day()


	@staticmethod
	def rainy_day():
		Weather.clouds = 100
		Weather.wind = 50
		Weather.rain = 80.0
		Weather.wetness = 50
		Weather.puddles = 50


