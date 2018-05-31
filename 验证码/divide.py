from PIL import Image

def divide1(name, threshold = 0):
	img = Image.open(name)

	width, height = img.size

	feature = [0] * width

	for x in range(width):
		cnt = 0
		for y in range(height):
			if img.getpixel((x,y)) == 0:
				cnt += 1

		if cnt > threshold:
			feature[x] = 1 # = cnt

	flag = 0
	length = 0
	x_left = 0
	res = []
	for i in range(len(feature)):
		if feature[i] == 1:
			if flag == 0:
				flag = 1
				x_left = i
				length = 1
			else:
				length += 1
		else:
			if flag == 1:
				res.append((x_left, length,))
				x_left = 0
				flag = 0
			else:
				pass
	# res = [(46, 50), (116, 46), (208, 56), (290, 48)]
		
	max_length = max([x[1] for x in res])
	cnt = 1
	for info in res:
		newimg = Image.new('1', (max_length, height), 255)
		#newimg.show()

		seg = img.crop((info[0],0,info[0]+info[1],height,))
		newimg.paste(seg, ((max_length-info[1])//2, 0))
		newimg.save(str(cnt) +'-'+name)
		cnt += 1

def divide2(name):
	img = Image.open(name)

	width, height = img.size

	feature = [0] * width

	for x in range(width):
		cnt = 0
		for y in range(height):
			if img.getpixel((x,y)) == 0:
				cnt += 1
		feature[x] = cnt

	average = width//3
	f = width//50
	res1 = min([x for x in range(average-f, average+f)])
	res2 = min([x for x in range(average*2-f, average*2+f)])
	print (res1, res2)

	newimg = Image.new('1', (res1, height), 255)
	seg = img.crop((0,0,res1,height,))
	newimg.paste(seg, (0, 0))
	newimg.save('1_'+name)

	newimg2 = Image.new('1', (res2-res1, height), 255)
	seg = img.crop((res1,0,res2,height,))
	newimg2.paste(seg, (0, 0))
	newimg2.save('2_'+name)

	newimg3 = Image.new('1', (width-res2, height), 255)
	seg = img.crop((res2,0,width,height,))
	newimg3.paste(seg, (0, 0))
	newimg3.save('3_'+name)


if __name__ == '__main__':
	#divide1('binarized_out.png', 0)

	divide2("2-binarized_out.png")