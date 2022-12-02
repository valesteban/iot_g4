from findAddresses import findAddresses
import pygatt
import time
import pyqtgraph as pg
import logging

#pyuic5 ejemplo_tarea2.ui -o ex.py


class GUIController:
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.macs = []
        self.UUIDs = []
        self.servers = []
        self.plot = None
        self.grph = None
        self.macindx = None

        self.adapter = pygatt.GATTToolBackend() ##pygatt
        print()
        
    def actualizarMacs(self):
        # actualiza la lista de dispositivos con bluetooth disponibles
        adrs = findAddresses()
        self.macs = adrs[1]
        self.UUIDs = adrs[2]
        self.ui.selec_7.clear()
        self.ui.selec_7.addItems(adrs[0])
        #print()

    def conectarMac(self):
        # se conecta mediante BLE a un dispostivo disponible
        indx = self.ui.selec_7.currentIndex()
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
    
    def configSetup(self):
        # envía una configuración indicada por BLE al dispositivo conectado
        ESPconf = self.getConfigParams()
        pack = ESPconf.pack()
        print("El largo del paquete es:" + str(len(pack)))
        qty=0
        while qty<100:
            try:
                self.adapter.start()
                device = self.adapter.connect(self.macs[self.macindx], timeout=2.0)
                device.exchange_mtu(80)
                print('Se conecto!')
                characteristics = device.discover_characteristics().keys()
                # La siguiente linea es para escribir en la caracteristica de UUID list(characteristics)[4], puede hardcodear si
                # sabe la UUID de la caracteristica a escribir, este misma funcion para leer es tan solo char_read
                # Recomiendo leer acerca del sistema de Subscribe para recibir notificaciones del cambio u otros
                device.char_write(list(characteristics)[4], pack)
                print("Se escribio el paquete")
                qty = 100
            except pygatt.exceptions.NotConnectedError:
                qty += 1
                print("Se han fallado: {qty} intentos" )
                print("Not connected")
                time.sleep(1)
            finally:
                self.adapter.stop()
