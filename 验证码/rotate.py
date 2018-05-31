import numpy as np
import cv2

def rotation(name):
	img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
	cv2.imshow("dasd", img)

	# 灰度图和二值化
	#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
	#ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY) 

	# 反转图片
	img = cv2.bitwise_not(img)
	
	thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	coords = np.column_stack(np.where(thresh > 0))
	rect = cv2.minAreaRect(coords)
	angle = rect[-1]
	
	if angle < -45:
		angle = -(90+angle)
	else:
		angle = -angle

	rows, cols = img.shape[:2]
  	
  	# 旋转angle角度
	M = cv2.getRotationMatrix2D((cols // 2, rows // 2), angle, 1.0)  
	img = cv2.warpAffine(img, M, (cols, rows))

	# 再次反转图片
	img = cv2.bitwise_not(img)

	cv2.imwrite("Rotated_"+ name, img)

if __name__ == '__main__':
	rotation('4-binarized_1781.png')