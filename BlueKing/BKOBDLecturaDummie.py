# vim: set fileencoding=UTF-8 :
import socket, string

__author__ = 'fredericpena'

import time, random, bluetooth
from PyQt4 import QtCore


class BKOBDLecturaDummie(QtCore.QThread):

    def __init__(self, bt_address):
        super(BKOBDLecturaDummie, self).__init__()

        self.corriendo = False
        self.senal = QtCore.SIGNAL("informacion_leida")

        self.bt_address = bt_address
        self.bt_pin = "1234"

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
                    print "Got nothing\n"
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
            print "boguscode?" + code

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
                break
            except bluetooth.btcommon.BluetoothError as error:
                self.obdSocket.close()
                print "No se pudo conectar: ", error, " reintentando en 10 segundos..."
                time.sleep(10)

    def run(self):

        self.conectar()

        self.sendSocket("ATZ")
        print "Respuesta de ATZ: %s" % self.leerSocket()
        self.sendSocket("ATE0")
        print "Respuesta de ATE0: %s" % self.leerSocket()
        self.sendSocket("ATL0")
        print "Respuesta de ATL0: %s" % self.leerSocket()

        velocidad = 0
        rpm = 700

        while self.corriendo == True:
            # Generar datos para cada lectura y activar slots...

            # Dato de RPM
            self.sendSocket("010C1")
            lectura = self.interpretarResultado(self.leerSocket())
            rpm = eval("0x" + lectura, {}, {})

            self.sendSocket("010D1")
            lectura = self.interpretarResultado(self.leerSocket())
            velocidad = eval("0x" + lectura, {}, {})

            # Dato de Temperatura motor
            engTemp = random.randint(0, 120)

            # LLamar los slots
            self.emit(self.senal, {'velocidad': velocidad, 'rpm': rpm, 'engTemp': engTemp})

            time.sleep(0.0333333)
