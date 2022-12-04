import re
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, QMetaType


class WifiProperties(QObject):
    host_changed = pyqtSignal(str)
    tcp_changed = pyqtSignal(int)
    udp_changed = pyqtSignal(int)
    ssid_changed = pyqtSignal(str)
    passwd_changed = pyqtSignal(str)

    host_invalidated = pyqtSignal()
    tcp_invalidated = pyqtSignal()
    udp_invalidated = pyqtSignal()
    ssid_invalidated = pyqtSignal()
    passwd_invalidated = pyqtSignal()

    host_re = r"^"+"[.]".join([r"(?P<byte_"+str(i)+">25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})" for i in range(1,5)]) + r"$"
    attrs = ["host_ipv4", "port_tcp", "port_udp", "ssid", "passwd"]

    def __init__(self):
        QObject.__init__(self)
        self._host_ipv4 = "255.255.255.255"
        self._port_tcp = 5000
        self._port_udp = 5000
        self._ssid: QMetaType.Type.QString = ""
        self._passwd: QMetaType.Type.QString = ""

    #Host IP
    def read_host_ipv4(self):
        return self._host_ipv4

    def set_host_ipv4(self, new_ip):
        if new_ip != self._host_ipv4:
            if self.validate_host_ipv4(new_ip):
                self._host_ipv4 = new_ip
                self.host_changed.emit(new_ip)

    def validate_host_ipv4(self, new_ip):
        m = re.match(self.host_re, new_ip)
        if m is not None:
            return True
        else:
            self.host_invalidated.emit()
            return False

    def reset_host_ipv4(self):
        self._host_ipv4 = "255.255.255.255"

    

    #TCP
    def read_port_tcp(self):
        return self._port_tcp

    def set_port_tcp(self, new_port):
        if new_port != self._port_tcp:
            if self.validate_port_tcp(new_port):
                self._port_tcp = new_port
                self.tcp_changed.emit(new_port)

    def validate_port_tcp(self, new_port):
        if new_port < 2**16:
            return True
        else:
            self.tcp_invalidated.emit()
            return False

    def reset_port_tcp(self):
        self._port_tcp = 5000

    

    #UDP
    def read_port_udp(self):
        return self._port_udp

    def set_port_udp(self, new_port):
        if new_port != self._port_udp:
            if self.validate_port_udp(new_port):
                self._port_udp = new_port
                self.udp_changed.emit(new_port)

    def validate_port_udp(self, new_port):
        if new_port < 2**16:
            return True
        else:
            self.udp_invalidated.emit()
            return False

    def reset_port_udp(self):
        self._port_udp = 5000

    

    #SSID
    def read_ssid(self):
        return self._ssid

    def set_ssid(self, new_ssid):
        if new_ssid != self._ssid:
            if self.validate_ssid(new_ssid):
                self._ssid = new_ssid
                self.ssid_changed.emit(new_ssid)

    def validate_ssid(self, new_ssid):
        if new_ssid != "":
            return True
        else:
            self.ssid_invalidated.emit()
            return False

    def reset_ssid(self):
        self._ssid = "dummy"

    #Passwd
    def read_passwd(self):
        return self._passwd

    def set_passwd(self, new_passwd):
        if new_passwd != self._passwd:
            if self.validate_passwd(new_passwd):
                self._passwd = new_passwd
                self.passwd_changed.emit(new_passwd)

    def validate_passwd(self, new_passwd):
        if new_passwd != "":
            return True
        else:
            self.passwd_invalidated.emit()
            return False

    def reset_passwd(self):
        self._passwd = "dummy"

    # utility functions
    def validate_all(self, *vals):
        result = True
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            mid_result = getattr(self, "validate_"+attr)(vals[i])
            result = result and mid_result
        return result

    def set_all(self, *new_vals):
        assert len(new_vals) == len(self.attrs)
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            getattr(self, "set_"+ attr)(new_vals[i])
        
    def get_all(self):
        return [getattr(self, attr) for attr in self.attrs]

    host_ipv4 = pyqtProperty(str, read_host_ipv4, set_host_ipv4, notify=host_changed)
    port_tcp = pyqtProperty(int, read_port_tcp, set_port_tcp, notify=tcp_changed)
    port_udp = pyqtProperty(int, read_port_udp, set_port_udp, notify=udp_changed)
    ssid = pyqtProperty(str, read_ssid, set_ssid, notify=ssid_changed)
    passwd = pyqtProperty(str, read_passwd, set_passwd, notify=passwd_changed)


class ConfigProperties(QObject):
    status_conf_changed = pyqtSignal(int)
    protocol_conf_changed = pyqtSignal(int)
    discontinuous_time_changed = pyqtSignal(int)
    acc_sampling_changed = pyqtSignal(int)
    acc_sensibility_changed = pyqtSignal(int)
    gyro_sensibility_changed = pyqtSignal(int)
    bme688_sampling_changed = pyqtSignal(int)

    status_conf_invalidated = pyqtSignal()
    protocol_conf_invalidated = pyqtSignal()
    discontinuous_time_invalidated = pyqtSignal()
    acc_sampling_invalidated = pyqtSignal()
    acc_sensibility_invalidated = pyqtSignal()
    gyro_sensibility_invalidated = pyqtSignal()
    bme688_sampling_invalidated = pyqtSignal()

    statuses_conf = { 21, 22, 23, 30, 31 }
    protocols_conf = { i for i in range(1,6) }
    acc_samplings = { 10, 100, 400, 1000 } 
    acc_sensibilities = { 2,4,8,16 }
    gyro_sensibilities = { 200, 250, 500 }
    bme_samplings = { 1,2,3,4 }

    attrs = ["status_conf", "protocol_conf", "discontinuous_time", "acc_sampling", "acc_sensibility", "gyro_sensibility", "bme688_sampling"]

    def __init__(self):
        QObject.__init__(self)
        self._status_conf = 21
        self._protocol_conf = 1
        self._discontinuous_time = 60
        self._acc_sampling = 10
        self._acc_sensibility = 2
        self._gyro_sensibility = 200
        self._bme688_sampling = 1

    # status_conf
    def read_status_conf(self):
        return self._status_conf

    def set_status_conf(self, new_status):
        if self._status_conf != new_status:
            if self.validate_status_conf(new_status):
                self._status_conf = new_status
                self.status_conf_changed.emit(new_status)

    def validate_status_conf(self, new_status):
        if new_status in self.statuses_conf:
            return True
        else:
            self.status_conf_invalidated.emit()
            return False

    def reset_status_conf(self):
        self._status_conf = 21

    # protocol_conf
    def read_protocol_conf(self):
        return self._protocol_conf

    def set_protocol_conf(self, new_protocol):
        if self._protocol_conf != new_protocol:
            if self.validate_protocol_conf(new_protocol):
                self._protocol_conf = new_protocol
                self.protocol_conf_changed.emit(new_protocol)

    def validate_protocol_conf(self, new_protocol):
        if new_protocol in self.protocols_conf:
            return True
        else:
            self.protocol_conf_invalidated.emit()
            return False

    def reset_protocol_conf(self):
        self._protocol_conf = 1

    # discontinuous time
    def read_discontinuous_time(self):
        return self._discontinuous_time

    def set_discontinuous_time(self, new_time):
        if self._discontinuous_time != new_time:
            if self.validate_discontinuous_time(new_time):
                self._discontinuous_time = new_time
                self.discontinuous_time_changed.emit(new_time)

    def validate_discontinuous_time(self, new_time):
        if new_time >= 10:
            return True
        else:
            self.discontinuous_time_invalidated.emit()
            return False

    def reset_discontinuous_time(self):
        self._discontinuous_time = 60

    #acc_sampling
    def read_acc_sampling(self):
        return self._acc_sampling

    def set_acc_sampling(self, new_sample):
        if self._acc_sampling != new_sample:
            if self.validate_acc_sampling(new_sample):
                self._acc_sampling = new_sample
                self.acc_sampling_changed.emit(new_sample)

    def validate_acc_sampling(self, new_sample):
        if new_sample in self.acc_samplings:
            return True
        else:
            self.acc_sampling_invalidated.emit()
            return False

    def reset_acc_sampling(self):
        self._acc_sampling = 10


    #acc_sensibility
    def read_acc_sensibility(self):
        return self._acc_sensibility

    def set_acc_sensibility(self, new_sensibility):
        if self._acc_sensibility != new_sensibility:
            if self.validate_acc_sensibility(new_sensibility):
                self._acc_sensibility = new_sensibility
                self.acc_sensibility_changed.emit(new_sensibility)

    def validate_acc_sensibility(self, new_sensibility):
        if new_sensibility in self.acc_sensibilities:
            return True
        else:
            self.acc_sensibility_invalidated.emit()
            return False

    def reset_acc_sensibility(self):
        self._acc_sensibility = 2


    #gyro_sensibility
    def read_gyro_sensibility(self):
        return self._gyro_sensibility

    def set_gyro_sensibility(self, new_sensibility):
        if self._gyro_sensibility != new_sensibility:
            if self.validate_gyro_sensibility(new_sensibility):
                self._gyro_sensibility = new_sensibility
                self.gyro_sensibility_changed.emit(new_sensibility)

    def validate_gyro_sensibility(self, new_sensibility):
        if new_sensibility in self.gyro_sensibilities:
            return True
        else:
            self.gyro_sensibility_invalidated.emit()
            return False

    def reset_gyro_sensibility(self):
        self._gyro_sensibility = 200


    #gyro_sensibility
    def read_bme688_sampling(self):
        return self._bme688_sampling

    def set_bme688_sampling(self, new_sample):
        if self._bme688_sampling != new_sample:
            if self.validate_bme688_sampling(new_sample):
                self._bme688_sampling = new_sample
                self.bme688_sampling_changed.emit(new_sample)

    def validate_bme688_sampling(self, new_sample):
        if new_sample in self.bme_samplings:
            return True
        else:
            self.bme688_sampling_invalidated.emit()
            return False

    def reset_bme688_sampling(self):
        self._bme688_sampling = 1

    # utility functions
    def validate_all(self, *vals):
        result = True
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            mid_result = getattr(self, "validate_"+attr)(vals[i])
            result = result and mid_result
        return result

    def set_all(self, *new_vals):
        assert len(new_vals) == len(self.attrs)
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            getattr(self, "set_"+ attr)(new_vals[i])
        
    def get_all(self):
        return [getattr(self, attr) for attr in self.attrs]

    status_conf = pyqtProperty(int, read_status_conf, set_status_conf, freset=reset_status_conf, notify=status_conf_changed)
    protocol_conf = pyqtProperty(int, read_protocol_conf, set_protocol_conf, freset=reset_protocol_conf, notify=protocol_conf_changed)
    discontinuous_time = pyqtProperty(int, read_discontinuous_time, set_discontinuous_time, freset=reset_discontinuous_time, notify=discontinuous_time_changed)
    acc_sampling = pyqtProperty(int, read_acc_sampling, set_acc_sampling, freset=reset_acc_sampling, notify=acc_sampling_changed)
    acc_sensibility = pyqtProperty(int, read_acc_sensibility, set_acc_sensibility, freset=reset_acc_sensibility, notify=acc_sensibility_changed)
    gyro_sensibility = pyqtProperty(int, read_gyro_sensibility, set_gyro_sensibility, freset=reset_gyro_sensibility, notify=gyro_sensibility_changed)
    bme688_sampling = pyqtProperty(int, read_bme688_sampling, set_bme688_sampling, freset=reset_bme688_sampling, notify=bme688_sampling_changed)

