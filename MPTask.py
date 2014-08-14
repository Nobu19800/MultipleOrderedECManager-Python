import threading
import time

import OpenRTM_aist

from PyQt4 import QtCore, QtGui
from MainWindow import MainWindow


class MPComp:
    def __init__(self):
	self.comp = None
	self.I = 0
	self.J = 0
	self.K = 0

class MPTask(OpenRTM_aist.Task):
    def __init__(self, c):
        OpenRTM_aist.Task.__init__(self)
        self.m_ec = c
        self.m_comp = []
    def addComp(self, c, I, J, K):
        self.mc = MPComp()
        self.mc.comp = c
        self.mc.I = I
        self.mc.J = J
        self.mc.K = K
        self.m_comp.append(self.mc)
    def svc(self):
        if len(self.m_ec.rs) > self.m_ec.r_num:
            for i in range(0, len(self.m_comp)):
                self.m_ec.rs[self.m_ec.r_num].rs[self.m_comp[i].I].SR[self.m_comp[i].J][self.m_comp[i].K].s = 1
		self.m_ec.workerComp(self.m_comp[i].comp)
		self.m_ec.rs[self.m_ec.r_num].rs[self.m_comp[i].I].SR[self.m_comp[i].J][self.m_comp[i].K].s = 0

        return 0


    
class GUITask(OpenRTM_aist.Task):
    app_flag = False
    def __init__(self, ec):
        OpenRTM_aist.Task.__init__(self)
        self.m_ec = ec

    def svc(self):
        if GUITask.app_flag == False:
            GUITask.app_flag = True
            guard = OpenRTM_aist.ScopedLock(self.m_ec._mutex_del)

            app = QtGui.QApplication([""])
            mainWin = MainWindow(self.m_ec)
            mainWin.show()
            
            del guard

            app.exec_()
        else:
            pass

        return 0
    
    def updateRTC(self):
        pass





