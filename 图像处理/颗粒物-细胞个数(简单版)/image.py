# -*- coding: utf-8 -*-
import cv2
def eleCounter(Path):
	#预处理
	img = cv2.imread(Path)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gauss = cv2.GaussianBlur(gray,(7,7),0)
	_,threshed = cv2.threshold(gauss,175,255,cv2.THRESH_BINARY_INV)
	#形态学出来
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	morphed = cv2.morphologyEx(threshed,cv2.MORPH_OPEN,kernel,None,(-1,-1),1)
	#边缘处理
	_,cnts,_ = cv2.findContours(morphed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	canvas = img.copy()
	cv2.drawContours(canvas,cnts,-1,(100,20,100),1)
	#计数
	xcnts = []
	for cnt in cnts:
		area = cv2.contourArea(cnt)
		x,y,w,h = cv2.boundingRect(cnt)
		if area < 7 or area/(w*h)<0.3:
			continue
			xcnts.append(cnt)

	cv2.drawContours(canvas,xcnts,-1,(0,0,255),2)
	print("cells nums:{}/{}".format(len(xcnts),len(cnts)))

	#显示图像s
	cv2.imshow("src",img)
	cv2.imshow("Gray",gray)
	cv2.imshow("Gauss",gauss)
	cv2.imshow("Binarization",threshed)
	cv2.imshow("Open",morphed)
	cv2.imshow("dst",canvas)
	cv2.waitKey()
	cv2.destroyAllWindows()
	return xcnts
print(eleCounter(r"C:/Users/Lenovo/Desktop/test2.jpg"))


