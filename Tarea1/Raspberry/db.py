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


    def get_protocol2(self) -> tuple:
        """
            Metodo que consulta la base de datos preguntando por el procolo a utilizar
        """
        sql = '''

        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()



def get_protocol() -> tuple:
    """
        Funcion que consulta la base de datos preguntando por el procolo a utilizar
    """

    # 0: "id_protocol"
    # 1: "transport_layer"

    data = (2, 0)

    return data
