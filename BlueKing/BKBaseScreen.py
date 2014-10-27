# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import os,sys
from PyQt4.QtGui import *
from PyQt4 import *

class BKBaseScreen(QWidget):

    def __init__(self):
        super(BKBaseScreen).__init__()
        self.setGeometry(0,0,320,240)
        self.setStyleSheet("border:0px;")
        self._scene = QGraphicsScene()
        self._scene.setSceneRect(0,0,320,240)
        self.setScene(self._scene)

        self.inicializarUI()

    def addWidget(self, widget):
        self._scene.addWidget(widget)

    def inicializarUI(self):
        raise NotImplementedError