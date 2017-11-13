import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pdb
from mpl_toolkits.mplot3d import Axes3D
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui


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
	
	z = lidar[:, 2]
	selected_area = np.where((z > -2.0) & (z < 0.5))[0]

	n, bins, patches = plt.hist(lidar[selected_area, 3], 10, normed=1, facecolor='green', alpha=0.75)
	plt.show()
	scatter_plot = gl.GLScatterPlotItem(pos = lidar[selected_area, :3], color = pg.glColor('g'), size = 0.1)
	view_widget.addItem(scatter_plot)
	pdb.set_trace()


if __name__ == "__main__":
	pc_path = '/mnt/data_0/kitti/training/velodyne/002559.bin'
#	pc_path = '/mnt/data_0/SAIC_DATA/VLP32_2017_1106/xyzi_000007_559293.bin'
	lidar = np.fromfile(pc_path, dtype = np.float32).reshape(-1, 4)
	# if it is from our dumped data, than / 100.
#	lidar = lidar / 100.0
	visualize(lidar)
