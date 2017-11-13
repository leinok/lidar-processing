import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pdb
import pprint

def randomSelect(annotation_folder = '/mnt/data_0/kitti/training/volume_60/All/Annotations/', interested_class = 1):
    index = []
    for txt_name in os.listdir(annotation_folder):
	label = np.loadtxt(os.path.join(annotation_folder, txt_name))
	if label.ndim is 1:
	    label = np.expand_dims(label, axis = 0)
	label = label[:, -1]
	if interested_class in label:
	    index.append(txt_name)

    pdb.set_trace()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(index)


def testNpy(img_folder = '/mnt/data_0/kitti/training/new_bv_feat6/', img_name = 'bbox2D_001596.npy'):
    img = np.load(img_folder + img_name)
    pdb.set_trace()    
    plt.imshow(img[:, :, 1])
    plt.show()

if __name__ == "__main__":
    testNpy()	
