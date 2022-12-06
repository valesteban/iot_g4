class Header:
    bytes_size:int = 12

    def __init__(self, id=0, mac=0, t_layer=0, protocol=0, len_msg=0) -> None:
        self.id: int = id
        self.mac: str = mac
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
        
        mac_int = idmac & mask
        # store mac as hex string
        mac_raw_hex_str = mac_int.to_bytes(6,"little").hex()
        self.mac = ":".join([mac_raw_hex_str[i:i+2] for i in range(0,12,2)])
        

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

    # GETTERS
    def get_device_id(self) -> int:
        """
            Entrega la id del dispositivo
        """
        return self.id

    def get_mac(self) -> str:
        """
            Entrega la mac del header
        """
        return self.mac

    def get_transport_layer(self) -> int:
        """
            Entrega el transport layer 
        """
        return self.t_layer

    def get_protocol_id(self) -> int:
        """
            Entrega la id del protocolo
        """
        return self.protocol

    def get_message_length(self) -> int:
        """
            Entrega el largo del mensaje
        """
        return self.len_msg

    # CHECK DATA INTEGRITY
    def check_t_layer(self) -> tuple[bool,str,int]:
        attr_name = "t_layer"
        attr_value =  getattr(self, attr_name)
        integrity = attr_value == 0 or attr_value == 1
        return integrity, attr_name, attr_value

    def check_protocol(self) -> tuple[bool,str,int]:
        attr_name = "t_layer"
        attr_value =  getattr(self, attr_name)
        integrity = attr_value in range(0,5)
        return integrity, attr_name, attr_value