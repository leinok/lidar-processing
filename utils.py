import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pdb
import pprint
import re
import glob

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

def str2num(str_list, output_type):
	return [output_type(x) for x in str_list]

def plot_from_txt_fasterrcnn_logs(log_file):
	pattern_itr = re.compile(r"105\]\s+Iteration\s+([\d]+)")
	pattern_rpn = re.compile(r"rpn_cls_loss_pedestrian[\s=]{1,3}([\d\.]+)")
	pattern_box = re.compile(r"rpn_loss_bbox_pedestrian[\s=]{1,3}([\d\.]+)")
	pattern_loss = re.compile(r"[\s]loss[\s=]{1,3}([\d\.]+)")

	with open(log_file, 'r') as f:
		lines = f.read()
		itrs = pattern_itr.findall(lines)
		rpns = pattern_rpn.findall(lines)
		boxs = pattern_box.findall(lines)
		loss = pattern_loss.findall(lines)	
		pdb.set_trace()
		itrs = np.array(str2num(itrs, int))
		rpns = np.array(str2num(rpns, float))
		boxs = np.array(str2num(boxs, float))
		loss = np.array(str2num(loss, float))
 
		plt.figure()
		plt.sca(plt.subplot(311))
		plt.plot(itrs, rpns)
		plt.title("RPN Class Loss")

		plt.sca(plt.subplot(312))
		plt.plot(itrs, boxs)
		plt.title("RPN Boundary Box Loss")

		plt.sca(plt.subplot(313))
		plt.plot(itrs, loss)	
		plt.title("The total loss")


		plt.show()

def blindSpecificArea():
	left_angle = 90
	right_angle = 0
	center_x = 299.5

	x = np.linspace(0, 599, 600)	
	y = np.linspace(0, 599, 600)
	xx, yy = np.meshgrid(x, y)
	if left_angle == 0:
		idx = (xx >= center_x)
	elif right_angle == 0:
		idx = (xx <= center_x)
	else:
		right_tan = np.tan(right_angle / 180. * np.pi)
		left_tan = -np.tan(left_angle / 180. * np.pi)
		arctan = yy / (xx - center_x)
		idx = ((arctan > right_tan) | (arctan < left_tan))
		idx = np.logical_not(idx)
	
	return idx

def blindImg():
	idx = blindSpecificArea()

	original_folder = '/mnt/data_0/kitti/training/rotate-45_nointensity_new_bv_feat6/';
	blind_folder = '/mnt/data_0/kitti/training/rotate-45_nointensity_new_bv_feat6_blind/';
	for original_file in glob.glob(original_folder + '*.npy'):
		basename = os.path.basename(original_file)
		print basename
		x = np.load(original_file)
		x[idx,:] = 0
		save_name = os.path.join(blind_folder, basename)	
		np.save(save_name, x)

if __name__ == "__main__":	
	#log_file = "./faster_rcnn_end2end_VGG16_.txt.2017-11-27_15-01-25"
	#plot_from_txt_fasterrcnn_logs(log_file)	
	blindImg()
