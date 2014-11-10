# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import math
from PyQt4.QtGui import QWidget, QPainter, QColor, QConicalGradient, QGradient, QPen
from PyQt4 import QtCore

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

    def setValor(self, val):
        self.valor = val
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

        gradiente = QConicalGradient()
        gradiente.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradiente.setAngle(60)
        gradiente.setColorAt(0, rojo)
        gradiente.setColorAt(0.25, amarillo)
        gradiente.setColorAt(0.50, verde)

        lapizTrazo = QPen()
        lapizTrazo.setStyle(QtCore.Qt.SolidLine)
        lapizTrazo.setWidth(self.anchoLinea)
        lapizTrazo.setBrush(verde)

        porcentaje = self.valor / float(self.maxValor - self.minValor)
        span = math.floor((self.finishAngle - self.startAngle) * porcentaje)

        painter.setPen(lapizTrazo)
        painter.drawArc(nuevoRect, self.startAngle * 16, span * 16)

        super(BKGauge, self).paintEvent(event)