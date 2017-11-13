#include <iostream>
#include <math.h>
#include <time.h>
#include <cstring>
#include <string>
#include <fstream>
#include <boost/filesystem.hpp>
using namespace boost::filesystem;
using namespace std;

// x: front-back direction, y: left-right
double y_min = 0, y_max = 60, x_min = -30, x_max = 30, z_min = -2.3, z_max = 0.2; // For kitti, the default is -2.0 and 0.5
int height_level = 5;
double dx = 0.1, dy = 0.1, dz = 0.5; // dz = (z_max - z_min) / M
int x_len, y_len, z_len;

const int sizePt = 6;
unsigned char *counter;
int area_2d;

timespec diff(timespec start, timespec end)
{
	timespec temp;
	if ((end.tv_nsec-start.tv_nsec)<0) {
		temp.tv_sec = end.tv_sec-start.tv_sec-1;
		temp.tv_nsec = 1e+9 +end.tv_nsec-start.tv_nsec;
	} else {
		temp.tv_sec = end.tv_sec-start.tv_sec;
		temp.tv_nsec = end.tv_nsec-start.tv_nsec;
	}
	return temp;
}

int binRead(const char *fname, double *dat) {
	FILE *fp = fopen(fname, "rb");
	if (!fp) {
		printf("Failed to open file: %s\n", fname);
		return 1;
	}

	struct {
		float x;
		float y;
		float z;
		float in;
	}xyzi;

	// The data is in cm.
	int vecSize = 0;
	while (!feof(fp)) {
		fread(&xyzi, 1, sizeof(xyzi), fp);
		dat[0] = xyzi.x / 100.;
		dat[1] = xyzi.y / 100.;
		dat[2] = xyzi.z / 100.;
		dat[3] = xyzi.in;
		++vecSize;
		dat += sizePt;
	}
	fclose(fp);
	return vecSize;
}

// level belongs to {0, 1, 2, 3}
int heightMap(int M, int vector_size, double* dat, unsigned char* out) {
	int density_2d = M * area_2d;
	memset(counter, 0, area_2d * sizeof(unsigned char));
	// For record
	double max_all_ref = 0;
	unsigned char max_uc_ref = 0;
	int max_pos = 0;
	for (int i = 0; i < vector_size * 6; i += 6) {
		
		double x = dat[i];
		double y = dat[i+1];
		double z = dat[i+2];
		double in = dat[i+3];
		if (in > max_all_ref)
			max_all_ref = in;
		if (x < x_min || x >= x_max || y < y_min || y >= y_max || z < z_min || z >= z_max) {
			continue;
		}
		
		int xi = (x - x_min) / dx;
		int yi = (y - y_min) / dy;
		int zi = (z - z_min) / dz;
		if (xi >= x_len || yi >= y_len || zi >= z_len) {
			cout << "-----Debug for this part------";
			continue;
		}

		int pos_2d = yi * x_len + xi;
		int cur_pos = zi * area_2d + pos_2d;
		// Density map can be merged here.
		if (counter[pos_2d] <= 31)
		    counter[pos_2d]++;
		
		unsigned char uc_z = (unsigned char)((z - z_min) / (z_max - z_min) * 255);
		if (uc_z > out[cur_pos]) {
			out[cur_pos] = uc_z;
		}
			
	}

	// Density map normalize
	const double denominator = 4.15888308336; //log(64)

	for (int i = 0; i < area_2d; ++i) {
		unsigned char cur_counter = counter[i];
		if (cur_counter == 0)
			continue;
		else if (cur_counter >= 31)
			out[density_2d + i] = 255;
		else
			out[density_2d + i] = (unsigned char) (log( 2 * cur_counter) / denominator * 255);
	}
	return 0;
} 


int processSingleFrame(char* framePath, double* dat, unsigned char *out, int sizeOut) {
	timespec time1, time2;
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time1);
	memset(out, 0, sizeOut);
	int vec_size = binRead(framePath, dat);
	cout << "vec_size is: " << vec_size << '\n';
	heightMap(height_level, vec_size, dat, out);
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time2);
	cout << "sec is: " << diff(time1, time2).tv_sec << " while nsec is: " << diff(time1, time2).tv_nsec << '\n';
	char *save_bin_name = framePath;
	string save_name = string(framePath).replace(22, 15, "nointensity1_new_bv_feat6");
	//save_name = "data.bin";
	cout << string(save_name) <<'\n';
	std::ofstream outfile(save_name, std::ofstream::binary);
	outfile.write(reinterpret_cast<char*>(out), sizeOut);
	outfile.close();

	return 0;
}
// Intensity map: the number of points (counter) 
int main(int argc, char *argv[]) {
	if (argc < 2) {
		cout << "usage: " << argv[0] << " xxx.bin" << '\n';
		return 1;
	}

	path p (argv[1]);
	if (exists(p)) {
		if (is_regular_file(p) || is_directory(p))
			cout << "valid..." << '\n';
		else {
			cout << p << " exists, but is neither a regular file nor a directory\n";
			return 1;
		}
	}

	x_len = ceil((x_max - x_min) / dx);
	y_len = ceil((y_max - y_min) / dy);
	z_len = ceil((z_max - z_min) / dz);
	area_2d = x_len * y_len;
	cout << "x_len, y_len and z_len are " << x_len << ", " << y_len << " and " << z_len << '\n';
	const int numMaxPt = 150000;
	int sizeOut = x_len * y_len * (z_len + 1) * sizeof(unsigned char);
	double *dat = (double*)malloc(numMaxPt * sizePt * sizeof(double));
	unsigned char *out = (unsigned char*)malloc(sizeOut);	
	counter = (unsigned char*)malloc(area_2d * sizeof(unsigned char));


	if (is_regular_file(p)) { 
		processSingleFrame(argv[1], dat, out, sizeOut);
	}
	else {
		directory_iterator end_itr;
		for (directory_iterator itr(p); itr != end_itr; ++itr) {
		    if (is_regular_file(itr->path())) {
			string current_file = itr->path().string();
			cout << current_file << endl;
			processSingleFrame(const_cast<char*>(current_file.c_str()), dat, out, sizeOut);
		    }
		}
	}


	free(counter);

	free(out);	
	free(dat);
	return 0;
}	


	
	
