# vim: set fileencoding=UTF-8 :
__author__ = 'fredericpena'

import sys
#import BKSensorProximidad
from BlueKing.BKReversaScreen import BKReversaScreen
from PyQt4 import Qt

class BlueKing(Qt.QApplication):
    def __init__(self, args):
        Qt.QApplication.__init__(self,args)

        # Usar la pantalla de Reversa
        self.base = BKReversaScreen()

        self.exec_()

def main():
    app = BlueKing(sys.argv)

sys.modules[__name__] = main()