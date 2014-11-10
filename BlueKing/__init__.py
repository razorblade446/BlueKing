# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import sys, ConfigParser
#import BKSensorProximidad
from BlueKing.BKReversaScreen import BKReversaScreen
from BlueKing.BKHudScreen import BKHudScreen
from PyQt4 import Qt

class BlueKing(Qt.QApplication):

    bt_address = ""

    def __init__(self, args):
        Qt.QApplication.__init__(self,args)

        # Usar la pantalla de Reversa
        self.base = BKHudScreen()
        self.exec_()

def main():
    app = BlueKing(sys.argv)

sys.modules[__name__] = main()