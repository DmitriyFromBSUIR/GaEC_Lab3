

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
import Utils.AlgoDeclListParser as adp


class ExperimentControlPanel(QWidget):
    def __init__(self, scriptFilepath=glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH, isDebug=False):
        # super().__init__()
        super(ExperimentControlPanel, self).__init__()
        self.__algoDeclListParser = adp.AlgoDeclListParser(scriptFilepath=scriptFilepath, isDebug=isDebug)
        self.__algoDeclListParser.run()
        self.__algorithmsParams = self.__algoDeclListParser.algorithmsParams
        self.__generatedWidgetsDict = dict()
        # add scroll for layout
        self.scrollArea = QScrollArea(self)
        # self.scrollArea.setSizePolicy()
        # self.scrollArea.addStretch(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.containerWidget = QWidget()
        # print("w = ", widget.width())
        self.scrollArea.setWidget(self.containerWidget)
        # self.__mainLayout = QVBoxLayout(widget)
        self.__dynamicWgtsMainLayout = QVBoxLayout()
        self.__dynamicWgtsMainLayout.addStretch()
        self.containerWidget.setLayout(self.__dynamicWgtsMainLayout)
        # self.setLayout(self.__mainLayout)
        # self.__mainLayout = QVBoxLayout(self)
        # self.setLayout(self.scrollArea.widget().layout())
        #
        self.__mainLayout = QVBoxLayout(self)
        self.__mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.__dynamicWgtsMainLayout)
        #
        self.run()

    @property
    def generatedWidgetsDict(self):
        return self.__generatedWidgetsDict

    def addWgtsForStaticAlgoParams(self):
        #
        onlyNumbersRegexp = QtCore.QRegExp("^[0-9]+$")
        #
        lblCountOfChromosomesInPop = QLabel("Count of chromosomes in population:")
        self.__dynamicWgtsMainLayout.addWidget(lblCountOfChromosomesInPop)
        txtedtCountOfChromosomesInPop = QLineEdit()
        countOfChromosomesInPopValidator = QRegExpValidator(onlyNumbersRegexp, txtedtCountOfChromosomesInPop)
        txtedtCountOfChromosomesInPop.setValidator(countOfChromosomesInPopValidator)
        self.__dynamicWgtsMainLayout.addWidget(txtedtCountOfChromosomesInPop)
        #
        lblNumberOfEpochs = QLabel("Number Of Epochs:")
        self.__dynamicWgtsMainLayout.addWidget(lblNumberOfEpochs)
        txtedtNumberOfEpochs = QLineEdit()
        txtedtNumberOfEpochsValidator = QRegExpValidator(onlyNumbersRegexp, txtedtNumberOfEpochs)
        txtedtNumberOfEpochs.setValidator(txtedtNumberOfEpochsValidator)
        self.__dynamicWgtsMainLayout.addWidget(txtedtNumberOfEpochs)

    def generateWidgets(self):
        for enumName, enumVals in self.__algorithmsParams.items():
            enumName = re.sub(r"(\w)([A-Z])", r"\1 \2", enumName) + ":"
            lblAlgoParamCategory = QLabel(enumName)
            cmbxAlgoParamNames = QComboBox()
            for enumVal in enumVals:
                cmbxAlgoParamNames.addItem(enumVal.replace("_", " "))
            # add generated widgets in general dict
            self.__generatedWidgetsDict.update({lblAlgoParamCategory: cmbxAlgoParamNames})
            # add widgets in layout
            self.__dynamicWgtsMainLayout.addWidget(lblAlgoParamCategory)
            self.__dynamicWgtsMainLayout.addWidget(cmbxAlgoParamNames)

    def run(self):
        try:
            self.addWgtsForStaticAlgoParams()
            self.generateWidgets()
            self.show()
        except Exception as e:
            print("[", dt.datetime.now(), ", LOG] msg: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    expCntrlPanel = ExperimentControlPanel(scriptFilepath=glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH, isDebug=False)
    expCntrlPanel.run()
    sys.exit(app.exec_())