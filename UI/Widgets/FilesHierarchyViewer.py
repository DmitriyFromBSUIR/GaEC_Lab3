

#
import os
import sys
import re
import datetime as dt
#
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon
#
import Globals as glb


class FilesHierarchyViewer(QWidget):

    def __init__(self):
        # super().__init__()
        super(FilesHierarchyViewer, self).__init__()
        self.title = 'File system viewer'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.model = QFileSystemModel()
        self.model.setRootPath(glb.DIRECTORY_VIEWER_ROOT_PATH)
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FilesHierarchyViewer()
    sys.exit(app.exec_())