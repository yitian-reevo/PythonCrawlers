from PIL import Image

def recovery(name):
	img = Image.open(name)

	a = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12,
			13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
	print (len(a))
	im_new = Image.new("RGB", (260, 116))
	for row in range(2):
		for column in range(26):
			right = a[row * 26 + column] % 26 * 12 + 1
			down = 58 if a[row * 26 + column] > 25 else 0
			print (a[row * 26 + column], '!', row, column, right, down)
			for w in range(10):
				for h in range(58):
					ht = 58 * row + h
					wd = 10 * column + w

					print ("#", wd,ht, w+right, h+down)
					im_new.putpixel((wd, ht), img.getpixel((w + right, h + down)))


	im_new.show()

if __name__ == "__main__":
	recovery("yzm-6-wanzheng.jpg")