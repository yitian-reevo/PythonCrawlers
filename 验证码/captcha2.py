from PIL import Image
import numpy as np

img_array = [[1,0,0,0,0],
				[0,1,0,1,1],
				[1,1,1,0,0],
				[0,0,1,1,1]]
width = len(img_array[0])
height = len(img_array)
flag_array = [[False] * width ] * height
res = [-1] * width
offset = 0
threshold = 20

def parser(image):
	global img_array, width, height, res, offset
	img = Image.open(image)
	img_array = np.array(img)

	width = len(img_array[0])
	height = len(img_array)
	flag_array = [[False] * width ] * height

	for i in range(width):
		for j in range(height):
			if img_array[j][i] == 255:
				img_array[j][i] = 0
			else:
				img_array[j][i] = 1
	'''
		for i in range(width):
			flag = 0
			for j in range(height):
				if img_array[j][i] != 0:
					flag = 1
					break

			if flag == 1:
				offset = i
				break
	'''	
	res = [-1] * width

def display(n):
	for i in range(n):
		print (res[i], end=' ')
	print()

def getLine(n):
	if n < offset:
		res[n] = -1
		getLine(n+1)

	if n == width:
		display(width)
		return

	if n == offset:
		for j in range(height):
			if img_array[j][offset] == 1 and flag_array[j][offset] == False:
				flag_array[j][offset] = True
				res[offset] = j
				getLine(n+1)

	if n > 0 and n < width:
		hasMore = 0

		if res[n-1] > 0 and res[n-1] < height and img_array[res[n-1]][n] == 1 and flag_array[res[n-1]][n] == False:
			flag_array[res[n-1]][n] = True
			hasMore = 1
			res[n] = res[n-1]
			getLine(n+1)
	
		if res[n-1] > 0 and img_array[res[n-1]-1][n] == 1 and flag_array[res[n-1]-1][n] == False:
			flag_array[res[n-1]-1][n] = True
			res[n] = res[n-1] - 1				
			hasMore = 1
			getLine(n+1)

		if res[n-1] < height - 1 and img_array[res[n-1]+1][n] == 1 and flag_array[res[n-1]+1][n] == False:
			flag_array[res[n-1]+1][n] = True
			hasMore = 1
			res[n] = res[n-1] + 1
			getLine(n+1)

		if (hasMore == 0):
			display(n)

if __name__ == "__main__":
	#parser("binarized_image.png")
	#with open('asd.txt', 'w') as file:
	#	for i in range(height):
	#		for j in range(width):
	#			file.write(str(img_array[i][j]).strip())
	#			file.write(',')
	getLine(0)