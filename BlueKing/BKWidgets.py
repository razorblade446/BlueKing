# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import math, time
from PyQt4.QtGui import QWidget, QPainter, QColor, QPen
from PyQt4 import QtCore
from PyQt4.QtCore import QThread

class UpdateTimer(QThread):
        def __init__(self):
            QThread.__init__(self)
            self.corriendo = False
            self.senal = QtCore.SIGNAL("update_frame")

        def iniciarTimer(self):
            self.corriendo = True
            self.start()

        def terminarTimer(self):
            self.corriendo = False
            while self.isRunning():
                continue

        def run(self):
            while self.corriendo:
                self.emit(self.senal)
                time.sleep(0.1)
            self.terminate()

class BKGauge(QWidget):

    def __init__(self):
        super(BKGauge, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.startAngle = 210       # Angulo inicial del indicador
        self.finishAngle = 60       # Angulo final del indicador
        self.maxValor = 200         # Valor Maximo
        self.minValor = 0           # Valor Minimo
        self.valor = 0              # Valor
        self.colorDial = "00FF00"   # Color Dial
        self.anchoLinea = 20

        # Hilo de refresco
        self.updateTimer = UpdateTimer()
        #self.updateTimer.connect(self.updateTimer, self.updateTimer.senal, self.update)
        #self.updateTimer.iniciarTimer()

    def destroy(self, bool_destroyWindow=True, bool_destroySubWindows=True):
        if bool_destroyWindow or bool_destroySubWindows:
            self.updateTimer.terminarTimer()

    def setValor(self, val):
        self.valor = val
        if self.valor > self.maxValor:
            self.maxValor = self.valor
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)

        tamanio = self.geometry().size()

        nuevoRect = QtCore.QRect(math.floor(self.anchoLinea / 2), math.floor(self.anchoLinea / 2), tamanio.width() - self.anchoLinea, tamanio.height() - self.anchoLinea)
        verde = QColor()
        verde.setNamedColor("#00FF00")

        amarillo = QColor()
        amarillo.setNamedColor("#FFFF00")

        rojo = QColor()
        rojo.setNamedColor("#FF0000")

        colorSeleccionado = QColor()
        colorSeleccionado.setNamedColor(self.colorDial)

        lapizTrazo = QPen()
        lapizTrazo.setStyle(QtCore.Qt.SolidLine)
        lapizTrazo.setWidth(self.anchoLinea)
        lapizTrazo.setBrush(colorSeleccionado)
        lapizTrazo.setCapStyle(QtCore.Qt.FlatCap)

        porcentaje = self.valor / float(self.maxValor - self.minValor)
        span = math.floor((self.finishAngle - self.startAngle) * porcentaje)

        painter.setPen(lapizTrazo)

        painter.drawArc(nuevoRect, self.startAngle * 16, span * 16)

        super(BKGauge, self).paintEvent(event)