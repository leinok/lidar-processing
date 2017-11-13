This is a description of KITTI Lidar coordinates:

               
             / 
	    /
           /
	  /			(-)
	 /	
        /
	----------------->	(0)	(yaw angle)
	\
	 \			(+)
	  \
	   \
	    \
	     \
 


	          /|\  (x)
	           |
		 --|--
                 | | |
	 <-------|-| |
	(y)	 |   |
		 -----


In the lidar_velodyne file, I reverse the y direction to keep the image consistent with the camera image
