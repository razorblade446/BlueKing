# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import string, time, random, lightblue
from PyQt4 import QtCore


class BKOBDLectura(QtCore.QThread):

    def __init__(self, bt_address):
        super(BKOBDLectura, self).__init__()

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
                self.obdSocket = lightblue.socket(lightblue.RFCOMM)
                self.obdSocket.connect((self.bt_address, 1))
                print "Sock..."
                break
            except lightblue.BluetoothError as error:
                self.obdSocket.close()
                print "No se pudo conectar: ", error, " reintentando en 10 segundos..."
                time.sleep(10)

    def run(self):

        if self.bt_address != "testing":
            print "Inicialización de Bluetooth..."
            self.conectar()
            self.sendSocket("ATZ")
            print "Respuesta de ATZ: %s" % self.leerSocket()
            self.sendSocket("ATE0")
            print "Respuesta de ATE0: %s" % self.leerSocket()
            self.sendSocket("ATL0")
            print "Respuesta de ATL0: %s" % self.leerSocket()
            self.sendSocket("ATH0")
            print "Respuesta de ATH0: %s" % self.leerSocket()
            self.sendSocket("ATBRD45")
            print "Respuesta de ATBRD45: %s" % self.leerSocket()

        velocidad = 0
        rpm = 700

        while self.corriendo == True:
            # Generar datos para cada lectura y activar slots...

            try:

                if self.bt_address != "testing":

                    self.sendSocket("010C")
                    lectura = self.interpretarResultado(self.leerSocket())
                    rpm = eval("0x" + lectura, {}, {})

                    self.sendSocket("010D")
                    lectura = self.interpretarResultado(self.leerSocket())
                    velocidad = eval("0x" + lectura, {}, {})

                    self.sendSocket("0105")
                    lectura = self.interpretarResultado(self.leerSocket())
                    engTemp = eval("0x" + lectura, {}, {}) - 40

                # Dato de RPM

                else:
                    rpm = random.randint(0,6000)
                    velocidad = random.randint(0, 200)
                    engTemp = random.randint(0, 120)

            except lightblue.BluetoothError as error:
                self.obdSocket.close()
                print "Conexión perdida, reintentanto conexion..."
                self.conectar()

            # LLamar los slots
            self.emit(self.senal, {'velocidad': velocidad, 'rpm': rpm, 'engTemp': engTemp})

            #time.sleep(0.01)

        self.terminate()