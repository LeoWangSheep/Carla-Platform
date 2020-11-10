'''
from ...  .Mainloop import main_loop
'''
# import MainLoop


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
                     custom_cloud,
                     scenario,
                     agent_name
                     ):
    if if_custom == 'false':
        if_custom = False
    else:
        if_custom = True

    data_frame_dict = {'agent_path': agent_path, 'if_custom': if_custom, 'preset_time': preset_time,
                       'preset_weather': preset_weather, 'custom_time': int(custom_time), 'custom_rainfall': int(custom_rainfall),
                       'custom_ground_humidity': int(custom_ground_humidity), 'custom_wind': int(custom_wind),
                       'custom_fog': int(custom_fog), 'custom_air_humidity': int(custom_air_humidity), 'custom_cloud': int(custom_cloud),
                       'scenario': scenario, 'agent_name': agent_name}

    return data_frame_dict


if __name__ == '__main__':
    message_1 = DictConstruction(agent_path='D:/992_Project/Carla-Platform/DrivingAgent/CarlaAutoAgent.py',
                                 if_custom=False,
                                 preset_time='Noon',  # possible value: Noon, Sunset, Night, Sunrise
                                 preset_weather='Clear',  # possible value: Clear, Rainy, Fog, Wind
                                 custom_time=None,
                                 custom_rainfall=None,
                                 custom_ground_humidity=None,
                                 custom_wind=None,
                                 custom_fog=None,
                                 custom_air_humidity=None,
                                 custom_cloud=None,
                                 scenario='TurningObstacle',
                                 # possible value : TrafficLight, ObjectDetect, LeadingVehicle,
                                 # 				   TurningObstacle, BlindPoint
                                 agent_name='AutoAgent'
                                 )

    message_2 = DictConstruction(agent_path='D:/992_Project/Carla-Platform/DrivingAgent/DetectAgent_1.py',
                                 if_custom=False,
                                 preset_time='Sunset',  # possible value: Noon, Sunset, Night, Sunrise
                                 preset_weather='Rainy',  # possible value: Clear, Rainy, Fog, Wind
                                 custom_time=None,
                                 custom_rainfall=None,
                                 custom_ground_humidity=None,
                                 custom_wind=None,
                                 custom_fog=None,
                                 custom_air_humidity=None,
                                 custom_cloud=None,
                                 scenario='ObjectDetect',
                                 # possible value : TrafficLight, ObjectDetect, LeadingVehicle,
                                 # 				   TurningObstacle, BlindPoint
                                 agent_name='DetectAgent'
                                 )

    # MainLoop.main_loop(message_1)
