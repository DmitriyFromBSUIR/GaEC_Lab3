#
import sys
#
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QSizePolicy, QScrollArea


class Widget(QWidget):

    def __init__(self, parent= None):
        super(Widget, self).__init__()

        btn_new = QPushButton("Append new label")
        btn_new.clicked.connect(self.add_new_label)

        #Container Widget
        self.widget = QWidget()
        #Layout of Container Widget
        layout = QVBoxLayout(self)
        for _ in range(20):
            label = QLabel("test")
            layout.addWidget(label)
        layout.addStretch()
        self.widget.setLayout(layout)

        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        #Scroll Area Layer add
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(btn_new)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)

    def add_new_label(self):
        label = QLabel("new")
        self.widget.layout().addWidget(label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Widget()
    dialog.show()
    sys.exit(app.exec_())