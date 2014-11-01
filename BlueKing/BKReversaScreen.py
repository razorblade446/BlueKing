__author__ = 'fredericpena'

import time
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot
from BKSensorProximidadDummie import BKSensorProximidadDummie

class BKReversaScreen(QWidget):

    def __init__(self):
        super(BKReversaScreen,self).__init__()
        self.sensorActivo = 0
        self.inicializarUI()
        self.distancias=[]

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
            self.sensor1 = BKSensorProximidad(0, 15, 14)
            self.sensor1.connect(self.sensor1, QtCore.SIGNAL('distancia_sensor'), self.mostrarMedida)
            self.sensor1.start()
            self.distancias[0] = 0.0
            self.sensor2 = BKSensorProximidad(1, 23, 22)
            self.sensor2.connect(self.sensor2, QtCore.SIGNAL('distancia_sensor'), self.mostrarMedida)
            self.sensor2.start()
            self.distancias[1] = 0.0
            self.sensor3 = BKSensorProximidad(2, 25, 24)
            self.sensor3.connect(self.sensor2, QtCore.SIGNAL('distancia_sensor'), self.mostrarMedida)
            self.sensor3.start()
            self.distancias[2] = 0.0
            self.sensorActivo = 1
        else:
            # Detener sensores
            self.sensor1.stop()
            #self.sensor2.stop()
            #self.sensor3.stop()

    def mostrarMedida(self, sensor, numero):
        # Calcular la menor distancia.
        self.distancias[sensor] = numero
        tnumero = 1000.0
        for n in range(len(self.distancias)):
            if self.distancias[n] < tnumero:
                tnumero = self.distancias[n]

        if tnumero == 1000.0:
            self.distlabel.setText("---")
        else:
            self.distlabel.setText(`numero`)