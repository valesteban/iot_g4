import json
from desempaquetamiento import Protocol

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
