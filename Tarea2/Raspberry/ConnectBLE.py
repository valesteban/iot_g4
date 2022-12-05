from findAddresses import findAddresses
import pygatt
import time
import pyqtgraph as pg
import logging
import ipaddress

#pyuic5 ejemplo_tarea2.ui -o ex.py

import struct
from db import DB
#from main_server import Raspberry


class GUIController:
    def __init__(self, gui_obj):
        #self.raspberry = raspberry
        # TODO:
        # Descomentar Ui
        #self.ui = Ui_Dialog()
        #self.parent = parent

        self.gui_obj = gui_obj
        
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

        self.gui_obj.notify_end_find()

        self.macs = adrs[1]
        self.UUIDs = adrs[2]

        for i in range(len(self.macs)):
            self.gui_obj.notify_esp_found(self.UUIDs[i], self.macs[i])

        # TODO: UI
        #self.ui.selec_7.clear()
        #self.ui.selec_7.addItems(adrs[0])
        #print()

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
        # envía una configuración indicada por BLE al dispositivo conectado
        ESPconf = str(self.get_DB_ConfigParams())
        print("CONFIGURACION A ENVIAR:")
        print(ESPconf)

        # Enviar la configuracion como formato ipv4
        ESPconf = list(ESPconf)
        ESPconf[11] = str(ipaddress.IPv4Address(ESPconf[11]))
        ESPconf = tuple(ESPconf)


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
                print(characteristics)
                # La siguiente linea es para escribir en la caracteristica de UUID list(characteristics)[4], puede hardcodear si
                # sabe la UUID de la caracteristica a escribir, este misma funcion para leer es tan solo char_read
                # Recomiendo leer acerca del sistema de Subscribe para recibir notificaciones del cambio u otros
                device.char_write(list(characteristics)[4], pack)   #hay q poner el uid
                print("Se escribio el paquete")
                qty = 100
                #en caso de read siempre hay que ponerle un id para tomar el paquete
                #en caso de write hay que poner el uid y el apquete que queremos enviar uid -> list(characteristics)[4] 
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
        self.raspberry.actualizarStatus()
                
    
if __name__ == "__main__":
    """
    controller.actualizarMacs()
    """
    controller = GUIController()
    controller.actualizarMacs()
    controller.configSetup()
    
