# vim: set fileencoding=UTF-8 :
from bluetooth.bluez import BluetoothSocket
from bluetooth._bluetooth import RFCOMM

__author__ = 'fredericpena'

import string, time, random, bluetooth
from PyQt4 import QtCore
from bluetooth import BluetoothSocket, BluetoothError


class BKOBDLectura(QtCore.QThread):

    def __init__(self):
        super(BKOBDLectura, self).__init__()

        self.corriendo = False
        self.pausada = False
        self.senal = QtCore.SIGNAL("informacion_leida")
        self.senalBluetooth = QtCore.SIGNAL("bluetooth_estado")
        self.testMode = True
        self.obdSocket = BluetoothSocket(RFCOMM)

    def setSocket(self, socket_opt):
        try:
            socket_opt.getsockname()
            self.obdSocket = socket_opt
            self.testMode = False
        except Exception as error:
            # El parametro debe ser "testing"
            self.testMode = True

    def sendSocket(self, comando):
        self.obdSocket.send("%s\r" % comando)

    def leerSocket(self):
        buffer = ""

        if self.obdSocket:
            repeat_count = 0
            while 1:
                c = self.obdSocket.recv(1)
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

                    #debug_display(self._notify_window, 3, "Get result:" + buffer)

        return buffer

    def interpretarResultado(self, code):

        # 9 seems to be the length of the shortest valid response
        if len(code) < 7:
            # raise Exception("BogusCode")
            print "código raro?" + code

        code = string.split(code, "\r")
        code = code[0]

        # remove whitespace
        code = string.split(code)
        code = string.join(code, "")

        #cables can behave differently 
        if code[:6] == "NODATA":  # there is no such sensor
            return "NODATA"

        # first 4 characters are code from ELM
        code = code[4:]
        return code

    def conectar(self):
        while True:
            try:
                self.obdSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.obdSocket.connect((self.bt_address, 1))
                print "Socket conectado..."
                break
            except bluetooth.BluetoothError as error:
                self.obdSocket.close()
                print "No se pudo conectar: ", error, " reintentando en 10 segundos..."
                time.sleep(10)

    def run(self):

        velocidad = 0
        rpm = 700
        engTemp = 0
        voltage = 0

        while self.corriendo == True:
            # Pausa del hilo
            while self.pausada and self.corriendo:
                continue

            # Generar datos para cada lectura y activar slots...
            try:

                if not self.testMode:

                    self.sendSocket("010C1")
                    lectura = self.interpretarResultado(self.leerSocket())
                    rpm = eval("0x" + lectura, {}, {}) / 4

                    self.sendSocket("010D1")
                    lectura = self.interpretarResultado(self.leerSocket())
                    velocidad = eval("0x" + lectura, {}, {}) * 1.1

                    self.sendSocket("0105")
                    lectura = self.interpretarResultado(self.leerSocket())
                    engTemp = eval("0x" + lectura, {}, {}) - 40

                else:
                    rpm = random.randint(0,6000)
                    velocidad = random.randint(0, 200)
                    engTemp = random.randint(0, 120)
                    voltage = float(random.randint(90, 135) / 10)
                    time.sleep(0.066666666666666)

            except bluetooth.BluetoothError as error:
                print "Conexión perdida, reintentanto conexion..."
                self.obdSocket.close()
                velocidad = 0
                rpm = 0
                engTemp = 0
                voltage = 0
                self.pausada = True
                self.emit(self.senalBluetooth, {'status':'perdida'})
                self.emit(self.senal, {'velocidad': 0, 'rpm': 0, 'engTemp': 0, 'voltage': 0})

            self.emit(self.senal, {'velocidad': velocidad, 'rpm': rpm, 'engTemp': engTemp, "voltage": voltage})

        self.terminate()