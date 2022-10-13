#cosas por mientras reemplazando bbdd
# 0 = TCP | 1 = UDP
#ID_PROTOCOL -->  0,1,2,3,4 
#TRANSPORT_LAYER -->  0 = TCP | 1 = UDP


def get_protocol() -> dict:
    """
    Funcion que consulta la base de datos preguntando por el procolo a utilizar
    """

    data = {
       "id_protocol": 2,
        "transport_layer": 1
    }

    return data

