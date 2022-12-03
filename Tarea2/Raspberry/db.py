import mariadb
import json


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
    ===    Tabla Configuracion    ===
    """

    def change_config(self, configuration_dict:dict) -> None:
        """
            Meotodo que cambia la configuracionde la BBDD por una nueva.

            Example:
                configuration_dict = {
                    "id_device" : 4,
                    "status_conf" " 20
                    ...
                    }
                DB.change_config(configuration_dict)
        """

        sql = '''
            UPDATE configuracion
            SET id_device = %s, status_conf = %s, protocol_conf = %s, acc_sampling = %s, acc_sensibility = %s,
            gyro_sensibility = %s, bme688_sampling = %s, discontinuos_time = %s, tcp_port = %s, udp_port = %s,
            host_ip_addr = %s, ssid = %s, pas = %s   
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
        host_ip_addr = configuration_dict["host_ip_addr"]
        ssid = configuration_dict["ssid"]
        pas = configuration_dict["pass"]

        new_config = (id_device, status_conf, protocol_conf, acc_sampling, acc_sensibility, \
            gyro_sensibility, bme688_sampling, discontinuos_time, \
                tcp_port, udp_port, host_ip_addr, ssid, pas)
        self.cursor.execute(sql, new_config)
        self.db.commit() # actualizo la db
    

    def get_data(self) -> tuple:
        """
            Metodo que entrega los datos ingresados
        """
        sql = '''
            SELECT *
            FROM datos
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_logs(self) -> tuple:
        """
            Metodo que entrega los logs
        """
        sql = '''
            SELECT *
            FROM logs
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_protocol(self) -> tuple:
        """
            Metodo que consulta la base de datos preguntando por el procolo a utilizar

            returns: ((protocolId), transportLayer), ) 
        """ 
        sql = '''
            SELECT protocolId, transportLayer
            FROM configuracion
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def save_data(self, protocol_values:dict) -> None:
        """
            Metodo que guarda datos en la DB
        """

        #try:
        sql_save_data = '''
            INSERT INTO datos (deviceId, timestamp, mac_address, data)
            VALUES (%s, %s, %s, %s)
        '''

        # (id_device, timestamp, mac_address, data)
        new_data = (protocol_values["id_device"], protocol_values["timestamp"], protocol_values["mac"], protocol_values["data"],)
        print("NEW DATA:", new_data)
        self.cursor.execute(sql_save_data, new_data)
        self.db.commit() # actualizo la db

        #except:
        #    print("ERROR AL GUARDAR NUEVO DATO EN LA BASE DE DATOS")

    
    def save_log(self, protocol_values:dict) -> None:
        """
            Metodo que guarda un log en la DB
        """
        # Obtener id del dato
        #try:
        sql = '''
            SELECT id
            FROM datos
            WHERE deviceId = %s
            AND timestamp = %s
        '''
        self.cursor.execute(sql, (protocol_values["id_device"], protocol_values["timestamp"],))
        dato_id = self.cursor.fetchall()[0][0]
        #except:
        #pprint("logs: ERROR AL ENCONTRAR EL DATO")

        # Guardar el log
        #try:
        sql_save_log = '''
            INSERT INTO logs
            VALUES (%s, %s, %s, %s, %s)
        '''
        # (datos_id, deviceId, timestamp, protocolId, transportLayer)
        new_log = (dato_id, protocol_values["id_device"], protocol_values["timestamp"], protocol_values["id_protocol"], protocol_values["transport_layer"])
        self.cursor.execute(sql_save_log, new_log)
        self.db.commit() # actualizo la db

        #except:
        #    print("ERROR AL GUARDAR NUEVO DATO EN LA BASE DE DATOS")


    def return_config(self) -> tuple:
        """
            Metodo que entrega la configuracion actual
        """

        sql_show_config = '''
            SELECT *
            FROM configuracion
        '''
        self.cursor.execute(sql_show_config)
        return self.cursor.fetchall()

    def delete_all_data(self) -> None:
        """
            Metodo que limpia la tabla de datos
        """

        sql = '''
            DELETE FROM datos
        '''

        self.cursor.execute(sql)
        self.db.commit()

    def delete_all_logs(self) -> None:
        """
            Metodo que elimina los logs
        """

        sql = '''
            DELETE FROM logs
        '''

        self.cursor.execute(sql)
        self.db.commit()

