

#
import sys
import os
import datetime as dt
import re
#
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QVBoxLayout, \
    QSizePolicy, QScrollArea
from PyQt5.QtGui import QRegExpValidator
#
import Globals as glb


class ExperimentStatisticsPanel(QWidget):
    def __init__(self):
        # super().__init__()
        super(ExperimentStatisticsPanel, self).__init__()
        self.__experimentIntermediateResaults = None

    def run(self):
        try:

            self.show()
        except Exception as e:
            print("[", dt.datetime.now(), ", LOG] msg: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    expStatPanel = ExperimentStatisticsPanel()
    expStatPanel.run()
    sys.exit(app.exec_())