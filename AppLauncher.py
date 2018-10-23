
#
import sys
import os
import datetime as dt
import re
#
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit, QVBoxLayout
from PyQt5 import QtWidgets, uic
#
import Globals as glb


def p(x):
    print(x)


class Communicate(QtCore.QObject):
    def __init__(self):
        # super().__init__()
        super(Communicate, self).__init__()
        self.__sendLogs = QtCore.pyqtSignal()

    @property
    def sendLogs(self):
        return self.__sendLogs


class AppLauncher(QWidget):
    def __init__(self, appEntryPointScriptFilepath=glb.APP_GUI_ENTRY_POINT):
        super(AppLauncher, self).__init__()
        self.__appEntryPointScriptFilepath = appEntryPointScriptFilepath
        self.__comm = Communicate()
        print('Connecting process')
        self.__process = QtCore.QProcess(self)
        self.__process.readyReadStandardOutput.connect(self.stdoutReady)
        self.__process.readyReadStandardError.connect(self.stderrReady)
        self.__process.started.connect(lambda: p('Started!'))
        self.__process.finished.connect(lambda: p('Finished!'))

    def append(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        # self.output.ensureCursorVisible()

    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput())
        print(text.strip())
        self.append(text)

    def stderrReady(self):
        text = str(self.process.readAllStandardError())
        print(text.strip())
        self.append(text)

    def attachToScript(self):
        print('Starting process')
        print(self.__appEntryPointScriptFilepath)
        self.__process.start('python', [self.__appEntryPointScriptFilepath])
        self.__procEnv = self.__process.processEnvironment()
        #for key in self.__procEnv.keys():
        #    print("proc env:   key:", key, " val:", self.__procEnv.value(key))
        print(self.__procEnv.toStringList())

    def run(self):
        try:
            self.attachToScript()
        except Exception as e:
            print("[", dt.datetime.now(), ", LOG] msg: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    appLauncher = AppLauncher()
    appLauncher.run()

    # Start event loop
    sys.exit(app.exec_())