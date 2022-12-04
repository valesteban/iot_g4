


def start_status20():
    """
        Inicializa la raspberry en status 20

        El ESP32 tendrá un Cliente TCP y la Raspberry un Servidor TCP (el Ssid, Pass y Port_TCP se
        toman de los valores configurados por la interfaz). En este modo el ESP32 puede actualizar cualquiera
        de los valores de la tabla Parámetros de Configuración a través de una conexión TCP. Los valores
        se adquieren de la tabla config de la DB
    """