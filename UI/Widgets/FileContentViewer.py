

#
import os
import sys
import re
import datetime as dt
from enum import Enum
#
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QSizePolicy
#
import Globals as glb
import UI.Widgets.Notepad as npad


class TextEditorWorkMode(Enum):
    SIMPLE = 0
    FULLFEATURED = 1


class FileContentViewer(QWidget):
    def __init__(self, defaultFilepath=glb.FILE_CONTENT_VIEWER_DEFAULT_FILEPATH, textEditorWorkMode=TextEditorWorkMode.SIMPLE):
        # super().__init__()
        super(FileContentViewer, self).__init__()
        self.__defaultFilepath = defaultFilepath
        self.__textEditorWorkMode = textEditorWorkMode
        self.__widget = None
        #
        self.run()

    @property
    def filepath(self):
        return self.__defaultFilepath

    @property
    def textEditorWorkMode(self):
        return self.__textEditorWorkMode

    @property
    def widget(self):
        return self.__widget

    def createWidget(self):
        if self.__textEditorWorkMode.value == TextEditorWorkMode.SIMPLE.value:
            self.__widget = npad.main()

    def run(self):
        try:
            self.createWidget()
        except Exception as e:
            print("[", dt.datetime.now(), "] LOG: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fcv = FileContentViewer()
    fcv.run()
    sys.exit(app.exec_())