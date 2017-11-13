import numpy as np
import pdb
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#bin_name = "/mnt/data_0/SAIC_DATA/nointensity1_new_bv_feat6/xyzi_000431_636566.bin"
bin_name = '/home/saiclei/data.bin'
bin_data = np.fromfile(bin_name, dtype = np.uint8).reshape(6, 600, 600)

real_data = np.load('/mnt/data_0/kitti/training/nointensity_new_bv_feat6/bbox2D_003987.npy')

f, axarr = plt.subplots(2, 3)
im = axarr[0, 0].imshow(bin_data[0, :, :], vmin = 0, vmax = 255)
axarr[0, 1].imshow(bin_data[1, :, :], vmin = 0, vmax = 255)
axarr[0, 2].imshow(bin_data[2, :, :], vmin = 0, vmax = 255)
axarr[1, 0].imshow(bin_data[3, :, :], vmin = 0, vmax = 255)
axarr[1, 1].imshow(bin_data[4, :, :], vmin = 0, vmax = 255)
axarr[1, 2].imshow(bin_data[5, :, :], vmin = 0, vmax = 255)
f.colorbar(im)

f1, axarr1 = plt.subplots(2, 3)
im = axarr1[0, 0].imshow(real_data[:, :, 0], vmin = 0, vmax = 255)
axarr1[0, 1].imshow(real_data[:, :, 1], vmin = 0, vmax = 255)
axarr1[0, 2].imshow(real_data[:, :, 2], vmin = 0, vmax = 255)
axarr1[1, 0].imshow(real_data[:, :, 3], vmin = 0, vmax = 255)
axarr1[1, 1].imshow(real_data[:, :, 4], vmin = 0, vmax = 255)
axarr1[1, 2].imshow(real_data[:, :, 5], vmin = 0, vmax = 255)
f1.colorbar(im)

#fig = plt.figure()
#ax = fig.add_subplot(111)
#X = real_data[:, :, 5]
#ax.imshow(X, cmap=cm.jet, interpolation='nearest')
#
#numrows, numcols = X.shape
#def format_coord(x, y):
#    col = int(x+0.5)
#    row = int(y+0.5)
#    if col>=0 and col<numcols and row>=0 and row<numrows:
#        z = X[row,col]
#        return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
#    else:
#        return 'x=%1.4f, y=%1.4f'%(x, y)
#
#ax.format_coord = format_coord
plt.show()

pdb.set_trace()

