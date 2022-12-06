import struct

from header import Header

from sensor import BattSensor
from sensor import THPCSensor
from sensor import AccelKPI
from sensor import AccelSensor

class Protocol:

    def __init__(self) -> None:
        self.header: Header = Header()
        self.battery: BattSensor = BattSensor()
        # Timestamp es atributto de Battsensor

    def __str__(self) -> str:
        res = f"{self.__class__.__name__}\n"
        attrs = vars(self)
        for member in attrs:
            member_obj = getattr(self, member)
            member_obj_name = member_obj.__class__.__name__.upper()
            res += f"\n\t{member_obj_name} ={member_obj}"
        return  res

    def decode_msg(self, arrBytes: bytes, pos: int = 0) -> int:
        return self.battery.decode(arrBytes, pos)

    def get_protocol_data(self) -> dict:
        """
            Entrega la data asociada a cada protocolo.
            Por defecto entrega el batt_level y timestamp
        """

        batt_level = self.battery.get_level()
        timestamp = self.battery.get_timestamp()

        data = {
            "batt_level": batt_level,
            "timestamp" : timestamp
        }

        return data

    @classmethod
    def from_header(cls, header: Header) -> "Protocol":
        newPro = cls()
        newPro.header = header
        return newPro

    # GETTERS
    def get_header(self) -> Header:
        """
            Entrega el header del mensaje
        """
        return self.header

    def get_battery(self) -> BattSensor:
        """
            Entrega el attributo battery del protocolo
        """
        return self.battery

    
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

    # Override
    def get_protocol_data(self) -> dict:
        """
            Entrega la data asociada al protocolo 1 en forma de dict
        """

        # Batt sensor
        data = super().get_protocol_data()

        # Protocolo 1 data
        # THPC sensor
        temp = self.thpc.get_temp()
        press = self.thpc.get_pres()
        hum = self.thpc.get_hum()
        co = self.thpc.get_co2()

        data["temp"] = temp
        data["press"] = press
        data["hum"] = hum
        data["co"] = co
        
        return data


class Protocol2(Protocol):
    len_msg:int = 20

    def __init__(self) -> None:
        super().__init__()
        self.thpc: THPCSensor = THPCSensor()
        self.kpi: AccelKPI = AccelKPI()
    
    def __str__(self) -> str:
        res = f"{self.__class__.__name__}\n"
        attrs = vars(self)
        for member in attrs:
            member_obj = getattr(self, member)
            member_obj_name = member_obj.__class__.__name__.upper()
            if member == "kpi":
                res += f"\n\t{member_obj_name} =(rms: {self.kpi.rms:.4f})"
            else:
                res += f"\n\t{member_obj_name} ={member_obj}"
        return  res


    def decode_msg(self, arrBytes: bytes, pos: int) -> int:
        read_bytes = super().decode_msg(arrBytes, pos)
        total_bytes = read_bytes
        pos += read_bytes

        read_bytes = self.thpc.decode(arrBytes, pos)
        total_bytes += read_bytes
        pos += read_bytes

        self.kpi.rms = struct.unpack('<f', arrBytes[pos:pos+4])[0]

        return total_bytes+4

    # Override
    def get_protocol_data(self) -> dict:
        """
            Entrega la data asociada al protocolo 2 en forma de dict
        """
        # Batt sensor
        data = super().get_protocol_data()

        # Protocol 2 data
        # THPC sensor
        temp = self.thpc.get_temp()
        press = self.thpc.get_pres()
        hum = self.thpc.get_hum()
        co = self.thpc.get_co2()

        # RMS Kpi sensor
        rms = self.kpi.get_rms()

        data["temp"] = temp
        data["press"] = press
        data["hum"] = hum
        data["co"] = co
        data["rms"] = rms

        return data 


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

    # Override
    def get_protocol_data(self) -> dict:
        """
            Entrega la data asociada al protocolo 3 como dict
        """
        # Batt sensor
        data = super().get_protocol_data()

        # Protocol 3 data
        # THPC sensor
        temp = self.thpc.get_temp()
        press = self.thpc.get_pres()
        hum = self.thpc.get_hum()
        co = self.thpc.get_co2()

        # KPI sensor
        rms = self.kpi.get_rms()
        amp_x = self.kpi.get_amp_x()
        frec_x = self.kpi.get_frec_x()
        amp_y = self.kpi.get_amp_y()
        frec_y = self.kpi.get_frec_y()
        amp_z = self.kpi.get_amp_z()
        frec_z = self.kpi.get_frec_z()

        data["temp"] = temp
        data["press"] = press
        data["hum"] = hum
        data["co"] = co
        data["rms"] = rms
        data["amp_x"] = amp_x
        data["frec_x"] = frec_x
        data["amp_y"] = amp_y
        data["frec_y"] = frec_y
        data["amp_z"] = amp_z
        data["frec_z"] = frec_z

        return data 

class Protocol4(Protocol):
    len_msg_without_acc:int = 16

    def __init__(self) -> None:
        super().__init__()
        self.thpc: THPCSensor = THPCSensor()
        self.acc: AccelSensor = AccelSensor()
        self.len_data = 0

    def __str__(self) -> str:
        res = f"{self.__class__.__name__}\n"
        attrs = vars(self)
        for member in attrs:
            member_obj = getattr(self, member)
            member_obj_name = member_obj.__class__.__name__.upper()
            if (member != "len_data"):
                res += f"\n\t{member_obj_name} ={member_obj}"
        return  res

    def decode_msg(self, arrBytes: bytes, size: int=0, pos: int=0) -> int:
        if size <= 0:
            size = self.header.len_msg - Protocol4.len_msg_without_acc
        sizeof_float = struct.calcsize("<f")
        num_coords = 3
        arr_len = int((size/sizeof_float)/num_coords)
        print("ArrLen: ", arr_len)

        read_bytes = super().decode_msg(arrBytes, pos)
        total_bytes = read_bytes
        pos += read_bytes

        read_bytes = self.thpc.decode(arrBytes, pos)
        total_bytes += read_bytes
        pos += read_bytes

        total_bytes += self.acc.decode(arrBytes, arr_len, pos)
        self.len_data = size

        return total_bytes
        
    # Override
    def get_protocol_data(self) -> dict:
        """
            Entrega la data del protocolo 4 como dict
        """
        # Batt sensor
        data = super().get_protocol_data()

        # Protocolo 4 data
        # THPC sensor
        temp = self.thpc.get_temp()
        press = self.thpc.get_pres()
        hum = self.thpc.get_hum()
        co = self.thpc.get_co2()

        # Accel Sensor
        acc_x = self.acc.get_acc_x()
        acc_y = self.acc.get_acc_y()
        acc_z = self.acc.get_acc_z()

        data["temp"] = temp
        data["press"] = press
        data["hum"] = hum
        data["co"] = co

        data["acc_x"] = acc_x
        data["acc_y"] = acc_y
        data["acc_z"] = acc_z

        return data