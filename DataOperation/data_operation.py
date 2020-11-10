import mysql.connector
import mysql
import sys

'''
args = sys.argv
print(args)
'''

def connect_database():
    global mydb
    try:
        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="root",
                                       database="992_database")
    except Exception as e:
        raise Exception("The database connection is not succeed, please have a check!")

    # print("Database Connection Successful")

    global mycursor
    mycursor = mydb.cursor()


def disconnect_db():
    mycursor.close()
    mydb.close()

blind_point_dataframe = {'clouds': 60,
                         'rain': 0.0,
                         'puddles': 0.0,
                         'wind': 100,
                         'fog': 0.0,
                         'wetness': 0.0,
                         'azimuth': 0.0,
                         'altitude': 90,
                         'time_stamp': 1603265236.0993092,
                         'date_time': '2020-10-21 15:27:16',
                         'mark': 70,
                         'agent_path': 'D:/992_Project/Carla-Platform/DrivingAgent/CarlaAutoAgent.py',
                         'agent_name': 'AutoAgent',
                         'Scenario': 'Blind Point',
                         'close_times': 6,
                         'is_arrive': True,
                         'collision_times': 1}

leading_vehicle_dataframe = {'clouds': 60,
                             'rain': 0.0,
                             'puddles': 0.0,
                             'wind': 100,
                             'fog': 0.0,
                             'wetness': 0.0,
                             'azimuth': 0.0,
                             'altitude': 90,
                             'time_stamp':
                                 1603265411.999487,
                             'date_time': '2020-10-21 15:30:11',
                             'mark': 60,
                             'agent_path': 'D:/992_Project/Carla-Platform/DrivingAgent/CarlaAutoAgent.py',
                             'agent_name': 'AutoAgent',
                             'Scenario': 'Leading Vehicle',
                             'close_times': 4,
                             'is_arrive': True,
                             'collision_times': 7}

turning_dataframe = {'clouds': 60,
                     'rain': 0.0,
                     'puddles': 0.0,
                     'wind': 100,
                     'fog': 0.0,
                     'wetness': 0.0,
                     'azimuth': 0.0,
                     'altitude': 90,
                     'time_stamp': 1603265731.99693,
                     'date_time': '2020-10-21 15:35:31',
                     'mark': 80,
                     'agent_path': 'D:/992_Project/Carla-Platform/DrivingAgent/CarlaAutoAgent.py',
                     'agent_name': 'AutoAgent',
                     'Scenario': 'Turning Obstacle',
                     'close_times': 4,
                     'is_arrive': True,
                     'collision_times': 1}

object_dataframe = {'clouds': 0.0,
                    'rain': 0.0,
                    'puddles': 0.0,
                    'wind': 0.0,
                    'fog': 0.0,
                    'wetness': 0.0,
                    'azimuth': 0.0,
                    'altitude': 90,
                    'time_stamp': 1602665220.8308778,
                    'date_time': '2020-10-14 16:47:00',
                    'agent_path': 'D:/992_Project/Carla-Platform/DrivingAgent/DetectAgent_1.py',
                    'agent_name': 'DetectAgent',
                    'Location': None,
                    'mark': 19.44,
                    'Scenario': 'Object Detection',
                    'accuracy': 27.78,
                    'avg_time': 2.61,
                    'detects': 'bus;pedestrian;|bus;|car;car;pedestrian;|car;car;motorbike;|pedestrian;car;pedestrian;|pedestrian;pedestrian;pedestrian;|',
                    'answers': 'pedestrian;bus;pedestrian;|bus;pedestrian;pedestrian;|car;bus;bicycle;|bus;car;bicycle;|bicycle;car;bicycle;|pedestrian;bicycle;motorbike;|', }

traffic_dataframe = {'clouds': 0.0,
                     'rain': 0.0,
                     'puddles': 0.0,
                     'wind': 0.0,
                     'fog': 0.0,
                     'wetness': 0.0,
                     'azimuth': 0.0,
                     'altitude': 90,
                     'time_stamp': 1602665556.0630894,
                     'date_time': '2020-10-14 16:52:36',
                     'agent_path': 'D:/992_Project/Carla-Platform/DrivingAgent/DetectAgent_1.py',
                     'agent_name': 'DetectAgent',
                     'mark': 70.0,
                     'Location': None,
                     'Scenario': 'Traffic Light Detection',
                     'accuracy': 100.0,
                     'avg_time': 2.77,
                     'detects': 'Red;|Red;|Red;|Yellow;|Yellow;|Yellow;|Green;|Green;|Green;|Green;|',
                     'answers': 'Red;|Red;|Red;|Yellow;|Yellow;|Yellow;|Green;|Green;|Green;|Green;|', }


def insert_weather(data_frame):
    sql = "INSERT INTO weather(clouds,rain,puddles,wind,fog,wetness,azimuth,altitude) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    name = [(data_frame['clouds'], data_frame['rain'], data_frame['puddles'], data_frame['wind'], data_frame['fog'],
             data_frame['wetness'], data_frame['azimuth'], data_frame['altitude'])]
    mycursor.executemany(sql, name)
    sqlform = "SELECT * from weather order by id desc limit 1"
    mycursor.execute(sqlform)

    # mydb.commit()
    records = mycursor.fetchall()
    return records[0][0]


def choose_scenario(data_frame):
    scenario_name = data_frame['Scenario']
    sql = f"SELECT id from testing_scenario where name='{scenario_name}'"
    sql.format_map(vars())
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return records[0][0]


def insert_new_record(data_frame):
    sql = "INSERT INTO testing_record(testing_scenario_id, weather_id, mark, agent_name, agent_path, time_stamp, " \
          "date_time) values(%s, %s, %s, %s, %s, %s, %s) "
    name = [(choose_scenario(data_frame), insert_weather(data_frame), data_frame['mark'], data_frame['agent_name'],
             data_frame['agent_path'], data_frame['time_stamp'], data_frame['date_time']
             )]
    mycursor.executemany(sql, name)
    sql2 = "SELECT * from testing_record order by id desc limit 1"
    mycursor.execute(sql2)
    records3 = mycursor.fetchall()
    return records3[0][0]


def insert_scenario_param(data_frame):
    table_name = data_frame['Scenario']
    table_name = table_name.lower()
    table_name = ''.join(table_name.split())

    if table_name == 'blindpoint':
        sql_1 = "INSERT INTO blindpoint(testing_record_id,close_times, is_arrive, " \
                "collision_times) values(%s, %s, %s,%s) "
        name_1 = [(insert_new_record(data_frame), data_frame['close_times'],
                   data_frame['is_arrive'],
                   data_frame['collision_times'])]
        mycursor.executemany(sql_1, name_1)
        sqlform_1 = "SELECT * from blindpoint "
        mycursor.execute(sqlform_1)
        records_1 = mycursor.fetchall()

    if table_name == 'leadingvehicle':
        sql_2 = "INSERT INTO leadingvehicle(testing_record_id,close_times, is_arrive, " \
                "collision_times) values(%s, %s, %s, %s) "
        name_2 = [(insert_new_record(data_frame), data_frame['close_times'],
                   data_frame['is_arrive'],
                   data_frame['collision_times'])]
        mycursor.executemany(sql_2, name_2)
        sqlform_2 = "SELECT * from leadingvehicle order by id desc limit 1"
        mycursor.execute(sqlform_2)
        records_2 = mycursor.fetchall()

    if table_name == 'turningobstacle':
        sql_3 = "INSERT INTO turningobstacle(testing_record_id,close_times, is_arrive, " \
                "collision_times) values(%s, %s, %s, %s) "
        name_3 = [(insert_new_record(data_frame), data_frame['close_times'],
                   data_frame['is_arrive'],
                   data_frame['collision_times'])]
        mycursor.executemany(sql_3, name_3)
        sqlform_3 = "SELECT * from turningobstacle order by id desc limit 1"
        mycursor.execute(sqlform_3)
        records_3 = mycursor.fetchall()

    if table_name == 'objectdetection':
        sql_4 = "INSERT INTO objectdetection(testing_record_id,accuracy, avg_time, " \
                "detects, answers) values(%s, %s, %s, %s, %s) "
        name_4 = [
            (insert_new_record(data_frame), data_frame['accuracy'], data_frame['avg_time'],
             data_frame['detects'], data_frame['answers'])]
        mycursor.executemany(sql_4, name_4)
        sqlform_4 = "SELECT * from objectdetection order by id desc limit 1"
        mycursor.execute(sqlform_4)
        records_4 = mycursor.fetchall()

    if table_name == 'trafficlightdetection':
        sql_5 = "INSERT INTO trafficlightdetection(testing_record_id, accuracy, avg_time, " \
                "detects, answers) values(%s, %s, %s, %s, %s) "
        name_5 = [
            (insert_new_record(data_frame), data_frame['accuracy'], data_frame['avg_time'],
             data_frame['detects'], data_frame['answers'])]
        mycursor.executemany(sql_5, name_5)
        sqlform_5 = "SELECT * from trafficlightdetection order by id desc limit 1"
        mycursor.execute(sqlform_5)
        records_5 = mycursor.fetchall()


def get_record_list(page_num, load_num):
    connect_database()
    sql = "select count(*) from testing_record"
    mycursor.execute(sql)
    total_count = mycursor.fetchall()
    total_page = (total_count[0][0] + load_num - 1) / load_num
    if page_num > total_page:
        raise Exception("The load_num input is wrong. Maybe you pass a error page number.")
    start_num = (page_num - 1) * load_num
    sql2 = f"select * from testing_record ORDER BY id DESC limit {start_num},{load_num} "
    sql2.format_map(vars())
    mycursor.execute(sql2)
    result = mycursor.fetchall()
    disconnect_db()
    return result


def get_detailed_list(record_id):
    connect_database()
    sql = f"SELECT testing_scenario.name FROM testing_record " \
          f"left join weather on testing_record.weather_id = weather.id " \
          f"left join testing_scenario on testing_record.testing_scenario_id = testing_scenario.id where " \
          f"testing_record.id = {record_id} "
    sql.format_map(vars())
    mycursor.execute(sql)
    name = mycursor.fetchall()
    table_name = name[0][0]
    table_name = table_name.lower()
    table_name = ''.join(table_name.split())
    sql2 = f"SELECT * FROM testing_record " \
           f"left join weather on testing_record.weather_id = weather.id " \
           f"left join testing_scenario on testing_record.testing_scenario_id = testing_scenario.id " \
           f"left join {table_name} on testing_record.id = {table_name}.testing_record_id where " \
           f"testing_record.id = {record_id} "
    sql2.format_map(vars())
    mycursor.execute(sql2)
    result = mycursor.fetchall()
    # print(result)
    disconnect_db()
    return result


def insert(data_frame):
    connect_database()
    insert_scenario_param(data_frame)
    mydb.commit()
    disconnect_db()


if __name__ == '__main__':
    connect_database()
    insert(object_dataframe)
    # get_record_list(int(args[1]), int(args[2]))
    # get_detailed_list(int(args[3]))
    mycursor.close()
    mydb.close()
