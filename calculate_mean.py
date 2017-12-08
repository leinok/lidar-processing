##
# This is used to load all files in a folder and calculate the mean value
#
import os
import cv2
import numpy as np
import pdb

img_folder = '/mnt/data_0/kitti/training/nointensity_mc_data/nointensity_new_bv_feat6/'
num = 0
sum_value = np.array([0., 0., 0., 0., 0., 0.])
for img_name in os.listdir(img_folder):
    if img_name.endswith(".png"):
	img = cv2.imread(os.path.join(img_folder, img_name))
    elif img_name.endswith(".npy"):
	img = np.load(os.path.join(img_folder, img_name))
    img = img.astype(np.float32, copy=False)
    pdb.set_trace()
    sum_value += img.sum(axis=(0,1))
    num += 1
    if (num >= 300):
	break
 
pdb.set_trace()
sum_value / num
