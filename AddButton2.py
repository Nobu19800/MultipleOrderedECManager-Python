from PyQt4 import QtCore, QtGui
from ExComp import CompLayout

class AddButton2(QtGui.QWidget):
    clicked = QtCore.pyqtSignal("CompLayout")
    def __init__(self, text, parent=None):
        super(AddButton2, self).__init__(parent)
        
        self.Cl = None
        self.PB = QtGui.QPushButton(text)
        self.mainLayout = QtGui.QVBoxLayout()
        
        #connect(PB, SIGNAL(clicked()),
        #    this, SLOT(clickedSlot()))

        self.PB.clicked.connect(self.clickedSlot)

        self.mainLayout.addWidget(self.PB)

        self.setLayout(self.mainLayout)

    def clickedSlot(self):
        print 1
        self.clicked.emit(self.Cl)
