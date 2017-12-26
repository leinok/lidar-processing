import numpy as np
import pdb
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#bin_name = "/mnt/data_0/SAIC_DATA/nointensity1_new_bv_feat6/xyzi_000431_636566.bin"
#bin_name = '/home/saiclei/data.bin'
#bin_data = np.fromfile(bin_name, dtype = np.uint8).reshape(6, 600, 600)

real_data = np.load('/mnt/data_0/kitti/training/nointensity_mc_data/nointensity_new_bv_feat6/bbox2D_003987.npy')

original_name = 'bbox2D_000178'
original_data = np.load('/mnt/data_0/kitti/training/nointensity_mc_data/nointensity_new_bv_feat6_rotate_3times_blind/{}.npy'.format(original_name))
file_name = 'bbox2D_010178'
rotate45_data = np.load('/mnt/data_0/kitti/training/nointensity_mc_data/nointensity_new_bv_feat6_rotate_3times_blind/{}.npy'.format(file_name))

f, axarr = plt.subplots(2, 3)
im = axarr[0, 0].imshow(original_data[:, :, 0], vmin = 0, vmax = 255)
axarr[0, 1].imshow(original_data[:, :, 1], vmin = 0, vmax = 255)
axarr[0, 2].imshow(original_data[:, :, 2], vmin = 0, vmax = 255)
axarr[1, 0].imshow(original_data[:, :, 3], vmin = 0, vmax = 255)
axarr[1, 1].imshow(original_data[:, :, 4], vmin = 0, vmax = 255)
axarr[1, 2].imshow(original_data[:, :, 5], vmin = 0, vmax = 255)
bboxes = np.loadtxt('/mnt/data_0/kitti/training/volume_60/All/New_Train_Annotations_rotate_3times/{}.txt'.format(original_name))
if bboxes.ndim == 1:
	bboxes = np.expand_dims(bboxes, axis = 0)
for i in xrange(bboxes.shape[0]):
	bbox = bboxes[i, :] 
	axarr[1, 2].add_patch(plt.Rectangle((bbox[0], bbox[1]),
			        	bbox[3] - bbox[0],
			        	bbox[4] - bbox[1], fill = False,
		    		    edgecolor = 'r', linewidth = 1))

f.colorbar(im)

f1, axarr1 = plt.subplots(2, 3)
im = axarr1[0, 0].imshow(rotate45_data[:, :, 0], vmin = 0, vmax = 255)
axarr1[0, 1].imshow(rotate45_data[:, :, 1], vmin = 0, vmax = 255)
axarr1[0, 2].imshow(rotate45_data[:, :, 2], vmin = 0, vmax = 255)
axarr1[1, 0].imshow(rotate45_data[:, :, 3], vmin = 0, vmax = 255)
axarr1[1, 1].imshow(rotate45_data[:, :, 4], vmin = 0, vmax = 255)
axarr1[1, 2].imshow(rotate45_data[:, :, 5], vmin = 0, vmax = 255)
bboxes = np.loadtxt('/mnt/data_0/kitti/training/volume_60/All/New_Train_Annotations_rotate_3times/{}.txt'.format(file_name))
if bboxes.ndim == 1:
	bboxes = np.expand_dims(bboxes, axis = 0)
for i in xrange(bboxes.shape[0]):
	bbox = bboxes[i, :] 
	axarr1[1, 2].add_patch(plt.Rectangle((bbox[0], bbox[1]),
			        	bbox[3] - bbox[0],
			        	bbox[4] - bbox[1], fill = False,
		    		    edgecolor = 'r', linewidth = 1))
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

