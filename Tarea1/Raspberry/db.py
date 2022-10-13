import mysql.connector

class DB:

    def __init__(self, host, user, password, database) -> None:
        self.db = mysql.connector.connect(
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

            returns: ((protocolId), transportLayer)) 
        """
        sql = '''
            SELECT protocolId, transportLayer
            FROM configuracion
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

