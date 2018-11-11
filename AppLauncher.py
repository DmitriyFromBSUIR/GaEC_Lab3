
#
import sys
import os
import datetime as dt
import re
from queue import Queue
#
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtWidgets, uic
#
import Globals as glb
import UI.MainWindow as mw


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


class CustomProcess(QtCore.QProcess):
    def __init__(self):
        super(CustomProcess, self).__init__()
        self.readyReadStandardOutput.connect(self.stdoutReady)
        self.readyReadStandardError.connect(self.stderrReady)
        self.started.connect(lambda: p('Started!'))
        self.finished.connect(lambda: p('Finished!'))

    def append(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        # self.output.ensureCursorVisible()

    def stdoutReady(self):
        text = str(self.readAllStandardOutput())
        print(text.strip())
        self.append(text)

    def stderrReady(self):
        text = str(self.readAllStandardError())
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


class AppLauncher(QWidget):
    def __init__(self, appEntryPointScriptFilepath=glb.APP_GUI_ENTRY_POINT):
        super(AppLauncher, self).__init__()
        self.__appEntryPointScriptFilepath = appEntryPointScriptFilepath
        self.__comm = Communicate()
        print('Connecting process')
        self.__process = CustomProcess()

    def run(self):
        try:
            self.attachToScript()
        except Exception as e:
            print("[", dt.datetime.now(), ", LOG] msg: ", e)


class ConsoleLogQueue:
    def __init__(self):
        self.__queue = Queue()

    @property
    def queue(self):
        return self.__queue


# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class StreamWriter(object):
    def __init__(self, queue):
        self.__queue = queue

    def write(self, text):
        if self.__queue is not None:
            self.__queue.put(text)


class AppGuiLauncher(QWidget, QtCore.QObject):
    consoleLogsUpdateSignal = QtCore.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        super(AppGuiLauncher, self).__init__()
        self.__queue = queue
        self.__consoleLogUpdateSignal = QtCore.pyqtSignal(str)

    @property
    def queue(self):
        return self.__queue

    @property
    def consoleLogUpdateSignal(self):
        return self.__consoleLogUpdateSignal

    #@QtCore.pyqtSlot()
    def receiveLogsFromQueue(self):
        if self.__queue is not None:
            while True:
                text = self.__queue.get()
                self.mysignal.emit(text)

    @QtCore.pyqtSlot()
    def run(self):
        try:
            self.receiveLogsFromQueue()
        except Exception as e:
            print("[", dt.datetime.now(), ", LOG] msg: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # appLauncher = AppLauncher()
    # appLauncher.run()

    # Create Queue and redirect sys.stdout to this queue
    consoleLogsQueue = ConsoleLogQueue()
    queue = consoleLogsQueue.queue
    sys.stdout = StreamWriter(queue)

    # Create Main Application GUI
    # app = QApplication(sys.argv)
    mainWin = mw.MainWindow(app=app)
    mainWin.run()

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in
    # main application gui
    thread = QtCore.QThread()
    appGuiLauncher = AppGuiLauncher(queue=queue)
    appGuiLauncher.consoleLogsUpdateSignal.connect(mainWin.appendTextToExperimentConsole)
    appGuiLauncher.moveToThread(thread)
    thread.started.connect(appGuiLauncher.run)

    mainWin.startAlgorithmsInThread()
    thread.start()

    # Start event loop
    sys.exit(app.exec_())