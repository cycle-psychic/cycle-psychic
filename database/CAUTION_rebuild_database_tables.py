import mysql.connector


def delete():
    """
    This function will delete all existing tables in the database.

    It is designed to work with the first iteration of the database and assumes no further tables have been created, and
    the data currently in the tables are not required.
    """
    mycursor = mydb.cursor()
    drop_tables = "DROP TABLE `cyclepsychic`.`city_weather`, `cyclepsychic`.`all_station_info`, `cyclepsychic`.`station_data`, `cyclepsychic`.`station_information`;"
    mycursor.execute(drop_tables)
    print("Deletion complete.")

def recreate():
    """
    This function is designed to rebuild the initial database should a fresh start be required.

    It assumes no further changes have been made to the tables.
    """

    sqlquery = """
                CREATE TABLE IF NOT EXISTS `cyclepsychic`.`all_station_info` (
                  `address` VARCHAR(45) NULL DEFAULT NULL,
                  `contract_name` VARCHAR(45) NULL DEFAULT NULL,
                  `name` VARCHAR(45) NULL DEFAULT NULL,
                  `last_update` DATETIME NOT NULL,
                  `lng` DECIMAL(11,8) NULL DEFAULT NULL,
                  `lat` DECIMAL(10,8) NULL DEFAULT NULL,
                  `status` VARCHAR(45) NULL DEFAULT NULL,
                  `available_bikes` INT(11) NULL DEFAULT NULL,
                  `bonus` VARCHAR(45) NULL DEFAULT NULL,
                  `available_bike_stands` INT(11) NULL DEFAULT NULL,
                  `number` INT(11) NOT NULL,
                  `bike_stands` INT(11) NULL DEFAULT NULL,
                  `banking` VARCHAR(45) NULL DEFAULT NULL,
                  PRIMARY KEY (`number`, `last_update`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8mb4
                COLLATE = utf8mb4_0900_ai_ci;

                CREATE TABLE IF NOT EXISTS `cyclepsychic`.`all_station_info_test` (
                  `address` VARCHAR(45) NULL DEFAULT NULL,
                  `contract_name` VARCHAR(45) NULL DEFAULT NULL,
                  `name` VARCHAR(45) NULL DEFAULT NULL,
                  `last_update` DATETIME NOT NULL,
                  `lng` DECIMAL(11,8) NULL DEFAULT NULL,
                  `lat` DECIMAL(10,8) NULL DEFAULT NULL,
                  `status` VARCHAR(45) NULL DEFAULT NULL,
                  `available_bikes` INT(11) NULL DEFAULT NULL,
                  `bonus` VARCHAR(45) NULL DEFAULT NULL,
                  `available_bike_stands` INT(11) NULL DEFAULT NULL,
                  `number` INT(11) NOT NULL,
                  `bike_stands` INT(11) NULL DEFAULT NULL,
                  `banking` VARCHAR(45) NULL DEFAULT NULL,
                  PRIMARY KEY (`number`, `last_update`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8mb4
                COLLATE = utf8mb4_0900_ai_ci;
                
                CREATE TABLE IF NOT EXISTS `cyclepsychic`.`city_weather` (
                  `city_id` INT(11) NULL DEFAULT NULL,
                  `last_update` DATETIME NOT NULL,
                  `city_name` VARCHAR(45) NULL DEFAULT NULL,
                  `longitude` DOUBLE NULL DEFAULT NULL,
                  `latitude` DOUBLE NULL DEFAULT NULL,
                  `weather_id` INT(11) NOT NULL,
                  `weather_description` VARCHAR(45) NULL DEFAULT NULL,
                  `weather_main` VARCHAR(45) NULL DEFAULT NULL,
                  `main_temp` DOUBLE NULL DEFAULT NULL,
                  `main_pressure` DOUBLE NULL DEFAULT NULL,
                  `main_humidity` DOUBLE NULL DEFAULT NULL,
                  `main_temp_min` DOUBLE NULL DEFAULT NULL,
                  `main_temp_max` DOUBLE NULL DEFAULT NULL,
                  `main_sea_level` DOUBLE NULL DEFAULT NULL,
                  `main_wind_speed` DOUBLE NULL DEFAULT NULL,
                  `main_wind_direction` DOUBLE NULL DEFAULT NULL,
                  `main_clouds` DOUBLE NULL DEFAULT NULL,
                  `main_rain_volume_1h` DOUBLE NULL DEFAULT NULL,
                  `main_rain_volume_3h` DOUBLE NULL DEFAULT NULL,
                  `main_snow_volume_1h` DOUBLE NULL DEFAULT NULL,
                  `main_snow_volume_3h` DOUBLE NULL DEFAULT NULL,
                  `base` VARCHAR(45) NULL DEFAULT NULL,
                  `main_grnd_level` DOUBLE NULL DEFAULT NULL,
                  `sys_id` INT(11) NULL DEFAULT NULL,
                  `sys_type` INT(11) NULL DEFAULT NULL,
                  `sys_message` DOUBLE NULL DEFAULT NULL,
                  `sys_country` VARCHAR(45) NULL DEFAULT NULL,
                  `sys_sunrise` DATETIME NULL DEFAULT NULL,
                  `sys_sunset` DATETIME NULL DEFAULT NULL,
                  `cod` INT(11) NULL DEFAULT NULL,
                  `weather_icon` VARCHAR(45) NULL DEFAULT NULL,
                  PRIMARY KEY (`weather_id`, `last_update`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8mb4
                COLLATE = utf8mb4_0900_ai_ci;
                
                CREATE TABLE IF NOT EXISTS `cyclepsychic`.`city_weather_backup` (
                  `data_entry_number` INT(11) NOT NULL AUTO_INCREMENT,
                  `city_id` INT(11) NULL DEFAULT NULL,
                  `last_update` DATETIME NULL DEFAULT NULL,
                  `city_name` VARCHAR(45) NULL DEFAULT NULL,
                  `longitude` DECIMAL(9,6) NULL DEFAULT NULL,
                  `latitude` DECIMAL(9,6) NULL DEFAULT NULL,
                  `weather_id` INT(11) NULL DEFAULT NULL,
                  `weather_description` VARCHAR(45) NULL DEFAULT NULL,
                  `weather_main` VARCHAR(45) NULL DEFAULT NULL,
                  `main_temp` FLOAT NULL DEFAULT NULL,
                  `main_pressure` FLOAT NULL DEFAULT NULL,
                  `main_humidity` FLOAT NULL DEFAULT NULL,
                  `main_temp_min` FLOAT NULL DEFAULT NULL,
                  `main_temp_max` FLOAT NULL DEFAULT NULL,
                  `main_sea_level` FLOAT NULL DEFAULT NULL,
                  `main_wind_speed` FLOAT NULL DEFAULT NULL,
                  `main_wind_direction` FLOAT NULL DEFAULT NULL,
                  `main_clouds` FLOAT NULL DEFAULT NULL,
                  `main_rain_volume_1h` INT(11) NULL DEFAULT NULL,
                  `main_rain_volume_3h` INT(11) NULL DEFAULT NULL,
                  `main_snow_volume_1h` INT(11) NULL DEFAULT NULL,
                  `main_snow_volume_3h` INT(11) NULL DEFAULT NULL,
                  `city_weathercol` VARCHAR(45) NULL DEFAULT NULL,
                  PRIMARY KEY (`data_entry_number`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8mb4
                COLLATE = utf8mb4_0900_ai_ci;
                
                CREATE TABLE IF NOT EXISTS `cyclepsychic`.`station_information` (
                  `station_number` INT(11) NOT NULL,
                  `contract_name` VARCHAR(45) NULL DEFAULT NULL,
                  `name` VARCHAR(45) NULL DEFAULT NULL,
                  `address` VARCHAR(45) NULL DEFAULT NULL,
                  `latitude` FLOAT NULL DEFAULT NULL,
                  `longitude` FLOAT NULL DEFAULT NULL,
                  PRIMARY KEY (`station_number`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8mb4
                COLLATE = utf8mb4_0900_ai_ci;
                
                CREATE TABLE IF NOT EXISTS `cyclepsychic`.`station_data` (
                  `data_id` INT(11) NOT NULL AUTO_INCREMENT,
                  `station_number` INT(11) NULL DEFAULT NULL,
                  `timestamp` VARCHAR(20) NULL DEFAULT NULL,
                  `status` VARCHAR(45) NULL DEFAULT NULL,
                  `bike_stands` INT(5) NULL DEFAULT NULL,
                  `available_bike_stands` INT(5) NULL DEFAULT NULL,
                  `available_bikes` INT(5) NULL DEFAULT NULL,
                  `last_update` TIMESTAMP(6) NULL DEFAULT NULL,
                  PRIMARY KEY (`data_id`),
                  CONSTRAINT `fk_station_number`
                    FOREIGN KEY (`station_number`)
                    REFERENCES `cyclepsychic`.`station_information` (`station_number`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8mb4
                COLLATE = utf8mb4_0900_ai_ci;
                
                CREATE INDEX `fk_station_number` ON `cyclepsychic`.`station_data` (`station_number` ASC) VISIBLE;
    """
    mycursor = mydb.cursor()
    mycursor.execute(sqlquery)
    print("Rebuild complete")

# ask user for DB password
password= input("What is the password for the CyclePsychic database?")

mydb = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd=password,
    database="cyclepsychic"
)

delete()
recreate()