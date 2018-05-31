from PIL import Image
import numpy as np

img_array = [[1,0,0,0,0],
				[0,1,0,1,1],
				[1,1,1,0,0],
				[0,0,1,1,1]]
width = len(img_array[0])
height = len(img_array)
res = [None] * width

def parser(image):
	global img_array, width, height, res
	img = Image.open(image)
	img_array = np.array(img)
	width = len(img_array[0])
	height = len(img_array)
	res = [None] * width

def getLine(n):
	if n == width:
		for i in range(width):
			print (res[i], end=' ')
		print ()
		return

	if n == 0:
		for j in range(height):
			if img_array[j][0] == 1:
				res[0] = j
				getLine(n+1)

	if n > 0:
		p = res[n-1]
		if res[n-1] > 0 and img_array[res[n-1]-1][n] == 1:
			res[n] = res[n-1] - 1
			getLine(n+1)

		res[n-1] = p
		if img_array[res[n-1]][n] == 1:
			res[n] = res[n-1]
			getLine(n+1)

		res[n-1] = p
		if res[n-1] < height - 1 and img_array[res[n-1]+1][n] == 1:
			res[n] = res[n-1] + 1
			getLine(n+1)


if __name__ == "__main__":
	parser("binarized_image.png")
	getLine(0)