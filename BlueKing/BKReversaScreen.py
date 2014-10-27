__author__ = 'fredericpena'

import time
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot
from BKSensorProximidad import BKSensorProximidad

class BKReversaScreen(QWidget):

    def __init__(self):
        super(BKReversaScreen,self).__init__()
        self.sensorActivo = 0
        self.inicializarUI()

    def inicializarUI(self):
        self.setWindowTitle("BlueKing::Reversa")
        self.setGeometry(0,0,320,240)
        self.setAutoFillBackground(True)

        #QGraphicsView/Scene
        self.view = QGraphicsView()
        self.view.setStyleSheet("border: 0px;margin: 0px;background-color: #000000;")

        self.scene = QGraphicsScene(0,0,320,240)
        self.view.setScene(self.scene)

        self.baseLayout = QVBoxLayout()
        self.baseLayout.setContentsMargins(0,0,0,0)
        self.baseLayout.addWidget(self.view)

        self.distlabel = QLabel("-")
        self.distlabel.setGeometry(20, 20, 280, 200)
        self.distlabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.distlabel.setStyleSheet("color: #00FFFF;font-size: 150px;background-color: transparent;")
        self.scene.addWidget(self.distlabel)

        self.measureLabel=QLabel("metros")
        self.measureLabel.setGeometry(10,190,300,30)
        self.measureLabel.setAlignment(QtCore.Qt.AlignRight |QtCore.Qt.AlignVCenter)
        self.measureLabel.setStyleSheet("color: #FFFF00;font-size: 30px; font-weight: bold; font-style: italic;background-color: transparent;")
        self.scene.addWidget(self.measureLabel)

        self.setLayout(self.baseLayout)

        transformacion = QTransform()
        transformacion.scale(1.0,-1.0)

        #self.view.setTransform(transformacion)

        self.show()

    def mousePressEvent(self, QMouseEvent):
        if self.sensorActivo == 0:
            # Iniciar sensores de Proximidad
            self.sensor1 = BKSensorProximidad(1, 15, 14)
            self.sensor1.connect(self.sensor1, QtCore.SIGNAL('distancia_sensor'), self.mostrarMedida)
            self.sensor1.start()
            #self.sensor2 = BKSensorProximidad(2, 23, 22)
            #self.sensor2.start()
            #self.sensor3 = BKSensorProximidad(3, 25, 24)
            #self.sensor3.start()
            #self.sensorActivo = 1
        else:
            # Detener sensores
            self.sensor1.stop()
            #self.sensor2.stop()
            #self.sensor3.stop()

    @pyqtSlot(int, name='mostrarMedida')
    @pyqtSlot(int, name='distancia_sensor')
    def mostrarMedida(self, numero):
        self.distlabel.setText(`numero`)

class TestCounter(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.counter = 0

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(1000):
            time.sleep(0.03)
            self.emit(QtCore.SIGNAL('incrementarMedida'), self.counter)
            self.counter += 1
            print("cuenta: " + `self.counter`)
        self.terminate()