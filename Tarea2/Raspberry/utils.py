import json
from mensaje.protocol import Protocol

def get_protocol_values(data: Protocol) -> dict:
    """
        Funcion auxiliar que procesa un protocolo y obtiene
        toda la info necesaria para ser guardada en la DB
    """

    header = data.get_header()
    id_device = header.get_device_id()
    mac = header.get_mac()
    transport_layer = header.get_transport_layer()
    id_protocol = header.get_protocol_id()

    battery = data.get_battery()
    timestamp = battery.get_timestamp()

    protocol_data = json.dumps(data.get_protocol_data())

    protocol_values = {
        "id_device" : id_device,
        "timestamp" : timestamp,
        "mac": mac,
        "id_protocol": id_protocol,
        "transport_layer": transport_layer,
        "data" : protocol_data
    }

    return protocol_values



def parse_config(configuracion:list) -> dict:
    """
        Recibe una configuracion en forma de lista y la entrega con forma de diccionario
    """
    d = {
        "id_device": configuracion[0],
        "status_conf": configuracion[1],
        "protocol_conf": configuracion[2],
        "acc_sampling": configuracion[3],
        "acc_sensibility": configuracion[4],
        "gyro_sensibility": configuracion[5],
        "bme688_sampling": configuracion[6],
        "discontinuos_time": configuracion[7],
        "tcp_port": configuracion[8],
        "udp_port": configuracion[9],
        "host_ip_addr": configuracion[10],
        "ssid": configuracion[11],
        "pass": configuracion[12],
    }

    return d