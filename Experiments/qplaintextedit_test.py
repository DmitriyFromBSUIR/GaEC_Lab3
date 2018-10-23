
#
import sys
import os
import datetime as dt
import re
#
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit, QVBoxLayout
#
import Globals as glb


class ExperimentConsoleOutput(QWidget):
    def __init__(self):
        # super().__init__()
        super(ExperimentConsoleOutput, self).__init__()
        # Create text entry box
        self.__plainTextWgt = QPlainTextEdit()
        # Change font, colour of text entry box
        self.__plainTextWgt.setStyleSheet(
            """QPlainTextEdit {background-color: #333;
                               color: #00FF00;
                               text-decoration: underline;
                               font-family: Courier;}""")
        self.__mainLayout = QVBoxLayout(self)
        # "Central Widget" expands to fill all available space
        self.__mainLayout.addWidget(self.__plainTextWgt)
        # Print text to console whenever it changes
        self.__plainTextWgt.textChanged.connect(lambda: print(self.__plainTextWgt.document().toPlainText()))
        # Set initial value of text
        self.__plainTextWgt.document().setPlainText("Experiment log will print here")

    def run(self):
        try:
            self.show()
        except Exception as e:
            print("[", dt.datetime.now(), ", LOG] msg: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    experimentConsoleOutput = ExperimentConsoleOutput()
    experimentConsoleOutput.run()

    # Start event loop
    sys.exit(app.exec_())