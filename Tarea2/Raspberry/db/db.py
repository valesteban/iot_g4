import mariadb
import json
from desempaquetamiento import Protocol


class DB:

    def __init__(self, host, user, password, database) -> None:
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


    def change_config(self, id_protocol:int, transport_layer:int) -> None:
        """
            Meotodo que cambia la configuracionde la BBDD por una nueva
        """

        sql_change_config = '''
            UPDATE configuracion
            SET protocolId = %s, transportLayer = %s
        '''
        new_config = (id_protocol, transport_layer)
        self.cursor.execute(sql_change_config, new_config)
        self.db.commit() # actualizo la db

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

