# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

from lightblue import socket, RFCOMM
from PyQt4.QtCore import QThread, SIGNAL


class BKBluetoothConexion(QThread):

    def __init__(self, btAddress):
        super(BKBluetoothConexion, self).__init__()
        self.btAddress = btAddress
        self.senal = SIGNAL("BKBluetoothStatusSignal")
        self.corriendo = False
        self.socket = socket(RFCOMM)

    def iniciar(self):
        self.corriendo = True
        self.run()

    def detener(self):

        self.corriendo = False
        while self.isRunning():
            continue
        self.terminate()

    def run(self):
        pass