import struct

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

    # GETTERS
    def get_level(self) -> int:
        """
            Entrega el batt_level
        """
        return self.level


    def get_timestamp(self) -> int:
        """
            Entrega el timestamp del battery
        """
        return self.timestamp


class THPCSensor:
    bytes_size:int = 10

    def __init__(self, temp= 0, pres = 0., hum = 0, co_2 = 0.) -> None:
        self.temp: int = temp
        self.pres: float = pres
        self.hum: int = hum
        self.co_2: float = co_2

    def __str__(self) -> str:
        return f"(temp: {self.temp}; hum: {self.hum}; pres: {self.pres:.4f}; CO_2: {self.co_2:.4f})"

    def decode(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = 10
        unpacked = struct.unpack('<bfbf', arrBytes[pos:pos+read_bytes])

        self.temp, self.pres, self.hum, self.co_2 = unpacked
        return read_bytes

    # GETTERS
    def get_temp(self) -> int:
        """
            Entrega la temperatura del sensor
        """ 
        return self.temp

    def get_pres(self) -> float:
        """
            Entrega presion del sensor
        """ 
        return self.pres

    def get_hum(self) -> int:
        """
            Entrega la humedad del sensor
        """ 
        return self.hum

    def get_co2(self) -> float:
        """
            Entrega el co2 del sensor
        """ 
        return self.co_2


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
    
    # GETTERS
    def get_rms(self) -> float:
        """
            Entrega el rms del accel. kpi
        """
        return self.rms

    def get_amp_x(self) -> float:
        """
            Entrega el amp_x del accel. kpi
        """
        return self.amp_x

    def get_frec_x(self) -> float:
        """
            Entrega el frec_x del accel. kpi
        """
        return self.frec_x

    def get_amp_y(self) -> float:
        """
            Entrega el amp_y del accel. kpi
        """
        return self.amp_y

    def get_frec_y(self) -> float:
        """
            Entrega el frec_y del accel. kpi
        """
        return self.frec_y

    def get_amp_z(self) -> float:
        """
            Entrega el amp_z del accel. kpi
        """
        return self.amp_z

    def get_frec_z(self) -> float:
        """
            Entrega el frec_z del accel. kpi
        """
        return self.frec_z

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
    
    # GETTERS
    def get_acc_x(self) -> list[float]:
        """
            Entrega la data del eje x del medidor de aceleracion
        """
        return self.data_x

    def get_acc_y(self) -> list[float]:
        """
            Entrega la data del eje y del medidor de aceleracion
        """
        return self.data_y

    def get_acc_z(self) -> list[float]:
        """
            Entrega la data del eje z del medidor de aceleracion
        """
        return self.data_z