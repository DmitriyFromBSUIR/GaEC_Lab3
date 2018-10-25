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
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit, QVBoxLayout, QTextEdit, QPushButton
from PyQt5 import QtWidgets, uic


# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal
class MyReceiver(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        # QObject.__init__(self, *args, **kwargs)
        super().__init__()
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)

# An example QObject (to be run in a QThread) which outputs information with print
class LongRunningThing(QtCore.QObject):
    @QtCore.pyqtSlot()
    def run(self):
        for i in range(1000):
            print(i)

# An Example application QWidget containing the textedit to redirect stdout to
class MyApp(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.textedit = QTextEdit()
        self.button = QPushButton('start long running thread')
        self.button.clicked.connect(self.start_thread)
        self.layout.addWidget(self.textedit)
        self.layout.addWidget(self.button)

    @QtCore.pyqtSlot(str)
    def append_text(self, text):
        self.textedit.moveCursor(QtGui.QTextCursor.End)
        self.textedit.insertPlainText( text )

    @QtCore.pyqtSlot()
    def start_thread(self):
        self.thread = QtCore.QThread()
        self.long_running_thing = LongRunningThing()
        self.long_running_thing.moveToThread(self.thread)
        self.thread.started.connect(self.long_running_thing.run)
        self.thread.start()

# Create Queue and redirect sys.stdout to this queue
queue = Queue()
sys.stdout = WriteStream(queue)

# Create QApplication and QWidget
qapp = QApplication(sys.argv)
app = MyApp()
app.show()

# Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
thread = QtCore.QThread()
my_receiver = MyReceiver(queue)
my_receiver.mysignal.connect(app.append_text)
my_receiver.moveToThread(thread)
thread.started.connect(my_receiver.run)
thread.start()

qapp.exec_()