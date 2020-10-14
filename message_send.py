'''
from ...  .Mainloop import main_loop
'''
import MainLoop


def DictConstruction(agent_path,
                     if_custom,  # True->Custom
                     preset_time,
                     preset_weather,
                     custom_time,
                     custom_rainfall,
                     custom_ground_humidity,
                     custom_wind,
                     custom_fog,
                     custom_air_humidity,
                     scenario,
                     agent_name
                     ):
    data_frame_dict = {'agent_path': agent_path, 'if_custom': if_custom, 'preset_time': preset_time,
                       'preset_weather': preset_weather, 'custom_time': custom_time, 'custom_rainfall': custom_rainfall,
                       'custom_ground_humidity': custom_ground_humidity, 'custom_wind': custom_wind,
                       'custom_fog': custom_fog, 'custom_air_humidity': custom_air_humidity, 'scenario': scenario,
                       'agent_name': agent_name}
    # print(data_frame_dict)
    return data_frame_dict


if __name__ == '__main__':
    message_1 = DictConstruction(agent_path='D:/992_Project/Carla-Platform/DrivingAgent/CarlaAutoAgent.py',
                                 if_custom=False,
                                 preset_time='Noon',  # possible value: Noon, Sunset, Night, Sunrise
                                 preset_weather='Wind',  # possible value: Clear, Rainy, Fog, Wind
                                 custom_time=None,
                                 custom_rainfall=None,
                                 custom_ground_humidity=None,
                                 custom_wind=None,
                                 custom_fog=None,
                                 custom_air_humidity=None,
                                 scenario='LeadingVehicle',
                                 # possible value : TrafficLight, ObjectDetect, LeadingVehicle,
                                 # 				   TurningObstacle, BlindPoint
                                 agent_name='AutoAgent'
                                 )

    message_2 = DictConstruction(agent_path='D:/992_Project/Carla-Platform/DrivingAgent/DetectAgent_1.py',
                                 if_custom=False,
                                 preset_time='Noon',  # possible value: Noon, Sunset, Night, Sunrise
                                 preset_weather='Clear',  # possible value: Clear, Rainy, Fog, Wind
                                 custom_time=None,
                                 custom_rainfall=None,
                                 custom_ground_humidity=None,
                                 custom_wind=None,
                                 custom_fog=None,
                                 custom_air_humidity=None,
                                 scenario='TrafficLight',
                                 # possible value : TrafficLight, ObjectDetect, LeadingVehicle,
                                 # 				   TurningObstacle, BlindPoint
                                 agent_name='DetectAgent'
                                 )

    MainLoop.main_loop(message_2)
