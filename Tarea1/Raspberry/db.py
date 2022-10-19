import mariadb

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

    # TODO
    def save_data(self, data:dict) -> None:
        """
            Metodo que guarda datos en la DB
        """

        try:
            sql_save_data = '''
                INSERT INTO datos
                VALUES (%s, %s, %s, %s)
            '''
            # FIXME
            # (id_device, timestamp, mac_address, data)
            new_data = (data)
            self.cursor.execute(sql_save_data, new_data)
            self.db.commit() # actualizo la db

        except:
            print("ERROR AL GUARDAR NUEVO DATO EN LA BASE DE DATOS")

    
    # TODO
    def save_log(self, data:dict) -> None:
        """
            Metodo que guarada un log en la DB
        """

        try:
            sql_save_log = '''
                INSERT INTO logs
                VALUES (%s, %s, %s, %s)
            '''
            # FIXME
            # (deviceId, timestamp, protocolId, transportLayer)
            new_log = ()
            self.cursor.execute(sql_save_log, new_log)
            self.db.commit() # actualizo la db

        except:
            print("ERROR AL GUARDAR NUEVO DATO EN LA BASE DE DATOS")


    def change_config(self, id_protocol:int, transport_layer:int) -> None:
        """
            Meotodo que cambia la configuracionde la BBDD por una nueva
        """

        try:
            sql_change_config = '''
                UPDATE configuracion
                SET protocolId = %s, transportLayer = %s
            '''
            new_config = (id_protocol, transport_layer)
            self.cursor.execute(sql_change_config, new_config)
            self.db.commit() # actualizo la db
        except:
            print("ERROR AL CAMBIAR LA BASE DE DATOS")

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


    