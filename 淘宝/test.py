import random

def get_track(distance):  
	track = []

	current = 0
	mid = distance * 3 / 4
	t = 0.2
	v = 0
	while current < distance:
		if current < mid:
			a = 2
		else:
			a = -3
		v0 = v
		v = v0 + a * t
		move = v0 * t + 1 / 2 * a * t * t
		current += move
		track.append(round(move))
	return track

def get_track_from_GM():
	file = open("human.gms")
	x, y = 1176, 413
	res = []
	while True:
		line = file.readline().strip()

		if not line:
			break

		data = line.split(" ")
		pos = (int(data[0])-x, int(data[1])-y, random.randint(0,10)*0.01)
		res.append(pos)
		
	file.close()
	return res

if __name__ == "__main__":
	res = get_track_from_GM()
	print (res)