

#
import sys
import os
import datetime as dt
import re
#
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy
#
import Globals as glb
import Utils.AlgoDeclListParser as adp


class ExperimentControlPanel(QWidget):
    def __init__(self, scriptFilepath=glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH, isDebug=False):
        # super().__init__()
        super(ExperimentControlPanel, self).__init__()
        self.__algoDeclListParser = adp.AlgoDeclListParser(scriptFilepath=scriptFilepath, isDebug=isDebug)
        self.__algoDeclListParser.run()
        self.__algorithmsParams = self.__algoDeclListParser.algorithmsParams