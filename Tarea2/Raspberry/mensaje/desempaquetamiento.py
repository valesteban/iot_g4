from mensaje.header import Header

from mensaje.protocol import Protocol
from mensaje.protocol import Protocol0
from mensaje.protocol import Protocol1
from mensaje.protocol import Protocol2
from mensaje.protocol import Protocol3
from mensaje.protocol import Protocol4

import json


translation: dict[str, Protocol] = {
        0: Protocol0,
        1: Protocol1,
        2: Protocol2,
        3: Protocol3,
        4: Protocol4
    }

def decode_pkg(encoded_pkg: bytes) -> Protocol:
    curr = 0

    header = Header()
    read_bytes = header.decode(encoded_pkg, 0)
    check_pkg_integrity(header, encoded_pkg[12:])
    curr += read_bytes

    proClass = translation[header.protocol]
    pro = proClass.from_header(header)
    try:
        pro.decode_msg(encoded_pkg, pos=curr)
    except Exception as e:
        if len(e.args) >= 1:
            additional = "    Received Header: {}\n".format(header)
            e.args = (e.args[0]+str(additional),)+e.args[1:]
            raise(e)

    
    return pro

def check_pkg_integrity(a_header: Header, msg_bytes: bytes):

    for fun_str in ["check_t_layer", "check_protocol"]:
        fun = getattr(a_header, fun_str)
        integrity, attr_name, attr_value = fun()
        if not integrity:
            raise Exception("Corrupt header:{}\n Incorrect value {} for attribute {}.".format(a_header, attr_value, attr_name))
    
    # check msg len
    declared_msg_len = a_header.get_message_length()
    declared_protocol = a_header.get_protocol_id()

    actual_msg_len = len(msg_bytes)

    if declared_msg_len != actual_msg_len:
        raise Exception("Expected message of length {}, got {}".format(declared_msg_len, actual_msg_len))

    if declared_protocol in range(0,4):
        expected_msg_len = translation[declared_protocol].len_msg
        if declared_msg_len != expected_msg_len:
            raise Exception("Message of length {} does not match length of {} for Protocol {}".format(declared_msg_len, expected_msg_len, declared_protocol))
        
    else: #Protocolo 4
        diff = translation[declared_protocol].len_msg_without_acc
        declared_array_len = declared_msg_len - diff
        if (declared_array_len % 12) != 0: # Bytes not divisible by 12
            raise Exception("Cannot decode message as Protocol {}. Invalid array length of {}, should be divisible by 12.".format(declared_protocol, declared_array_len))

def print_hex(hex_str):
    n = len(hex_str)
    hex_stride = 2
    hex_line_stride = 16

    for i in range(0,n,hex_line_stride*hex_stride):
        piece_len = min(hex_line_stride*hex_stride, n-i)
        hex_piece = hex_str[i:i+piece_len]

        bytes_in_line = (i//2).to_bytes(4, "big").hex()
        print(" ", bytes_in_line, "|  ", end=" ")
        for j in range(i,i+piece_len,hex_stride):
            print(hex_str[j:j+hex_stride], end=" ")
        print()


def get_protocol_values(data: Protocol, status, conf_peripheral) -> dict:
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

    protocol_data = data.get_protocol_data()

    # conf_peripheral = 
    # acc_sampling + acc_sensibility + gyro_sensibility + bme688_sampling

    protocol_values = {
        "id_device" : 3,
        "status_report" : status,
        "protocol_report": id_protocol,
        "battery_level": battery.get_level(),
        "conf_peripheral": conf_peripheral,
        "time_client" : timestamp,
        "configuration_id_device": 3,
        "data": protocol_data
    }

    return protocol_values 


if __name__ == "__main__":
    hex = "94 01 00 00 00 00 08 00 06 00 00 01 01 54 34 95 47 63"
    b = bytes.fromhex(hex)
    he = b.hex()

    hex1 = "24 00 00 00 00 00 59 04 10 00 01 00 01 0c bb 44 c7 01 06 ad fc 84 44 36 54 b2 44 43"
    b1 = bytes.fromhex(hex1)

    hex3 = "94 01 00 00 00 00 08 00 2c 00 03 01 01 1b 47 b8 48 63 0f a6 d0 7a 44 3d dd 94 8e 42 68 01 c6 3d a8 9a b0 3c 45 6a ee 41 29 cf b6 3d d0 09 6d 42 90 cb f7 3c 6c 6f b2 42"
    b3 = bytes.fromhex(hex3)

    hex2 = "94 01 00 00 00 00 08 00 14 00 02 01 01 57 72 a6 48 63 15 68 d9 8a 44 4b a4 50 de 42 8b c5 f5 3d"
    b2 = bytes.fromhex(hex2)

    hex4 = '94 01 00 00 00 00 08 00 00 01 04 01 01 44 e0 c1 48 63 16 52 fa 91 44 2f 16 26 06 43 40 21 67 3e 37 e9 73 3e 5b 57 80 3e cf b8 86 3e e6 18 8d 3e 90 77 93 3e bc d4 99 3e 5c 30 a0 3e 5b 8a a6 3e ad e2 ac 3e 3f 39 b3 3e 02 8e b9 3e e3 e0 bf 3e d6 31 c6 3e c6 80 cc 3e a6 cd d2 3e 65 18 d9 3e f1 60 df 3e 3d a7 e5 3e 35 eb eb 3e fc c5 3e 40 2a a2 3e 40 6c 7c 3e 40 c0 54 3e 40 29 2b 3e 40 a5 ff 3d 40 36 d2 3d 40 dc a2 3d 40 96 71 3d 40 67 3e 3d 40 4f 09 3d 40 4d d2 3c 40 62 99 3c 40 8f 5e 3c 40 d6 21 3c 40 35 e3 3b 40 ae a2 3b 40 42 60 3b 40 f2 1b 3b 40 bd d5 3a 40 c8 74 90 3f c2 71 98 3f 32 6d a0 3f 03 67 a8 3f 20 5f b0 3f 74 55 b8 3f eb 49 c0 3f 73 3c c8 3f f2 2c d0 3f 58 1b d8 3f 8f 07 e0 3f 82 f1 e7 3f 1c d9 ef 3f 4c be f7 3f f8 a0 ff 3f 88 c0 03 40 3f af 07 40 97 9c 0b 40 86 88 0f 40 01 73 13 40'
    b4 = bytes.fromhex(hex4)
    print_hex(b4.hex())

    

    """
    print(hex)
    
    print(b[0:4])
    first2bytes = int.from_bytes(b[0:8], "little")
    print(first2bytes >> 48)
    mask = int("0x0000ffffffffffff",16)
    print(mask)
    print(first2bytes & mask)

    tplBytes = int.from_bytes(b[8:12], "little")
    print(tplBytes >> 24)
    print((tplBytes >> 16) & (int("0x000000ff",16)))
    print(tplBytes & int("0x0000ffff",16))

    msg = b[12:18]

    h = Header()
    h.decode(b, 0)
    print(h)

    print("struct", struct.unpack('<bbi', b[12:18]))

    val1 = msg[0]
    print(val1)

    batt = msg[1]
    print(batt)

    times = int.from_bytes(msg[2:6], "little")
    print(times)

    p0 = Protocol0()
    p0.decode_msg(b[12:18], 0)
    print("Protocol0: ", p0)

    print(b1)
    print(b1[18])
    print(struct.unpack('<f', b1[19:23]))

    p1 = Protocol1()
    p1.decode_msg(b1[12:],0)
    print("Protocol1: ", p1)

    
    p2 = Protocol2()
    p2.decode_msg(b2[12:],0)
    print("Protocol2: ", p2)

    #       0  1  2  3  4  5  6        9                             19                            29       32          36     
    hex3 = "94 01 00 00 00 00 08 00 2c 00 03 01 01 1b 4a a8 48 63 0f a6 d0 7a 44 3d dd 94 8e 42 68 01 c6 3d 00 00 30 a8 9a b0 3c 00 00 20 45 6a ee 41 00 00 00 29 cf b6 3d 00 00 00"
        """

    """
PROTOCOL 3
    HEADER={id: 8; mac: 404; t_layer: 1; protocol: 3; len_msg: 44}
    MSG=[{battery_level: 27; time_stamp: 1665710151; data_1: 1},
        {temp: 15; hum: 61; pres: 1003.2601; hum: 71.2907},
        {amp_x: 0.0216; frec_x: 29.8019; amp_y: 0.0893; frec_y: 59.2596; amp_z: 0.0302; frec_z: 89.2176; rms: 0.0967}]    Printing 56 bytes as hex
    """
    """
    p3 = Protocol3()
    a = AccelKPI()
    #print("co2", struct.unpack('<f', b3[32:36]))
    #print(a.decode(b3[28:], 0))
    #print(a)
    p3.decode_msg(b3[12:],0)
    print(p3)

    header4 = Header()
    header4.decode(b4, 0)

    p4 = Protocol4()
    p4.decode_msg(b4[12:], header4.len_msg - Protocol4.len_msg_without_acc)
    print(p4)
    """
    print("\n", decode_pkg(b))
    print("\n", decode_pkg(b1))
    print("\n", decode_pkg(b2))
    print("\n", decode_pkg(b3))
    print("\n", decode_pkg(b4))

"""
[{Acc_x: 0.2257; Acc_y: 2.9808; Acc_z: 1.1286},
{Acc_x: 0.2382; Acc_y: 2.9786; Acc_z: 1.1910},
{Acc_x: 0.2507; Acc_y: 2.9763; Acc_z: 1.2533},
{Acc_x: 0.2631; Acc_y: 2.9739; Acc_z: 1.3156},
{Acc_x: 0.2756; Acc_y: 2.9714; Acc_z: 1.3779},
{Acc_x: 0.2880; Acc_y: 2.9687; Acc_z: 1.4401},
{Acc_x: 0.3005; Acc_y: 2.9660; Acc_z: 1.5023},
{Acc_x: 0.3129; Acc_y: 2.9631; Acc_z: 1.5643},
{Acc_x: 0.3253; Acc_y: 2.9601; Acc_z: 1.6264},
{Acc_x: 0.3377; Acc_y: 2.9569; Acc_z: 1.6883},
{Acc_x: 0.3500; Acc_y: 2.9537; Acc_z: 1.7502},
{Acc_x: 0.3624; Acc_y: 2.9503; Acc_z: 1.8121},
{Acc_x: 0.3748; Acc_y: 2.9469; Acc_z: 1.8738},
{Acc_x: 0.3871; Acc_y: 2.9433; Acc_z: 1.9355},
{Acc_x: 0.3994; Acc_y: 2.9396; Acc_z: 1.9971},
{Acc_x: 0.4117; Acc_y: 2.9357; Acc_z: 2.0586},
{Acc_x: 0.4240; Acc_y: 2.9318; Acc_z: 2.1201},
{Acc_x: 0.4363; Acc_y: 2.9278; Acc_z: 2.1814},
{Acc_x: 0.4485; Acc_y: 2.9236; Acc_z: 2.2427},
{Acc_x: 0.4608; Acc_y: 2.9193; Acc_z: 2.3039}]
"""
