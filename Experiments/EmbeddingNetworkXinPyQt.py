import sys
from PyQt5 import QtWidgets
from Experiments.graphtest import Ui_MainWindow
import networkx as nx
import numpy as np
import pylab as P
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, sin, pi


# example
class DrawSin(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)

        self.axes.hold(False)

        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class Core(QtWidgets.QMainWindow):
    def __init__(self):
        super(Core, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        grid = QtWidgets.QGridLayout(self.ui.widget)
        #grid = QtWidgets.QGridLayout(self.window())

        draw_sin = DrawSin(self.ui.widget)
        #draw_sin = DrawSin(self.window())
        grid.addWidget(draw_sin)

        #self.ui.widget.setFocus()


# my graph
class Test:
    def graphb(self):
        B = nx.Graph()
        B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        Y = set(B) - X

        X = sorted(X, reverse=True)
        Y = sorted(Y, reverse=True)

        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        nx.draw(B, pos=pos, with_labels=True)

        #plt.show()  # to remove
        return plt.figure()


def main():
    app = QtWidgets.QApplication(sys.argv)
    test = Test()
    test.graphb()
    ui = Core()
    ui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()