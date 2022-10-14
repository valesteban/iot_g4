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

    #def add_data(self, data:dict) -> None:
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