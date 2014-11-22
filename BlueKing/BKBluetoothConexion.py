# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import time, bluetooth, itertools
from bluetooth import RFCOMM, BluetoothSocket, BluetoothError
from PyQt4.QtCore import QThread, SIGNAL

class BKBluetoothConexion(QThread):

    def __init__(self, btAddress):
        super(BKBluetoothConexion, self).__init__()
        self.btAddress = "NO"
        self.senal = SIGNAL("BKBluetoothStatusSignal")
        self.corriendo = False
        self.socket = BluetoothSocket(RFCOMM)

    def iniciar(self):
        self.corriendo = True
        self.start()

    def detener(self):

        self.corriendo = False
        while self.isRunning():
            continue

    def buscarObd(self):

        # Buscamos el servicio Serial
        try:
            self.emit(self.senal,{'status':'buscando'})
            for svc in itertools.chain(bluetooth.find_service(name='SPP'), bluetooth.find_service(name='Serial Port')):
                print "Servicio: %s " % svc['name']
                self.btAddress = svc['host']
                print "Usando servicios en %s" % self.btAddress
                break
        except Exception as e:
            print "Error en búsqueda: %s" % e.message
            self.btAddress = "NO"


    def sendSocket(self, comando):
        self.socket.send("%s\r" % comando)

    def leerSocket(self):
        buffer = ""

        if self.socket:
            repeat_count = 0
            while 1:
                c = self.socket.recv(1)
                if len(c) == 0:
                    if (repeat_count == 5):
                        break
                    print "No se obtuvo nada\n"
                    repeat_count = repeat_count + 1
                    continue

                if c == '\r':
                    continue

                if c == ">":
                    break

                if buffer != "" or c != ">":  # if something is in buffer, add everything
                    buffer = buffer + c

        return buffer


    def conectar(self):

        # Backoff Exponencial
        espera = 20

        while self.btAddress == "NO" or self.btAddress == "":
            self.buscarObd()

        while self.corriendo:
            try:
                print "ADDR: " + self.btAddress
                self.socket = BluetoothSocket(RFCOMM)
                res = self.socket.connect((self.btAddress, 1))

                print "Inicialización de Bluetooth..."
                self.sendSocket("ATZ")
                print "Respuesta de ATZ: %s" % self.leerSocket()
                self.sendSocket("ATE0")
                print "Respuesta de ATE0: %s" % self.leerSocket()
                self.sendSocket("ATL0")
                print "Respuesta de ATL0: %s" % self.leerSocket()
                self.sendSocket("ATH0")
                print "Respuesta de ATH0: %s" % self.leerSocket()
                self.sendSocket("ATAT2")
                print "Respuesta de ATAT2: %s" % self.leerSocket()
                break
            except BluetoothError as error:
                print "No se pudo conectar: " + error.message
                print "Reintentando conexión (Backoff Exponencial " + `espera` + " ms)"
                self.emit(self.senal, {'status':'NO'})
                time.sleep(float(espera / 1000))
                espera *= 2
                if espera > 10000:
                    espera = 20

        # Si sale del ciclo, se debe emitir la señal con el socket Bluetooth si no se ha abortado primero
        if self.corriendo:
            self.emit(self.senal, {'status':'OK', 'socket': self.socket.dup()})

    def run(self):

        while self.corriendo:
            try:
                gaddr = self.socket.getsockname()
                if gaddr[0] == "00:00:00:00:00:00":
                    raise Exception("Bluetooth not bound")
                time.sleep(5)
            except Exception as error:
                print "Desconexion ... reintentanto conexión de nuevo (" + error.message + ")"
                self.conectar()


        self.emit(self.senal,{'status':'cierre'})
        self.socket.close()
        self.terminate()