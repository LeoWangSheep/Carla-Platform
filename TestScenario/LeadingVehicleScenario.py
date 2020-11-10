import time
import random
from threading import Thread, Lock
from TestScenario.BaseScenario import Scenario
from TestScenario.DrivingScenario import DrivingScenario

import carla

l_v_position = [{'start': {'x': 165, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1},
                 'destination': {'x': -45, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1},
                 'description': "The leading vehicle drive slowly",
                 'enemy_vehicle': {'start': {'x': 155, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1},
                                   'mode': 'Slow'},
                 },

                {'start': {'x': 165, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1},
                 'destination': {'x': -45, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1},
                 'description': "The leading vehicle drive stop suddenly",
                 'enemy_vehicle': {'start': {'x': 155, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1},
                                   'mode': 'Stop'},
                 }
                 ]


l_v_destination = [{'x': -45, 'y': 196, 'z': 3, 'pitch': 0, 'yaw': 180, 'roll': 0, 'id': 1}]

actor_blueprint_categories = {
    'car1': 'vehicle.tesla.model3',
    'car2': 'vehicle.audi.a2'
}


class LeadingVehicleScenario(DrivingScenario):
    def __init__(self, weather=None):
        super().__init__(3, weather)
        self.info_dataframe['Scenario'] = 'Leading Vehicle'

    def set_up_scenario_start(self, agent):
        init_position = l_v_position[0]['start']
        # setting up ego vehicle
        super().set_up_scenario_start(agent, init_position)
        try:
            self._agent.bind_vehicle(self._physical_vehicle, target_speed=40)
        except Exception as e:
            self._scenario_done = True
            raise Exception(str(e))
        time.sleep(1)

    def run_scenario(self):
        for position in l_v_position:
            if self._scenario_done:
                break
            self.change_next_position(position, 0)
            self._level_done = False
            # run the detect thread
            self.run_instance(position)
        self._scenario_done = True
        self.record_score()

    def change_next_position(self, position, mode):
        if position is None:
            return
        print("Scenario: ", position['description'])
        super().change_next_position(position['start'], mode)
        enemy_vehicle_map = position['enemy_vehicle']
        if enemy_vehicle_map is None or enemy_vehicle_map['start'] is None:
            self._enemy_vehicle = None
            self._enemy_mode = ""
            return
        enemy_position = enemy_vehicle_map['start']
        enemy_vehicle_location = carla.Location(x=enemy_position['x'], y=enemy_position['y'], z=enemy_position['z'])
        enemy_vehicle_rotation = carla.Rotation(pitch=enemy_position['pitch'], yaw=enemy_position['yaw'],
                                                roll=enemy_position['roll'])
        self._leading_vehicle = Scenario._carla_env.spawn_new_actor(actor_blueprint_categories['car2'],
                                                                    enemy_vehicle_location, enemy_vehicle_rotation,
                                                                    False)

        if self._leading_vehicle is None:
            print("Error Spawn Position")
            return
        self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, hand_brake=True))
        self._enemy_mode = enemy_vehicle_map['mode']
        time.sleep(2)

    def run_instance(self, position):
        follow_thread = Thread(target=self.follow_ego_vehicle, args=(position['start']['yaw'],))
        leading_driving_thread = Thread(target=self.leading_driving, args=(position['enemy_vehicle']['mode'],))
        ego_driving_thread = Thread(target=self.ego_driving, args=(position['destination'],))

        self.start_thread(follow_thread)
        self.start_thread(leading_driving_thread)
        self.start_thread(ego_driving_thread)

        leading_driving_thread.join()
        ego_driving_thread.join()
        follow_thread.join()
        time.sleep(2)

    def leading_driving(self, control):
        print("Leading Vehicle Driving...")
        while True:
            if self._scenario_done:
                break
            if self._level_done:
                break
            leading_v = self._leading_vehicle.get_location().x
            ego_v = self._physical_vehicle.get_location().x
            distance = abs(leading_v - ego_v)
            if control == 'Stop':
                if distance > 14:
                    self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0, steer=0.0))
                    time.sleep(6)
                elif distance <= 14:
                    self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.8, steer=0.0))
            elif control == 'Slow':
                self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))
            elif control == 'Normal':
                self._leading_vehicle.apply_control(carla.VehicleControl(throttle=0.8, steer=0.0))

        self._leading_vehicle.destroy()
        self._leading_vehicle = None

        '''
    def scenario_end(self):
        self._leading_vehicle.destroy()
        super().scenario_end()
        '''
