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
	def __init__(self, mode = None, weather_config = None):
		if mode != None:
			if "time_str" in mode.keys():
				# print("setting time...")
				Weather.set_time_frame(mode["time_str"])
			if "weather" in mode.keys():
				# print("setting weather...")
				Weather.set_weather_scenario(mode["weather"])
		if weather_config != None:
			# print("configure weather...")
			Weather.configure_weather(weather_config)

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
		elif weather_str == "Clear":
			Weather.clear_day()
		elif weather_str == "Fog":
			Weather.fog_day()
		elif weather_str == "Wind":
			Weather.wind_day()

	@staticmethod
	def rainy_day():
		Weather.clouds = 90
		Weather.wind = 30
		Weather.rain = 80
		Weather.wetness = 50
		Weather.puddles = 90

	@staticmethod
	def clear_day():
		Weather.clouds = 0
		Weather.wind = 0
		Weather.rain = 0
		Weather.wetness = 0
		Weather.puddles = 0
		Weather.fog = 0
	
	@staticmethod
	def fog_day():
		Weather.clouds = 60
		Weather.fog = 80

	@staticmethod
	def wind_day():
		Weather.clouds = 60
		Weather.wind = 100

	@staticmethod
	def configure_weather(weather_config):
		Weather.clouds = weather_config['clouds']
		Weather.rain = weather_config['rain']
		Weather.puddles = weather_config['puddles']
		Weather.wind = weather_config['wind']
		Weather.fog = weather_config['fog']
		Weather.wetness = weather_config['wetness']
		Weather.azimuth = weather_config['azimuth']
		Weather.altitude = weather_config['altitude']

	def get_weather_dict(self):
		weather_dict = {'clouds': round(Weather.clouds, 2), 'rain': round(Weather.rain, 2),
						'puddles': round(Weather.puddles, 2), 'wind': round(Weather.wind, 2),
						'fog': round(Weather.fog, 2), 'wetness': round(Weather.wetness, 2),
						'azimuth': round(Weather.azimuth, 2), 'altitude': round(Weather.altitude, 2)}
		return weather_dict



