# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QVBoxLayout, QPixmap, QGraphicsPixmapItem, QLabel, QTransform
from BlueKing.BKOBDLectura import *
from BlueKing.BKWidgets import *
from ConfigParser import ConfigParser

class BKHudScreen(QWidget):

    def __init__(self):
        super(BKHudScreen, self).__init__()
        self.bt_address=""
        self.inicializarUI()
        self.inicializarConfig()
        self.hilo = BKOBDLectura(self.bt_address)
        self.hilo.connect(self.hilo, self.hilo.senal, self.informacion_recibida)

    def closeEvent(self, event):
        print "Cierre de ventana..."
        self.hilo.corriendo = False
        while self.hilo.isRunning():
            continue
        print "Hilo terminado!!"
        event.accept()

    def inicializarConfig(self):
        # Leer configuraciones
        config = ConfigParser()
        config.read("config.ini")
        self.bt_address = config.get('Scanner','obd_interface')

    def inicializarUI(self):
        self.setWindowTitle("BlueKing HUD")
        self.setGeometry(0,0,320,240)
        self.setAutoFillBackground(True)

        self.view = QGraphicsView()
        self.view.setStyleSheet("border: 0px;margin: 0px;background-color: #000000;")

        self.scene = QGraphicsScene(0,0,320,240)
        self.view.setScene(self.scene)

        self.baseLayout = QVBoxLayout()
        self.baseLayout.setContentsMargins(0,0,0,0)
        self.baseLayout.addWidget(self.view)

        # Decoracion

        # Etiqueta km/h
        kmLabel = QLabel("Km/h")
        kmLabel.setGeometry(250,120, 70, 25)
        kmLabel.setStyleSheet("font-size: 25px; color: #C8FF00; background: transparent;text-decoration: italic")
        self.scene.addWidget(kmLabel)

        # Etiqueta RPM
        rpmSigLabel = QLabel("R.P.M.")
        rpmSigLabel.setGeometry(250, 152, 70, 25)
        rpmSigLabel.setStyleSheet("font-size: 25px; color: #C8FF00; background: transparent;text-decoration: italic")
        self.scene.addWidget(rpmSigLabel)

        # Icono Temperatura
        thermometro = QPixmap("imagenes/termometro_amarillo.png").scaled(32,32,QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        thermometro_item = QGraphicsPixmapItem(thermometro)
        thermometro_item.setPos(167, 208)
        self.scene.addItem(thermometro_item)

        # Icono Batería
        imagenBateria = QPixmap("imagenes/battery.png").scaled(32,32,QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        imagenBateria_item = QGraphicsPixmapItem(imagenBateria)
        imagenBateria_item.setPos(80, 206)
        self.scene.addItem(imagenBateria_item)

        # Icono Bluetooth
        imagenBluetooth = QPixmap("imagenes/bluetooth.png").scaled(32,32,QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        imagenBluetooth_item = QGraphicsPixmapItem(imagenBluetooth)
        imagenBluetooth_item.setPos(4, 208)
        self.scene.addItem(imagenBluetooth_item)

        # Indicadores

        # Velocidad
        self.gaugeWidget = BKGauge()
        self.gaugeWidget.setGeometry(70,50,180,180)
        self.gaugeWidget.colorDial="#00FF00"
        self.gaugeWidget.maxValor = 250
        self.gaugeWidget.valor = 1
        self.scene.addWidget(self.gaugeWidget)

        self.velocidadLabel = QLabel("250")
        self.velocidadLabel.setGeometry(115,90,130,60)
        self.velocidadLabel.setAlignment(QtCore.Qt.AlignRight |QtCore.Qt.AlignVCenter)
        self.velocidadLabel.setStyleSheet("font-family: Blutter;font-size: 60px;color: #00FFFF; background: transparent; font-weight: bold; text-align: right;")
        self.scene.addWidget(self.velocidadLabel)

        # RPM
        self.rpmGaugeWidget = BKGauge()
        self.rpmGaugeWidget.setGeometry(60, 40, 200, 200)
        self.rpmGaugeWidget.maxValor = 25000
        self.rpmGaugeWidget.valor = 1
        self.rpmGaugeWidget.anchoLinea = 20
        self.rpmGaugeWidget.colorDial = "#FF0000"
        self.scene.addWidget(self.rpmGaugeWidget)

        self.rpmLabel = QLabel("2658")
        self.rpmLabel.setGeometry(150, 150, 95, 30)
        self.rpmLabel.setAlignment(QtCore.Qt.AlignRight |QtCore.Qt.AlignVCenter)
        self.rpmLabel.setStyleSheet("font-family: Blutter; font-size: 30px;color: #FF0009; background-color: transparent;")
        self.scene.addWidget(self.rpmLabel)

        # Temperatura Motor
        self.engTempLabel = QLabel("180")
        self.engTempLabel.setGeometry(192, 208, 48, 32)
        self.engTempLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.engTempLabel.setStyleSheet("font-family: Blutter; font-size: 20px; color: #00FF00;background-color: transparent;")
        self.scene.addWidget(self.engTempLabel)

        # Indicador de Voltaje
        self.voltajeLabel = QLabel("12.2")
        self.voltajeLabel.setGeometry(112, 208, 48, 32)
        self.voltajeLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.voltajeLabel.setStyleSheet("font-size: 20px; color: #00FF00; background-color: transparent;")
        self.scene.addWidget(self.voltajeLabel)

        # Indicador de conexion Bluetooth
        self.bluetoothLabel = QLabel("NO")
        self.bluetoothLabel.setGeometry(32, 208, 48, 32)
        self.bluetoothLabel.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bluetoothLabel.setStyleSheet("font-size: 20px; color: #00FF00; background-color: transparent;")
        self.scene.addWidget(self.bluetoothLabel)

        self.setLayout(self.baseLayout)

        transformacion = QTransform()
        transformacion.scale(1.0,-1.0)

        #self.view.setTransform(transformacion)

        self.show()

    def informacion_recibida(self, datos):

        # Velocidad
        if 'velocidad' in datos:
            self.velocidadLabel.setText(`datos['velocidad']`)
            self.gaugeWidget.setValor(datos['velocidad'])

        # RPM
        if 'rpm' in datos:
            self.rpmLabel.setText(`datos['rpm']`)
            self.rpmGaugeWidget.setValor(datos['rpm'])

        # Temperatura Motor
        if 'engTemp' in datos:
            self.engTempLabel.setText(`datos['engTemp']`)

    def mousePressEvent(self, QMouseEvent):
        if not self.hilo.corriendo:
            self.hilo.corriendo = True
            self.hilo.start()


