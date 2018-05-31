import random
import string
import tesserocr
import time
import os
import numpy as np

import matplotlib.pyplot as plt
from PIL import Image
from claptcha import Claptcha

import Configure as Configs

def generate_claptcha(text, name, noise=0.0):
	c = Claptcha(text, "FreeMono.ttf", noise=noise)
	c.write(name)

def binarizing(image, threshold=140):
	img = Image.open(image)
	img = img.convert("L")
	img = img.resize((img.width*2, img.height*2))

	for w in range(img.width):
		for h in range(img.height):
			if img.getpixel((w,h)) < threshold:
				img.putpixel((w,h),0)
			else:
				img.putpixel((w,h),255)

	newname = "binarized_"+image
	img.save(newname)

	return newname

def depoint(image, threshold=245):
    img = Image.open(image)
    img = img.convert("L")
    w, h = img.size
    for y in range(1, h-1):
        for x in range(1, w-1):
            count = 0
            if img.getpixel((x,y-1)) > threshold:
                count = count + 1
            if img.getpixel((x,y+1)) > threshold:
                count = count + 1
            if img.getpixel((x-1,y)) > threshold:
                count = count + 1
            if img.getpixel((x+1,y)) > threshold:
                count = count + 1
            if img.getpixel((x-1,y-1)) > threshold:
                count = count + 1
            if img.getpixel((x-1,y+1)) > threshold:
                count = count + 1
            if img.getpixel((x+1,y-1)) > threshold:
                count = count + 1
            if img.getpixel((x+1,y+1)) > threshold:
                count = count + 1
            if count > 4:
                img.putpixel((x,y),255)


    img.save(image)
    return image

def generate_figure_flatten(name):
	img = Image.open(name)
	img = img.convert("L")
	
	data = []
	for x in range(img.width):
		for y in range(img.height):
			data.append(img.getpixel((x,y)))

	plt.figure("{0:s} - Hist".format(name))
	ar = np.array(data).flatten() 
	plt.hist(ar, bins = 256)
	plt.show()


if __name__ == "__main__":
	#for i in range(20):
	#	a = random.randint(1,2000)
	#	b = random.randint(1,9)
	#	generate_claptcha(str(a), 'collection/'+str(a) + '.png', b/10)
	name = 'out.png'
	#generate_figure_flatten(name)
	name = binarizing(name, 240)
	n = 15
	while n > 0:
		name = depoint(name)
		n = n - 1
	#print (name)
	#img = Image.open(name)
	
	#print (tesserocr.image_to_text(img))
	