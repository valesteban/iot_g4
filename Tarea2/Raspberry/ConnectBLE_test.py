from findAddresses import findAddresses
import pygatt
import time
import pyqtgraph as pg
import logging
import ipaddress

#pyuic5 ejemplo_tarea2.ui -o ex.py

from db import DB
import utils


class GUIController:
    def __init__(self, raspberry):
        # Atributo raspberry para notificar cualquier cambio
        self.raspberry = raspberry

        # TODO:
        # Descomentar Ui
        #self.ui = Ui_Dialog()
        #self.parent = parent

        
        self.macs = []
        self.UUIDs = []
        self.servers = []
        self.plot = None
        self.grph = None
        self.macindx = 0

        self.adapter = pygatt.GATTToolBackend() ##pygatt
                
    def actualizarMacs(self):
        """
            Busca la MAC de la ESP32 y la guarda
        """
        print("buscanding")
        # actualiza la lista de dispositivos con bluetooth disponibles
        adrs = findAddresses()

        if adrs == [[], [], []]:
            raise Exception("GUIController: No se encontraron direcciones MACs de ESP")

        self.macs = adrs[1]
        self.UUIDs = adrs[2]



        # TODO: UI
        #self.ui.selec_7.clear()
        #self.ui.selec_7.addItems(adrs[0])
        #print()
        print(f"GUIController: MACs ESP encontradas y seteadas: {self.macs}")

    def conectarMac(self):
        # se conecta mediante BLE a un dispostivo disponible
        #indx = self.ui.selec_7.currentIndex()
        #FIXME
        indx = 0
        self.macindx = indx
        ##pygatt
        logging.basicConfig()
        logging.getLogger('pygatt').setLevel(logging.DEBUG)
        qty = 0
        while(qty<100):
            try:
                self.adapter.start()
                device = self.adapter.connect(self.macs[indx],timeout=2.0)
                print('Se conecto!')
                # La siguiente linea es para ver todas las caracteristicas disponibles
                characteristics = device.discover_characteristics()
                for i in characteristics.keys():
                    print('Caracteristicas: '+str(i))#list(characteristics.keys())))
                time.sleep(1)
                qty = 100
            except pygatt.exceptions.NotConnectedError:
                qty += 1
                print("Se han fallado: {qty} intentos" )
                print("Not connected")
                time.sleep(1)
            finally:
                self.adapter.stop()
        print("Termino de test de conexión")

    def get_DB_ConfigParams(self):
        """
            Obtiene la Configuracion
        """
        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
        return db.get_all_config()[0]
    
    def configSetup(self):
        """
            Inicia la configuracion BLE para enviar la configuracion a la ESP32
        """

        # FIXME
        CONFIGURACION = (3,20,0,400,16,200,4,420,5010,5011,"192.168.28.1","iot4","12345678")
        db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
        db.change_config(utils.parse_config(CONFIGURACION))


        # envía una configuración indicada por BLE al dispositivo conectado
        print("GUIController: Obtengo la configuracion de la DB")
        ESPconf_db = self.get_DB_ConfigParams() # Configuracion a guardar

        # Enviar la configuracion como formato ipv4
        ESPconf = list(ESPconf_db)
        print(ESPconf)
        ESPconf[10] = str(ipaddress.IPv4Address(ESPconf[10]))
        ESPconf = tuple(ESPconf)
        print("GUIController: CONFIGURACION A ENVIAR:")
        print(ESPconf)

        ESPconf = str(ESPconf)
        pack = ESPconf.encode()
        print("El largo del paquete es:" + str(len(pack)))
        qty=0
        while qty<100:
            try:
                self.adapter.start()
                device = self.adapter.connect(self.macs[self.macindx], timeout=2.0) #para emparejar  los dispositivos BLE ()
                device.exchange_mtu(80)
                print(f'Se conecto!')
                characteristics = device.discover_characteristics().keys()
                # La siguiente linea es para escribir en la caracteristica de UUID list(characteristics)[4], puede hardcodear si
                # sabe la UUID de la caracteristica a escribir, este misma funcion para leer es tan solo char_read
                # Recomiendo leer acerca del sistema de Subscribe para recibir notificaciones del cambio u otros
                device.char_write(list(characteristics)[4], pack)   #hay q poner el uid
                print("Se escribio el paquete")
                qty = 100
                #en caso de read siempre hay que ponerle un id para tomar el paquete
                #en caso de write hay que poner el uid y el apquete que queremos enviar uid -> list(characteristics)[4] 

                # ACTUALIZO LA CONFIGURACION DE LA RASPBERRY
                print("GUIController: Seteando configuracion a la raspberry")
                self.raspberry.setConfiguracion(ESPconf_db)
            except pygatt.exceptions.NotConnectedError:
                qty += 1
                print(f"Se han fallado: {qty} intentos" )
                print("Not connected")
                time.sleep(1)
            finally:
                self.adapter.stop()

    def notificarCambio(self):
        """
            Notifica un cambio de estado a la Raspberry
        """
        self.raspberry.actualizarConfiguracion()
                
    
if __name__ == "__main__":
    """
    controller.actualizarMacs()
    """
    controller = GUIController()
    controller.actualizarMacs()
    controller.configSetup()
    
