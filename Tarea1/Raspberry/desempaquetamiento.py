import struct


class Header:
    bytes_size:int = 12

    def __init__(self, id=0, mac=0, t_layer=0, protocol=0, len_msg=0) -> None:
        self.id: int = id
        self.mac: int = mac
        self.t_layer: int = t_layer
        self.protocol: int = protocol
        self.len_msg: int = len_msg

    def __str__(self) -> str:
        return f"(id: {self.id}; mac: {self.mac}; t_layer: {self.t_layer}; protocol: {self.protocol}; len_msg: {self.len_msg})"

    # idmacBytes idealmente debe ser un arreglo de 8 bytes
    def decode_id_mac(self, idmac_bytes: bytes) -> None:
        idmac = int.from_bytes(idmac_bytes, "little")
        self.id = idmac >> 48
        mask = int("0x0000ffffffffffff",16)
        self.mac = idmac & mask

    # tpl_bytes idealmente debe ser de largo 4 bytes
    def decode_tpl(self, tpl_bytes: bytes) -> None:
        tpl = int.from_bytes(tpl_bytes, "little")
        self.t_layer = tpl >> 24
        protocol = tpl >> 16
        self.protocol = protocol & int("0x000000ff",16)
        self.len_msg = tpl & int("0x0000ffff",16)

    def decode(self, arrBytes: bytes, pos: int) -> int:
        self.decode_id_mac(arrBytes[pos: pos+8])
        read_bytes = 8
        pos += 8

        self.decode_tpl(arrBytes[pos: pos+4])
        read_bytes += 4

        return read_bytes

class BattSensor:
    bytes_size:int = 6
    def __init__(self, level=0, timestamp=0) -> None:
        self.data_1: int = 1
        self.level: int = level
        self.timestamp: int = timestamp
    
    def __str__(self) -> str:
        return f"(battery_level: {self.level}; time_stamp: {self.timestamp}; data_1: {self.data_1})"
    
    def decode(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = 6
        self.data_1, self.level, self.timestamp = struct.unpack('<bbi', arrBytes[pos:pos+read_bytes])
        return read_bytes

class THPCSensor:
    bytes_size:int = 10

    def __init__(self, temp= 0, pres = 0., hum = 0, co_2 = 0.) -> None:
        self.temp: int = temp
        self.pres: float = pres
        self.hum: int = hum
        self.co_2: float = co_2

    def __str__(self) -> str:
        return f"(temp: {self.temp}; hum: {self.hum}; pres: {self.pres:.4f}; hum: {self.co_2:.4f})"

    def decode(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = 10
        unpacked = struct.unpack('<bfbf', arrBytes[pos:pos+read_bytes])

        self.temp, self.pres, self.hum, self.co_2 = unpacked
        return read_bytes


class AccelKPI:
    bytes_size:int = 28
    def __init__(self, rms=0., amp_x=0., frec_x=0., amp_y=0., frec_y=0., amp_z=0., frec_z=0.):
        self.rms: float = rms
        self.amp_x: float = amp_x
        self.frec_x: float = frec_x
        self.amp_y: float = amp_y
        self.frec_y: float = frec_y
        self.amp_z: float = amp_z
        self.frec_z: float = frec_z

    def __str__(self) -> str:
        return f"(amp_x: {self.amp_x:.4f}; frec_x: {self.frec_x:.4f}; amp_y: {self.amp_y:.4f}; frec_y: {self.frec_y:.4f}; amp_z: {self.amp_z:.4f}; frec_z: {self.frec_z:.4f}; rms: {self.rms:.4f})"

    def decode(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = 4*7
        #unpacked = struct.unpack('<7f', arrBytes[pos:pos+read_bytes])
        unpacked = struct.unpack('<7f', arrBytes[pos:pos+read_bytes])

        self.rms, self.amp_x, self.frec_x, self.amp_y, self.frec_y, self.amp_z, self.frec_z = unpacked
        
        return read_bytes

class AccelSensor:

    def __init__(self, data_x=[], data_y=[], data_z=[], size=0) -> None:
        self.data_x: list[float] = data_x
        self.data_y: list[float] = data_y
        self.data_z: list[float] = data_z
        self.size: int = size

    def __str__(self) -> str:
        return "[" + ",\n".join([f"(Acc_x: {self.data_x[i]:.4f}; Acc_y: {self.data_y[i]:.4f}; Acc_z: {self.data_z[i]:.4f})" for i in range(self.size)]) + "]\n"

    def decode(self, arrBytes: bytes, size:int, pos: int = 0) -> int:
        attrs = ["data_x", "data_y", "data_z"]
        arr_byte_len = 4*size
        read_bytes = 3*arr_byte_len
        for i in range(len(attrs)):
            member = attrs[i]
            unpacked = struct.unpack('<{}f'.format(size), arrBytes[pos+arr_byte_len*i:pos+arr_byte_len*(i+1)])
            setattr(self, member, list(unpacked))
        self.size = size

        return read_bytes

class Protocol:

    def __init__(self) -> None:
        self.header: Header = Header()
        self.battery: BattSensor = BattSensor()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}\nHEADER =" + "\n\t".join(f"{getattr(self, member)}" for member in vars(self))

    def decode_msg(self, arrBytes: bytes, pos: int = 0) -> int:
        return self.battery.decode(arrBytes, pos)

    @classmethod
    def from_header(cls, header: Header) -> "Protocol":
        newPro = cls()
        newPro.header = header
        return newPro

class Protocol0(Protocol):
    len_msg:int = 6

    def __init__(self) -> None:
        super().__init__()


class Protocol1(Protocol):
    len_msg:int = 16

    def __init__(self) -> None:
        super().__init__()
        self.thpc: THPCSensor = THPCSensor()

    def decode_msg(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = super().decode_msg(arrBytes, pos)
        total_bytes = read_bytes
        pos += read_bytes

        total_bytes += self.thpc.decode(arrBytes, pos)

        return total_bytes


class Protocol2(Protocol):
    len_msg:int = 20

    def __init__(self) -> None:
        super().__init__()
        self.thpc: THPCSensor = THPCSensor()
        self.kpi: AccelKPI = AccelKPI()

    def decode_msg(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = super().decode_msg(arrBytes, pos)
        total_bytes = read_bytes
        pos += read_bytes

        read_bytes = self.thpc.decode(arrBytes, pos)
        total_bytes += read_bytes
        pos += read_bytes

        self.kpi.rms = struct.unpack('<f', arrBytes[pos:pos+4])[0]

        return total_bytes+4


class Protocol3(Protocol):
    len_msg:int = 44

    def __init__(self) -> None:
        super().__init__()
        self.thpc: THPCSensor = THPCSensor()
        self.kpi: AccelKPI = AccelKPI()

    def decode_msg(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = super().decode_msg(arrBytes, pos)
        total_bytes = read_bytes
        pos += read_bytes

        read_bytes = self.thpc.decode(arrBytes, pos)
        total_bytes += read_bytes
        pos += read_bytes

        total_bytes += self.kpi.decode(arrBytes, pos)

        return total_bytes

class Protocol4(Protocol):
    len_msg_without_acc:int = 16

    def __init__(self) -> None:
        super().__init__()
        self.thpc: THPCSensor = THPCSensor()
        self.acc: AccelSensor = AccelSensor()
        self.len_data = 0

    def decode_msg(self, arrBytes: bytes, size: int=0, pos: int=0) -> int:
        if size <= 0:
            size = self.header.len_msg - Protocol4.len_msg_without_acc
        read_bytes = super().decode_msg(arrBytes, pos)
        total_bytes = read_bytes
        pos += read_bytes

        read_bytes = self.thpc.decode(arrBytes, pos)
        total_bytes += read_bytes
        pos += read_bytes

        total_bytes += self.acc.decode(arrBytes, size, pos)
        self.len_data = size

        return total_bytes

def decode_pkg(encoded_pkg: bytes) -> Protocol:
    translation: dict[str, Protocol] = {
        0: Protocol0,
        1: Protocol1,
        2: Protocol2,
        3: Protocol3,
        4: Protocol4
    }

    curr = 0

    header = Header()
    read_bytes = header.decode(encoded_pkg, 0)
    curr += read_bytes

    proClass = translation[header.protocol]
    pro = proClass.from_header(header)
    pro.decode_msg(encoded_pkg, pos=curr)

    return pro


if __name__ == "__main__":
    hex = "94 01 00 00 00 00 08 00 06 00 00 01 01 54 34 95 47 63"
    b = bytes.fromhex(hex)
    he = b.hex()

    hex1 = "94 01 00 00 00 00 08 00 10 00 01 01 01 57 c9 99 48 63 10 8b ca 93 44 40 be 55 7e 42"
    b1 = bytes.fromhex(hex1)

    hex3 = "94 01 00 00 00 00 08 00 2c 00 03 01 01 1b 47 b8 48 63 0f a6 d0 7a 44 3d dd 94 8e 42 68 01 c6 3d a8 9a b0 3c 45 6a ee 41 29 cf b6 3d d0 09 6d 42 90 cb f7 3c 6c 6f b2 42"
    b3 = bytes.fromhex(hex3)

    hex2 = "94 01 00 00 00 00 08 00 14 00 02 01 01 57 72 a6 48 63 15 68 d9 8a 44 4b a4 50 de 42 8b c5 f5 3d"
    b2 = bytes.fromhex(hex2)

    hex4 = '94 01 00 00 00 00 08 00 24 00 04 01 01 44 e0 c1 48 63 16 52 fa 91 44 2f 16 26 06 43 40 21 67 3e 37 e9 73 3e 5b 57 80 3e cf b8 86 3e e6 18 8d 3e 90 77 93 3e bc d4 99 3e 5c 30 a0 3e 5b 8a a6 3e ad e2 ac 3e 3f 39 b3 3e 02 8e b9 3e e3 e0 bf 3e d6 31 c6 3e c6 80 cc 3e a6 cd d2 3e 65 18 d9 3e f1 60 df 3e 3d a7 e5 3e 35 eb eb 3e fc c5 3e 40 2a a2 3e 40 6c 7c 3e 40 c0 54 3e 40 29 2b 3e 40 a5 ff 3d 40 36 d2 3d 40 dc a2 3d 40 96 71 3d 40 67 3e 3d 40 4f 09 3d 40 4d d2 3c 40 62 99 3c 40 8f 5e 3c 40 d6 21 3c 40 35 e3 3b 40 ae a2 3b 40 42 60 3b 40 f2 1b 3b 40 bd d5 3a 40 c8 74 90 3f c2 71 98 3f 32 6d a0 3f 03 67 a8 3f 20 5f b0 3f 74 55 b8 3f eb 49 c0 3f 73 3c c8 3f f2 2c d0 3f 58 1b d8 3f 8f 07 e0 3f 82 f1 e7 3f 1c d9 ef 3f 4c be f7 3f f8 a0 ff 3f 88 c0 03 40 3f af 07 40 97 9c 0b 40 86 88 0f 40 01 73 13 40'
    b4 = bytes.fromhex(hex4)

    

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
    print(decode_pkg(b))
    print(decode_pkg(b1))
    print(decode_pkg(b2))
    print(decode_pkg(b3))
    print(decode_pkg(b4))

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
