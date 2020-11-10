#SET FOREIGN_KEY_CHECKS = 0;

#SET FOREIGN_KEY_CHECKS = 1;

# Dump of table leading_vehicle_scenario
# ------------------------------------------------------------


DROP TABLE IF EXISTS `LeadingVehicle`;

CREATE TABLE `LeadingVehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testing_record_id` int(11) NOT NULL,
  `testing_scenario_id` int(11) NOT NULL,
  `close_times` int(3) NOT NULL COMMENT 'danger distance with the leading vehicle',
  `is_arrive` bool NOT NULL COMMENT 'destination reached',  
  `collision_times` int(3) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`testing_record_id`) REFERENCES testing_record(id),
  FOREIGN KEY (`testing_scenario_id`) REFERENCES testing_scenario(id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table object_detection_scenario
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ObjectDetection`;

CREATE TABLE `ObjectDetection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testing_record_id` int(11) NOT NULL,
  `testing_scenario_id` int(11) NOT NULL,
  `accuracy` int(3) NOT NULL,
  `avg_time` int(3) NOT NULL,
  `detects` varchar(200) NOT NULL,
  `answers` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`testing_record_id`) REFERENCES testing_record(id),
  FOREIGN KEY (`testing_scenario_id`) REFERENCES testing_scenario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




# Dump of table testing_record
# ------------------------------------------------------------

DROP TABLE IF EXISTS `testing_record`;

CREATE TABLE `testing_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testing_scenario_id` int(11) NOT NULL,
  `weather_id` int(11) NOT NULL,
  `mark` int(3) NOT NULL,
  `agent_name` varchar(11) NOT NULL DEFAULT '',
  `agent_path` varchar(100) NOT NULL DEFAULT '',
  `time_stamp` int NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`weather_id`) REFERENCES weather(id),
  FOREIGN KEY (`testing_scenario_id`) REFERENCES testing_scenario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




# Dump of table testing_scenario
# ------------------------------------------------------------

DROP TABLE IF EXISTS `testing_scenario`;

CREATE TABLE `testing_scenario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL DEFAULT '' COMMENT '名称',
  PRIMARY KEY (`id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





# Dump of table traffic_light_scenario
# ------------------------------------------------------------



DROP TABLE IF EXISTS `TrafficLightDetection`;
CREATE TABLE `TrafficLightDetection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testing_record_id` int(11) NOT NULL,
  `testing_scenario_id` int(11) NOT NULL,
  `accuracy` int(3) NOT NULL,
  `avg_time` int(3) NOT NULL,
  `detects` varchar(200) NOT NULL,
  `answers` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`testing_record_id`) REFERENCES testing_record(id),
  FOREIGN KEY (`testing_scenario_id`) REFERENCES testing_scenario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




# Dump of table turning_obstacle_scenario
# ------------------------------------------------------------


DROP TABLE IF EXISTS `TurningObstacle`;
CREATE TABLE `TurningObstacle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testing_record_id` int(11) NOT NULL,
  `testing_scenario_id` int(11) NOT NULL,
  `close_times` int(3) NOT NULL COMMENT 'danger distance with the obstacle',
  `is_arrive` bool NOT NULL COMMENT 'destination reached',  
  `collision_times` int(3) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`testing_record_id`) REFERENCES testing_record(id),
  FOREIGN KEY (`testing_scenario_id`) REFERENCES testing_scenario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Dump of table blind_point_scenario
# ------------------------------------------------------------


DROP TABLE IF EXISTS `BlindPoint`;
CREATE TABLE `BlindPoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testing_record_id` int(11) NOT NULL,
  `testing_scenario_id` int(11) NOT NULL,
  `close_times` int(3) NOT NULL COMMENT 'danger distance with the leading vehicle',
  `is_arrive` bool NOT NULL COMMENT 'destination reached',  
  `collision_times` int(3) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`testing_record_id`) REFERENCES testing_record(id),
  FOREIGN KEY (`testing_scenario_id`) REFERENCES testing_scenario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table weather
# ------------------------------------------------------------

DROP TABLE IF EXISTS `weather`;



CREATE TABLE `weather` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clouds` int(3) NOT NULL,
  `rain` int(3) NOT NULL,  
  `puddles` int(3) NOT NULL,
  `wind` int(3) NOT NULL,
  `fog` int(3) NOT NULL,  
  `wetness` int(3) NOT NULL,
  `azimuth` int(3) NOT NULL,  
  `altitude` int(3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



INSERT INTO `testing_scenario` (`id`, `name`)
VALUES
	(1,'Blind Point'),
	(2,'Leading Vehicle'),
	(3,'Object Detection'),
	(4,'Traffic Light Detection'),
	(5,'Turning Obstacle')