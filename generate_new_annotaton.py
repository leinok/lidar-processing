"""
This is just an temporary python file
I figured the problem which I transpose the image
"""
import numpy as np
import os
import pdb

annotation_folder = '/mnt/data_0/kitti/training/volume_60/All/Annotations/'
save_folder = '/mnt/data_0/kitti/training/volume_60/All/New_Annotations/'
for filename in os.listdir(annotation_folder):
    file_name = os.path.join(annotation_folder, filename)
    annotation = np.loadtxt(file_name)
    if annotation.ndim == 1:
	annotation = np.expand_dims(annotation, axis = 0)
	
    new_annotation = annotation[:, [1, 0, 2, 4, 3, 5, 6, 7]]
    np.savetxt(os.path.join(save_folder, filename), new_annotation, fmt = '%.2f')
    
