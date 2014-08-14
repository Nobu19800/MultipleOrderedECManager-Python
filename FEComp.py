# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class FEComp(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FEComp, self).__init__(parent)
        self.ECS = []
        self.CL = QtGui.QVBoxLayout()
        
        self.setLayout(self.CL)

        
