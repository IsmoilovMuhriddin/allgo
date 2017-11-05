/**********************************************************************************************
* OpenCV-3.0.0 RASPIAN [TO DO] version
**********************************************************************************************/

#include "opencv2/opencv.hpp"  
#include "opencv2/imgproc.hpp"
#include <iostream>

/* TO DO: Include the raspicam headerfile */



using namespace std;
using namespace cv;

// Function headers
int processImgR(Mat);
int processImgG(Mat);
bool isIntersected(Rect, Rect);

// Global variables
bool isFirstDetectedR = true;
bool isFirstDetectedG = true;
Rect* lastTrackBoxR;
Rect* lastTrackBoxG;
int lastTrackNumR;
int lastTrackNumG;

int main()
{
	int redCount = 0;
	int greenCount = 0;

	Mat frame;
	Mat img;
	Mat imgYCrCb;
	Mat imgGreen;
	Mat imgRed;

	// Parameters of brightness
	double a = 0.3; // gain, modify this only.
	double b = (1 - a) * 125; // bias
	
/*


TO DO: Input Video Capturing code is commented- REPLACE IT WITH RASPICAM INPUT VIDEO CAPTURING FUNCTIONS

Hint: We discussed this before in the class once

	//	VideoCapture capture(0);
	//	if (!capture.isOpened())
	//	{
	//		cout << "Start device failed!\n" << endl;
	//		return -1;
	//	} 
	
	// while (1)
	// {
		// capture >> frame;
			
*/


		// Adjust the brightness
		frame.convertTo(img, img.type(), a, b);

		// Convert to YCrCb color space
		cvtColor(img, imgYCrCb, CV_BGR2YCrCb);

		imgRed.create(imgYCrCb.rows, imgYCrCb.cols, CV_8UC1);
		imgGreen.create(imgYCrCb.rows, imgYCrCb.cols, CV_8UC1);

		// Split three components of YCrCb
		vector<Mat> planes;
		split(imgYCrCb, planes);
		// Traversing to split the color of RED and GREEN according to the Cr component
		MatIterator_<uchar> it_Cr = planes[1].begin<uchar>(),
			it_Cr_end = planes[1].end<uchar>();
		MatIterator_<uchar> it_Red = imgRed.begin<uchar>();
		MatIterator_<uchar> it_Green = imgGreen.begin<uchar>();

		for (; it_Cr != it_Cr_end; ++it_Cr, ++it_Red, ++it_Green)
		{
			// RED, 145<Cr<470 
			if (*it_Cr > 145 && *it_Cr < 470)
				*it_Red = 255;
			else
				*it_Red = 0;

			// GREEN£¬95<Cr<110
			if (*it_Cr > 95 && *it_Cr < 110)
				*it_Green = 255;
			else
				*it_Green = 0;
		}

		//Expansion and corrosion  
		dilate(imgRed, imgRed, Mat(15, 15, CV_8UC1), Point(-1, -1));
		erode(imgRed, imgRed, Mat(1, 1, CV_8UC1), Point(-1, -1));
		dilate(imgGreen, imgGreen, Mat(15, 15, CV_8UC1), Point(-1, -1));
		erode(imgGreen, imgGreen, Mat(1, 1, CV_8UC1), Point(-1, -1));

		redCount = processImgR(imgRed);
		greenCount = processImgG(imgGreen);
		cout << "red:" << redCount << ";  " << "green:" << greenCount << endl;

		imshow("Origin", frame);
		imshow("Red", imgRed);
		imshow("Green", imgGreen);

		// Handle with the keyboard input
		if (cvWaitKey(20) == 'q')
			break;
	}

/* TO DO: Release the captured frame from raspicam*/



	return 0;
}

int processImgR(Mat src)
{
	Mat tmp;

	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	vector<Point> hull;

	CvPoint2D32f tempNode;
	CvMemStorage* storage = cvCreateMemStorage();
	CvSeq* pointSeq = cvCreateSeq(CV_32FC2, sizeof(CvSeq), sizeof(CvPoint2D32f), storage);

	Rect* trackBox;
	Rect* result;
	int resultNum = 0;

	int area = 0;

	src.copyTo(tmp);
	// Extract the contour
	findContours(tmp, contours, hierarchy, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE);

	if (contours.size() > 0)
	{
		trackBox = new Rect[contours.size()];
		result = new Rect[contours.size()];

		// Determine the area to track
		for (int i = 0; i < contours.size(); i++)
		{
			cvClearSeq(pointSeq);
			// Get the point set of the convex hull
			convexHull(Mat(contours[i]), hull, true);
			int hullcount = (int)hull.size();
			// Save points of the convex hull
			for (int j = 0; j < hullcount - 1; j++)
			{
				tempNode.x = hull[j].x;
				tempNode.y = hull[j].y;
				cvSeqPush(pointSeq, &tempNode);
			}

			trackBox[i] = cvBoundingRect(pointSeq);
		}

		if (isFirstDetectedR)
		{
			lastTrackBoxR = new Rect[contours.size()];
			for (int i = 0; i < contours.size(); i++)
				lastTrackBoxR[i] = trackBox[i];
			lastTrackNumR = contours.size();
			isFirstDetectedR = false;
		}
		else
		{
			for (int i = 0; i < contours.size(); i++)
			{
				for (int j = 0; j < lastTrackNumR; j++)
				{
					if (isIntersected(trackBox[i], lastTrackBoxR[j]))
					{
						result[resultNum] = trackBox[i];
						break;
					}
				}
				resultNum++;
			}
			delete[] lastTrackBoxR;
			lastTrackBoxR = new Rect[contours.size()];
			for (int i = 0; i < contours.size(); i++)
			{
				lastTrackBoxR[i] = trackBox[i];
			}
			lastTrackNumR = contours.size();
		}

		delete[] trackBox;
	}
	else
	{
		isFirstDetectedR = true;
		result = NULL;
	}
	cvReleaseMemStorage(&storage);

	if (result != NULL)
	{
		for (int i = 0; i < resultNum; i++)
		{
			area += result[i].area();
		}
	}
	delete[] result;

	return area;
}

int processImgG(Mat src)
{
	Mat tmp;

	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	vector< Point > hull;

	CvPoint2D32f tempNode;
	CvMemStorage* storage = cvCreateMemStorage();
	CvSeq* pointSeq = cvCreateSeq(CV_32FC2, sizeof(CvSeq), sizeof(CvPoint2D32f), storage);

	Rect* trackBox;
	Rect* result;
	int resultNum = 0;

	int area = 0;

	src.copyTo(tmp);
	// Extract the contour
	findContours(tmp, contours, hierarchy, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE);

	if (contours.size() > 0)
	{
		trackBox = new Rect[contours.size()];
		result = new Rect[contours.size()];

		// Determine the area to track
		for (int i = 0; i < contours.size(); i++)
		{
			cvClearSeq(pointSeq);
			// Get the point set of the convex hull
			convexHull(Mat(contours[i]), hull, true);
			int hullcount = (int)hull.size();
			// Save points of the convex hull
			for (int j = 0; j < hullcount - 1; j++)
			{
				//line(showImg, hull[j + 1], hull[j], Scalar(255, 0, 0), 2, CV_AA);
				tempNode.x = hull[j].x;
				tempNode.y = hull[j].y;
				cvSeqPush(pointSeq, &tempNode);
			}

			trackBox[i] = cvBoundingRect(pointSeq);
		}

		if (isFirstDetectedG)
		{
			lastTrackBoxG = new Rect[contours.size()];
			for (int i = 0; i < contours.size(); i++)
				lastTrackBoxG[i] = trackBox[i];
			lastTrackNumG = contours.size();
			isFirstDetectedG = false;
		}
		else
		{
			for (int i = 0; i < contours.size(); i++)
			{
				for (int j = 0; j < lastTrackNumG; j++)
				{
					if (isIntersected(trackBox[i], lastTrackBoxG[j]))
					{
						result[resultNum] = trackBox[i];
						break;
					}
				}
				resultNum++;
			}
			delete[] lastTrackBoxG;
			lastTrackBoxG = new Rect[contours.size()];
			for (int i = 0; i < contours.size(); i++)
			{
				lastTrackBoxG[i] = trackBox[i];
			}
			lastTrackNumG = contours.size();
		}

		delete[] trackBox;
	}
	else
	{
		isFirstDetectedG = true;
		result = NULL;
	}
	cvReleaseMemStorage(&storage);

	if (result != NULL)
	{
		for (int i = 0; i < resultNum; i++)
		{
			area += result[i].area();
		}
	}
	delete[] result;

	return area;
}

// Determine whether the two rectangular areas are intersected 
bool isIntersected(Rect r1, Rect r2)
{
	int minX = max(r1.x, r2.x);
	int minY = max(r1.y, r2.y);
	int maxX = min(r1.x + r1.width, r2.x + r2.width);
	int maxY = min(r1.y + r1.height, r2.y + r2.height);

	if (minX < maxX && minY < maxY)
		return true;
	else
		return false;
}

//// Compile :
/* g++ trafficLightDetect_RaspianPorted.cpp -I/usr/local/include -L/usr/local/lib -L/opt/vc/lib -lraspicam -lraspicam_cv -lmmal -lmmal_core -lmmal_util `pkg-config --cflags --libs opencv` */