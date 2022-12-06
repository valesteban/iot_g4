import ipaddress
import mariadb


"""
    DB Tarea 2
"""

# Campos:
# db
# cursor
class DB:

    def __init__(self, host:str, user:str, password:str, database:str) -> None:
        """
            Constructor de la BBDD
        """
        self.db = mariadb.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.db.cursor()

    """
    ===    Metodos globales ===
    """

    def delete_all(self) -> None:
        """
            Elimina todos los Logs y Datas
        """

        sql = '''
            DELETE FROM Data
        '''
        self.cursor.execute(sql)

        sql = '''
            DELETE FROM Data_acceloremeter_sensor
        '''
        self.cursor.execute(sql)

        sql = '''
            DELETE FROM Log
        '''
        self.cursor.execute(sql)
        self.db.commit()

    def delete_tables(self) -> None:
        """
            Elimina todas las tablas de la DB
        """
        sql = '''
            drop table Data
        '''
        self.cursor.execute(sql)

        sql = '''
            drop table Data_acceloremeter_sensor
        '''
        self.cursor.execute(sql)

        sql = '''
            drop table Log
        '''
        self.cursor.execute(sql)

        sql = '''
            drop table Configuration
        '''
        self.cursor.execute(sql)

        self.db.commit()


    def get_all_id_device(self) -> tuple:
        """
            Obtiene todos Id_devices registrados en la base de datos
        """

        sql = """
            SELECT id_device
            FROM Configuration
        """

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_all_data_from_id_device(self, id_device):
        """
            Obtiene la data y la data_acc_sensor asociada a una id_device
        """

        sql = """
            SELECT data, data_acceloremeter_sensor
            FROM Data, Data_acceloremeter_sensor
            WHERE id_device = %s
            AND Log_id_device = %s
        """

        self.cursor.execute(sql, (id_device,))
        return self.cursor.fetchall()


    """
    ===    Tabla Configuracion    ===
    """

    def get_device_config(self, id_device) -> tuple:
        """
            Metodo que entrega la configuracion especifica de un device
        """

        sql = """
            SELECT *
            FROM Configuration
            WHERE id_device = %s
        """

        self.cursor.execute(sql, (id_device, ))
        return self.cursor.fetchall()


    def get_all_config(self) -> tuple:
        """
            Metodo que entrega toda la configuracion actual

            Returns:
                [(id_device, status_conf, protocol_conf, ...)]
        """

        sql_show_config = '''
            SELECT *
            FROM Configuration
        '''
        self.cursor.execute(sql_show_config)
        return self.cursor.fetchall()


    def change_config(self, configuration_dict:dict) -> None:
        """
            Meotodo que cambia la tabla configuracion de la BBDD por una nueva.

            Example:
                configuration_dict = {
                    "id_device" : 4,
                    "status_conf" " 20
                    ...
                    }
                DB.change_config(configuration_dict)
        """

        sql = '''
            UPDATE Configuration
            SET id_device = %s, status_conf = %s, protocol_conf = %s, acc_sampling = %s, acc_sensibility = %s,
            gyro_sensibility = %s, bme688_sampling = %s, discontinuos_time = %s, tcp_port = %s, udp_port = %s,
            host_ip_addr = %s, ssid = %s, pass = %s   
        '''

        id_device = configuration_dict["id_device"] # primary key
        status_conf = configuration_dict["status_conf"]
        protocol_conf = configuration_dict["protocol_conf"]
        acc_sampling = configuration_dict["acc_sampling"]
        acc_sensibility = configuration_dict["acc_sensibility"]
        gyro_sensibility = configuration_dict["gyro_sensibility"]
        bme688_sampling = configuration_dict["bme688_sampling"]
        discontinuos_time = configuration_dict["discontinuos_time"]
        tcp_port = configuration_dict["tcp_port"]
        udp_port = configuration_dict["udp_port"]
        host_ip_addr = int(ipaddress.IPv4Address(configuration_dict["host_ip_addr"]))
        ssid = configuration_dict["ssid"]
        pas = configuration_dict["pass"]

        new_config = (id_device, status_conf, protocol_conf, acc_sampling, acc_sensibility, \
            gyro_sensibility, bme688_sampling, discontinuos_time, \
                tcp_port, udp_port, host_ip_addr, ssid, pas)
        self.cursor.execute(sql, new_config)
        self.db.commit() # actualizo la db

    def insert_default_configuration(self):
        """
            Metodo que insertar un valor por defecto de configuracion.
            Para que luego pueda ser modificado.
        """

        #FIXME
        self.delete_all()

        # Primero limpiamos la tabla
        sql = '''
            DELETE FROM Configuration
        '''
        self.cursor.execute(sql)

        # Agregamos valor por defecto
        sql = '''
            INSERT INTO Configuration
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''

        default_value = (0,0,0,0,0,0,0,0,0,0,0,"0","0")
        self.cursor.execute(sql, default_value)
        self.db.commit()

    
        
    

    """
    ===    Tabla Log    ===
    """

    def get_logs(self) -> tuple:
        """
            Metodo que entrega los logs
        """
        sql = '''
            SELECT *
            FROM Log
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def save_log(self, log_dict:dict) -> None:
        """
            Metodo que guarda un log en la DB

            Example:
            log_dict = {
                "id_device": 12,
                "status_report": 20,
                ...
            }
            DB.save_log(log_dict)
        """ 

        # Guardar el log
        sql = '''
            INSERT INTO Log (status_report, protocol_report, battery_level, conf_peripheral,
                                time_client, Configuration_id_device)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        # Obtengo los valores del diccionario para guardar
        # El timestamp del server, lo guarda automaticamente la DB
        status_report = log_dict["status_report"]
        protocol_report = log_dict["protocol_report"]
        battery_level = log_dict["battery_level"]
        conf_peripheral = log_dict["conf_peripheral"]
        time_client = log_dict["time_client"]
        # time_server, se calcula automaticamente
        configuration_id_device = log_dict["configuration_id_device"]

        
        new_log = (status_report, protocol_report, battery_level, conf_peripheral, \
            time_client, configuration_id_device)
        self.cursor.execute(sql, new_log)
        self.db.commit() # actualizo la db


    """
    ===    Tabla Data    ===
    """

    def get_data(self) -> tuple:
        """
            Metodo que entrega los datos ingresados
        """
        sql = '''
            SELECT *
            FROM Data
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def save_data(self, data_dict:dict) -> None:
        """
            Metodo que guarda datos en la DB

            Example:    
                data_dict = {
                    "id_device": 20,
                    "data": {},
                    "log_id_device: 20
                }

                DB.save_data(data_dict)
            
        """

        # Obtengo la ultima id generada en el Log.
        sql = '''
            SELECT id
            FROM Log
            ORDER BY id DESC
            LIMIT 1
        '''
        self.cursor.execute(sql)
        log_id = self.cursor.fetchall()[0][0]

        sql = '''
            INSERT INTO Data (id_device, Log_id, data)
            VALUES (%s, %s, %s)
        '''

        # Obtengo la info del diccionario
        id_device = data_dict["id_device"]
        data = data_dict["data"]

        new_data = (id_device, log_id, data)
        self.cursor.execute(sql, new_data)
        self.db.commit() # actualizo la db


    """
    ===    Tabla Data_acc_sensor    ===
    """
    def get_data_acc_sensor(self) -> tuple:
        """
            Metodo que entrega los datos del acc_sensor
        """
        sql = '''
            SELECT *
            FROM Data_acceloremeter_sensor
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def save_data_acc_sensor(self, data_acc_sensor_dict:dict) -> None:
        """
            Metodo que guarda datos del acc_sensor en la DB

            Example:    
                data_acc_sensor_dict = {
                    "id_device": 20,
                    "data_acc_sensor": {},
                    "log_id_device: 20
                }

                DB.save_data(data_acc_sensor_dict)
            
        """

        # Obtengo la ultima id generada en el Log.
        sql = '''
            SELECT id
            FROM Log
            ORDER BY id DESC
            LIMIT 1
        '''
        self.cursor.execute(sql)
        log_id = self.cursor.fetchall()[0][0]

        sql = '''
            INSERT INTO Data_acceloremeter_sensor (id_device, Log_id, data_acceloremeter_sensor)
            VALUES (%s, %s, %s)
        '''

        # Obtengo la info del diccionario
        id_device = data_acc_sensor_dict["id_device"]
        data_acc_sensor = data_acc_sensor_dict["data_acc_sensor"]

        new_data = (id_device, log_id, data_acc_sensor)
        self.cursor.execute(sql, new_data)
        self.db.commit() # actualizo la db



