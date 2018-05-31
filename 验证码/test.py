import math

def track(distance):
    track = []
    current = 0
    slow = distance * 0.8 # 接近结束的时候减速

    t = t1 = 0.2
    v0 = 0
    # x = v0t + 1/2 * a * t^2
    # v = v0 + at
    v02 = math.sqrt(slow*4)
    print (slow, v02)
    while current < distance:
        if current < slow:
            a = 2
            v = v0 + a * t  
            s = v0 * t + a * t**2 // 2 
            current = s
            t += 0.2
            track.append(int(current))
        else:    
            a = -3
            v = v02 + a * t1
            s = slow + v02 * t1 + a * t1**2 // 2
            current = s
            t1 += 0.2
            track.append(int(current))
    return track

print (track(500))