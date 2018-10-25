

#
import os
import sys
import datetime as dt
import re
#
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat, )
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
import PyQt5.QtWidgets as qwgt
from PyQt5.QtWidgets import (QAction, QApplication, QWidget, QDialog, QDockWidget,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit, QVBoxLayout, QHBoxLayout, QSplitter)
#
import Globals as glb
import UI.Widgets.FilesHierarchyViewer as fhv
import UI.Widgets.FileContentViewer as fcv
import UI.Widgets.ExperimentControlPanel as ecp
import UI.Widgets.ExperimentStatisticsPanel as esp
import UI.Widgets.ExperimentConsoleOutput as eco


mainWin = None


class MainWindow(QMainWindow):

    def __init__(self, app=None, isFullscreenMode=False, appWinWidthFactor=2, appWinHeightFactor=2):
        # super().__init__()
        super(MainWindow, self).__init__()
        self.__app = app
        self.__isFullscreenMode = isFullscreenMode
        self.__shiftAppWindowX = 100
        self.__shiftAppWindowY = 100
        self.__appWindowWidth = 0
        self.__appWindowHeight = 0
        self.__appWinWidthFactor = 2
        self.__appWinHeightFactor = 2
        if (appWinWidthFactor > 0) and (appWinHeightFactor > 0):
            self.__appWinWidthFactor = appWinWidthFactor
            self.__appWinHeightFactor = appWinHeightFactor
        self.__appDisplayRect = None
        self.initUI()
        # menu actions
        self.newExperimentAct = None
        # menu toolbar
        self.experimentControlToolbar = None
        # custom high-level widgets
        self.wgtFilesHierarchyViewer = None
        self.wgtFileContentViewer = None
        self.wgtExperimentTasksVisualizer = None
        self.wgtFitnessFunctionVisualizer = None
        self.wgtExperimentConsole = None
        self.wgtExperimentControlPanel = None
        self.wgtExperimentStatisticsPanel = None

    @property
    def experimentConsoleWgt(self):
        return self.wgtExperimentConsole

    def printScreenSettings(self):
        if self.__app is not None:
            screen = app.primaryScreen()
            print('Screen: %s' % screen.name())
            size = screen.size()
            print('Size: %d x %d' % (size.width(), size.height()))
            rect = screen.availableGeometry()
            print('Available: %d x %d' % (rect.width(), rect.height()))

    def getScreenSizes(self):
        displayRectSize = qwgt.QDesktopWidget().screenGeometry(-1)
        w = displayRectSize.width()
        h = displayRectSize.height()
        print(" Screen size : " + str(w) + "x" + str(h))
        return displayRectSize, w, h

    def setAppWindowSize(self, w, h):
        self.__appWindowWidth = w
        self.__appWindowHeight = h

    def appWindowAutotuning(self):
        displayRectSize, width, height = self.getScreenSizes()
        self.__appDisplayRect = displayRectSize
        self.setAppWindowSize(int(width / self.__appWinWidthFactor), int(height / self.__appWinHeightFactor))

    def configureWindow(self):
        self.appWindowAutotuning()
        if (self.__appDisplayRect is not None) and (self.__isFullscreenMode):
            # self.setGeometry(self.__appDisplayRect)
            self.showFullScreen()
        else:
            self.setGeometry(300, 300, self.__appWindowWidth, self.__appWindowHeight)
        self.setWindowTitle('GaEC Research Tool (Genetic and evolutionary computing research tool, build ver. 2018.09.22)')

    def newExperiment(self):
        pass

    def printing(self):
        document = self.textEdit.document()
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec_() != QDialog.Accepted:
            return
        document.print_(printer)
        self.statusBar().showMessage("Ready", 2000)

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def about(self):
        QMessageBox.about(self, "GaEC Research Tool",
                "The <b>GaEC Research Tool</b> is lab project that aimed to "
                "learn genetic algoritms and evolution methods "
                "for optimization and combinatorics tasks solving"
                )

    def launchLab1(self):
        pass

    def launchLab2(self):
        pass

    def launchLab3(self):
        pass

    def launchExperiment(self):
        print("Epriment started!!!")
        self.startAlgorithmsInThread()

    def createActions(self):
        print("app resources filedir = ", glb.APP_RESOURCES_DIR)
        self.newExperimentAct = QAction(QIcon(glb.APP_RESOURCES_DIR + 'new.png'),
                "&New experiment", self, shortcut=QKeySequence.New,
                statusTip="Create a new form letter", triggered=self.newExperiment)

        self.saveAct = QAction(QIcon(glb.APP_RESOURCES_DIR + 'save.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.printAct = QAction(QIcon(glb.APP_RESOURCES_DIR + 'print.png'), "&Print...", self,
                shortcut=QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.printing)

        self.undoAct = QAction(QIcon(glb.APP_RESOURCES_DIR + 'undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

        self.quitAct = QAction("&Exit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.launchLab1Act = QAction("&LaunchLab1", self, shortcut="Ctrl+1",
                                           statusTip="Start experiment", triggered=self.launchLab1)

        self.launchLab2Act = QAction("&LaunchLab2", self, shortcut="Ctrl+2",
                                           statusTip="Start experiment", triggered=self.launchLab2)

        self.launchLab3Act = QAction("&LaunchLab3", self, shortcut="Ctrl+3",
                                           statusTip="Start experiment", triggered=self.launchLab3)

        self.experimentManageAct = QAction("&Run", self, shortcut="Ctrl+L",
                statusTip="Start experiment", triggered=self.launchExperiment)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newExperimentAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.toolsMenu.addAction(self.launchLab1Act)
        self.toolsMenu.addAction(self.launchLab2Act)
        self.toolsMenu.addAction(self.launchLab3Act)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newExperimentAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.printAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAct)

        self.experimentControlToolbar = self.addToolBar("Experiment management")
        self.experimentControlToolbar.addAction(self.experimentManageAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createFilesHierarchyViewerWgt(self):
        dockWin = QDockWidget("Files Hierarchy Viewer", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wgtFilesHierarchyViewer = fhv.FilesHierarchyViewer()
        dockWin.setWidget(self.wgtFilesHierarchyViewer)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createFileViewerWgt(self):
        dockWin = QDockWidget("File Viewer", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # self.wgtFileContentViewer = fcv.FileContentViewer()
        # dockWin.setWidget(self.wgtFileContentViewer)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createExperimentTasksVisualizationWgt(self):
        dockWin = QDockWidget("Experiment Tasks Visualization", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wgtExperimentTasksVisualizer = QListWidget(dockWin)
        self.wgtExperimentTasksVisualizer.addItems((
            "File 1",
            "File 2"))
        dockWin.setWidget(self.wgtExperimentTasksVisualizer)
        # self.addDockWidget(Qt.NoDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createFitnessFunctionVisualizationWgt(self):
        dockWin = QDockWidget("Fitness Function Visualization", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wgtFitnessFunctionVisualizer = QListWidget(dockWin)
        self.wgtFitnessFunctionVisualizer.addItems((
            "File 1",
            "File 2"))
        dockWin.setWidget(self.wgtFitnessFunctionVisualizer)
        # self.addDockWidget(Qt.NoDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createExperimentConsoleWgt(self):
        dockWin = QDockWidget("Experiment Console", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wgtExperimentConsole = eco.ExperimentConsoleOutput()
        dockWin.setWidget(self.wgtExperimentConsole)
        # self.addDockWidget(Qt.NoDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createExperimentControlPanelWgt(self):
        dockWin = QDockWidget("Experiment Control Panel", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wgtExperimentControlPanel = ecp.ExperimentControlPanel()
        dockWin.setWidget(self.wgtExperimentControlPanel)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createExperimentStatisticsPanelWgt(self):
        dockWin = QDockWidget("Experiment Statistics Panel", self)
        dockWin.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wgtExperimentStatisticsPanel = esp.ExperimentStatisticsPanel()
        dockWin.setWidget(self.wgtExperimentStatisticsPanel)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWin)
        self.viewMenu.addAction(dockWin.toggleViewAction())
        return dockWin

    def createCentralWidget(self):
        #
        experimentTasksVisualizationWgt = self.createExperimentTasksVisualizationWgt()
        #
        fitnessFunctionVisualizationWgt = self.createFitnessFunctionVisualizationWgt()
        #
        experimentConsoleWgt = self.createExperimentConsoleWgt()
        # experimentConsoleWgt.setMaximumHeight(300)
        #
        # visLayout = QHBoxLayout()
        # visLayout.addWidget(experimentTasksVisualizationWgt)
        # visLayout.addWidget(fitnessFunctionVisualizationWgt)
        hSplitter = QSplitter(Qt.Horizontal)
        hSplitter.addWidget(experimentTasksVisualizationWgt)
        hSplitter.addWidget(fitnessFunctionVisualizationWgt)
        # dockedVisWgts = QWidget()
        # dockedVisWgts.setLayout(visLayout)
        #
        centralWgtMainLayout = QVBoxLayout()
        # centralWgtMainLayout.addWidget(dockedVisWgts)
        # centralWgtMainLayout.addWidget(experimentConsoleWgt)
        vSplitter = QSplitter(Qt.Vertical)
        vSplitter.addWidget(hSplitter)
        vSplitter.addWidget(experimentConsoleWgt)
        centralWgtMainLayout.addWidget(vSplitter)
        #
        centralWidget = QWidget()
        centralWidget.setLayout(centralWgtMainLayout)
        return centralWidget

    def createDockWindows(self):
        #
        self.createFilesHierarchyViewerWgt()
        #
        self.createFileViewerWgt()
        #
        centralWidget = self.createCentralWidget()
        self.setCentralWidget(centralWidget)
        #
        self.createExperimentControlPanelWgt()
        #
        self.createExperimentStatisticsPanelWgt()

    def initUI(self):
        # configure app window
        self.configureWindow()
        # set central wgt that save high level control panels

        # build main ui controls
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

    @QtCore.pyqtSlot(str)
    def appendTextToExperimentConsole(self, text):
        #self.textedit.moveCursor(QtGui.QTextCursor.End)
        #self.textedit.insertPlainText(text)
        self.wgtExperimentConsole.qPlainTextWgt.moveCursor(QtGui.QTextCursor.End)
        self.wgtExperimentConsole.qPlainTextWgt.insertPlainText(text)



    @QtCore.pyqtSlot()
    def startAlgorithmsInThread(self):
        self.thread = QtCore.QThread()

        # An example QObject (to be run in a QThread) which outputs information with print
        class LongRunningThing(QtCore.QObject):
            @QtCore.pyqtSlot()
            def run(self):
                for i in range(1000):
                    print(i)

        self.long_running_thing = LongRunningThing()
        self.long_running_thing.moveToThread(self.thread)
        self.thread.started.connect(self.long_running_thing.run)
        self.thread.start()

    def run(self):
        self.show()

def run():
    try:
        app = QApplication(sys.argv)
        mainWin = MainWindow(app=app)
        mainWin.run()
        sys.exit(app.exec_())
    except Exception as e:
        print("[", dt.datetime.now(), ", LOG] msg: ", e)


def getMainWindowGuiInstance():
    return mainWin

def getExperimentConsoleOutputWgt():
    if getMainWindowGuiInstance() is not None:
        return getMainWindowGuiInstance().experimentConsoleWgt()
    else:
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow(app=app)
    mainWin.run()
    sys.exit(app.exec_())