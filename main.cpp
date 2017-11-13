#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <iostream>
#include <math.h>


double x_min = 0, x_max = 60, y_min = -30, y_max = 30, z_min = -2, z_max = 0.4;
double dx = 0.1, dy = 0.1, dz = 0.1;
double val_max = 255;
int x_len, y_len, z_len;

const int sizePt = 6;  //xyzrgb


timespec diff(timespec start, timespec end)
{
	timespec temp;
	if ((end.tv_nsec-start.tv_nsec)<0) {
		temp.tv_sec = end.tv_sec-start.tv_sec-1;
		temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
	} else {
		temp.tv_sec = end.tv_sec-start.tv_sec;
		temp.tv_nsec = end.tv_nsec-start.tv_nsec;
	}
	return temp;
}

int binread(const char *fname, double *dat) {
  FILE *fp = fopen(fname, "rb");
  if (!fp) {
    printf("Failed to open file: %s\n", fname);
    return 0;
  }
  
  struct {
    float x;
    float y;
    float z;
    float in; //intensity
  }xyzi;
  int vecSize = 0;
  while(!feof(fp)) {
    fread(&xyzi, 1, sizeof(xyzi), fp);
    //printf("%f %f %f %f\n", xyzi.x, xyzi.y, xyzi.z, xyzi.in);
    dat[0] = xyzi.x;
    dat[1] = xyzi.y;
    dat[2] = xyzi.z;
    dat[3] = xyzi.in;
    ++vecSize;
    dat += sizePt;  //
  }
  fclose(fp);
  return vecSize;
}

int vol1(int vectorSize, double *dat, double *out) {
  //int vectorSize = 60000;
  for (int i = 0; i < vectorSize; i+=6) { //XYZRGB
    double x = dat[i];
    double y = dat[i+1];
    double z = dat[i+2];
    if (x < x_min || x >= x_max || y < y_min || y >= y_max || z < z_min || z >= z_max) {
      //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf", x, y, z); ReportInfo(buf);
      continue;
    }
    int xi = (x - x_min) / dx;
    int yi = (y - y_min) / dy;
    int zi = (z - z_min) / dz;
    if (xi >= x_len || yi >= y_len || zi >= z_len) {
      //char buf[255]; sprintf(buf, "out of idx - x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
      continue;
    }
 //printf("%d %d %d\n", xi, yi, zi);
    out[zi * x_len * y_len + yi * x_len + xi] = val_max;
    //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
  }
  return 0;
}

//counter -- channel # 4
int vol_61(int vectorSize, double *dat, double *out) {
  //int vectorSize = 60000;
  for (int i = 0; i < vectorSize; i+=6) { //XYZRGB
    double x = dat[i];
    double y = dat[i+1];
    double z = dat[i+2];
    if (x < x_min || x >= x_max || y < y_min || y >= y_max || z < z_min || z >= z_max) {
      //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf", x, y, z); ReportInfo(buf);
      continue;
    }
    int xi = (x - x_min) / dx;
    int yi = (y - y_min) / dy;
    //int zi = (z - z_min) / dz;
    if (xi >= x_len || yi >= y_len) { // || zi >= z_len
      //char buf[255]; sprintf(buf, "out of idx - x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
      continue;
    }
 //printf("%d %d %d\n", xi, yi, zi);
    out[0 * x_len * y_len + yi * x_len + xi] +=1;
    //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
  }
  return 0;
}

//max height intensity
int vol_62(int vectorSize, double *dat, double *out) {
  //int vectorSize = 60000;
  //memset(out + 2*x_len*y_len, -1, x_len*y_len);
  for (int xi = 0; xi < x_len; xi++)
    for (int yi = 0; yi < y_len; yi++) {
      out[2 * x_len * y_len + yi * x_len + xi] = -10000.0;
  }

  for (int i = 0; i < vectorSize; i+=6) { //XYZRGB
    double x = dat[i];
    double y = dat[i+1];
    double z = dat[i+2];
    double in = dat[i+3];
    if (x < x_min || x >= x_max || y < y_min || y >= y_max || z < z_min || z >= z_max) {
      //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf", x, y, z); ReportInfo(buf);
      continue;
    }
    int xi = (x - x_min) / dx;
    int yi = (y - y_min) / dy;
    //int zi = (z - z_min) / dz;
    if (xi >= x_len || yi >= y_len) { // || zi >= z_len
      //char buf[255]; sprintf(buf, "out of idx - x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
      continue;
    }
 //printf("%d %d %lf %lf\r", xi, yi, z, out[2 * x_len * y_len + yi * x_len + xi]);
    if (z > out[2 * x_len * y_len + yi * x_len + xi]) {
      out[1 * x_len * y_len + yi * x_len + xi] = in;
      out[2 * x_len * y_len + yi * x_len + xi] = z;
    }
    //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
  }
  return 0;
}

//max height (lvl: 2,3,4,5)
int vol_6n(int lvl, int vectorSize, double *dat, double *out, double z_minN, double z_maxN) {
  //int vectorSize = 60000;
  int ll = lvl * x_len * y_len;
  //memset(out + 2*x_len*y_len, -1, x_len*y_len);
  for (int xi = 0; xi < x_len; xi++)
    for (int yi = 0; yi < y_len; yi++) {
      out[ll + yi * x_len + xi] = -10000.0;
  }

  for (int i = 0; i < vectorSize; i+=6) { //XYZRGB
    double x = dat[i];
    double y = dat[i+1];
    double z = dat[i+2];
    double in = dat[i+3];
    if (x < x_min || x >= x_max || y < y_min || y >= y_max || z < z_minN || z >= z_maxN) {
      //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf", x, y, z); ReportInfo(buf);
      continue;
    }
    int xi = (x - x_min) / dx;
    int yi = (y - y_min) / dy;
    //int zi = (z - z_min) / dz;
    if (xi >= x_len || yi >= y_len) { // || zi >= z_len
      //char buf[255]; sprintf(buf, "out of idx - x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
      continue;
    }
 //printf("%d %d %lf %lf\r", xi, yi, z, out[2 * x_len * y_len + yi * x_len + xi]);
    if (z > out[ll + yi * x_len + xi]) {
      out[ll + yi * x_len + xi] = z;
    }
    //char buf[255]; sprintf(buf, "x/y/z = %lf %lf %lf;  %d %d %d", x, y, z, xi, yi, zi); ReportInfo(buf);
  }
  return 0;
}


int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("usage: %s xxx.bin\n", argv[0]);
    return 0;
  }

  // make sure the range is 0.2 and not 0.2x
  x_len = ceil((x_max - x_min) / dx);
  y_len = ceil((y_max - y_min) / dy);
  z_len = ceil((z_max - z_min) / dz);

  std::cout << "z_max and z_min are " << z_max << "and " << z_min << '\n';
  std::cout << "x_len, y_len and z_len are " << x_len << ' ' << y_len << ' ' << z_len <<'\n';
  const int numPt = 150000;
  int sizeOut = x_len * y_len * z_len * sizeof(double);
  double *dat = (double*)malloc(numPt * sizePt * sizeof(double));
  double *out = (double*)malloc(sizeOut);
  memset(out, 0, sizeOut);

  int vecSize = binread(argv[1], dat);
  //printf(“bin read %d %d %d\n", x_len, y_len, z_len);

  timespec time1, time2;
  clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time1);

  //vol1(vecSize, dat, out);
  // vol_61(vecSize, dat, out);
  vol_6n(3, vecSize, dat, out, -0.4, 0.2);

  clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time2);
  printf("%d, sec=%ld, nsec=%ld \n", vecSize, diff(time1,time2).tv_sec, diff(time1,time2).tv_nsec);

  free(out);
  free(dat);
  return 0;
}
