"""
Show Bird View Image
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import numpy as np
import pdb

# Calculate the rotated x and y
class Lidar2D(object):
    def __init__(self, img, bboxes, orientations = 0):
	# bbox dim is 2, img is image to be shown, this can be from top_down image.
	self.img = img
	self.bboxes = bboxes
	self.orientations = orientations
	self.fig, self.ax = plt.subplots(figsize=(15, 15))

    def rotateXY(self, bx, by, theta):
    # (https://stackoverflow.com/questions/9971230/calculate-rotated-rectangle-size-from-known-bounding-box-coordinates)
	temp_value = 1./((np.cos(theta))**2 - (np.sin(theta))**2)
        x = temp_value * (bx * np.cos(theta) - by*np.sin(theta))
        y = temp_value * (-bx * np.sin(theta) + by*np.cos(theta))
        return x, y

    def flipImage(self):
        self.im = self.im[:, ::-1, :]
	width = self.im.shape[1]
	for i in xrange(len(self.orientations)):
	    oldx1 = bboxes[i, 0]
	    oldx2 = bboxes[i, 2]
	    x1 = width - oldx2 - 1
	    x2 = width - oldx1 - 1
	    bboxes[i, 0] = x1
	    bboxes[i, 2] = x2
	    if orientations[i] >= 0:
	        orientations[i] = np.pi - orientations[i]
	    else:
	        orientations[i] = -np.pi - orientations[i]

    def drawBoxes(self):
        for i in xrange(1, len(bboxes)):
            bbox = bboxes[i, :]
            orientation = orientations[i]
            self.ax.add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], 
					     fill = False, edgecolor = 'yellow', linestyle = '-.', linewidth = 3.5))
            self.ax.arrow((bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2, 
		      20 * -np.cos(orientation), 20 * np.sin(-orientation), head_width = 5, 
		      head_length = 10, fc = [0.1, 0.2, 0.7], ec = 'r')
            self.ax.plot([(bbox[0]+bbox[2])/2, (bbox[0]+bbox[2])/2 - 20],  
	            [(bbox[1]+bbox[3])/2, (bbox[1]+bbox[3])/2],
		    linestyle='-.', color='w', linewidth=2)

            self.ax.text(bbox[0], bbox[1] - 2, '{:.3f}'.format(orientation / np.pi * 180), 
		     bbox = dict(facecolor = 'blue', alpha = 0.5), fontsize = 14, color = 'white')
	    self.drawRotateBox(bbox, orientation)
	    
    def drawRotateBox(self, bbox, orientation):
        bx = bbox[2] - bbox[0] + 1
	by = bbox[3] - bbox[1] + 1
	orientation = (np.pi/2. + orientation)
	# Need to double check the orientation
	if orientation > 0: 
	    theta = orientation
	elif orientation < 0:
	    theta = -orientation
	x, y = self.rotateXY(bx, by, theta+0.2)
	r2 = patches.Rectangle(((bbox[0] + bbox[2]) / 2 - x/2 , (bbox[1] + bbox[3]) / 2  - y /2),
                          x, y, fill=False, edgecolor='red', linewidth=3.5)

	t2 = mpl.transforms.Affine2D().rotate_deg_around((bbox[0] + bbox[2])/2, (bbox[1]+bbox[3])/2, 
					orientation / np.pi * 180) + self.ax.transData
     	r2.set_transform(t2)	
	self.ax.add_patch(r2)
	     	

if __name__ == "__main__":
    
    img_name = '/mnt/data_0/kitti/training/new_bv_map3/bbox2D_000049.png'
    gt_name = '/mnt/data_0/kitti/training/volume_60/Car/New_annotations/bbox2D_000049.txt'
    gt_bboxes = np.loadtxt(gt_name)
    if gt_bboxes.ndim is 1:
        gt_bboxes = np.expand_dims(gt_bboxes, axis = 0) 
    bboxes = gt_bboxes[:, [0, 1, 3, 4]]
    orientations = gt_bboxes[:, 6]
    im = cv2.imread(img_name)
    test_lidar = Lidar2D(im, bboxes)
    flipped = False
    if flipped == True:
	test_lidar.flipImage()

    test_lidar.ax.imshow(im, aspect = 'equal')
    test_lidar.drawBoxes()
	

    plt.plot([364, 353, 341, 330], [228, 238, 203, 214], 'b*')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
