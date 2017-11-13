import sys
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui

from bird_view.kitti_velodyne import * 
import pdb


class Window(QtGui.QMainWindow):
 
    def __init__(self):
        super(Window, self).__init__()
	self.setGeometry(50, 50, 500, 300)
	self.setWindowTitle("PyQT Visualizer")
  	self.setWindowIcon(QtGui.QIcon('saic.jpeg'))

        extractAction = QtGui.QAction("&Load a lidar point cloud!!!", self)
	extractAction.setShortcut("Ctrl+Q")
	extractAction.setStatusTip("Leave the App")
	extractAction.triggered.connect(self.closeApplication)

	self.statusBar()

	main_menu = self.menuBar()
	file_menu = main_menu.addMenu('&File')
	file_menu.addAction(extractAction)
	self.home()	

    def closeApplication(self):
        print("See U")
	sys.exit()

    def loadLidar(self):
	pass

    def home(self):
	btn = QtGui.QPushButton("Quit", self)
#	btn.clicked.connect(QtCore.QCoreApplication.instance().quit)\
	btn.clicked.connect(self.closeApplication)
	btn.resize(btn.minimumSizeHint())
	btn.move(0, 0)
	self.show()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

def visualize(lidar):
    pg.mkQApp()
    view_widget = gl.GLViewWidget()
    view_widget.show()
    xgrid = gl.GLGridItem()
    ygrid = gl.GLGridItem()
    zgrid = gl.GLGridItem()
    view_widget.addItem(xgrid)
    view_widget.addItem(ygrid)
    view_widget.addItem(zgrid)
    xgrid.rotate(90, 0, 1, 0)
    ygrid.rotate(90, 1, 0, 0)
    #posIdx = np.where(lidar[:, 1] > 0)[0]
    scatter_plot = gl.GLScatterPlotItem(pos = lidar[:, :3], color = pg.glColor('r'), size = 0.1)
    view_widget.addItem(scatter_plot)
    pdb.set_trace()

def visualize_new(lidar):
    pg.mkQApp()
    w = pg.GraphicsView(useOpenGL = True)
    w.show()    

if __name__ == "__main__":
    lidar = readLidarBin('/mnt/data_0/SAIC_DATA/VLP32_2017_1103/xyzi_000356_441197.bin', False)
    visualize(lidar)
#    run()
