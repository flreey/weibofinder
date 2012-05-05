from math import *

EARTH_RADIUS_METER = 6378137.0

def hav(t):
    return pow(sin(t/2), 2)

def cal_distance(flat, flng, tlat, tlng):
    """caculate the spherical distance of two points """
    flat = radians(flat)
    flng = radians(flng)
    tlat = radians(tlat)
    tlng = radians(tlng)

    dlng = fabs(flng - tlng)
    dlat = fabs(flat - tlat)
    h = hav(dlat) + cos(flat) * cos(tlat) * hav(dlng)
    return 2 * EARTH_RADIUS_METER * asin(sqrt(h))

def offset_lng(lat, distance):
    return 2 * asin(sin(distance / (2 * EARTH_RADIUS_METER)) / cos(lat))

def offset_lat(distance):
    return distance / EARTH_RADIUS_METER

def get_offset_cube(lat, lng, distance):
    #distance = distance
    off_lng = fabs(offset_lng(lat, distance))
    off_lat = fabs(offset_lat(distance))
    left_top = lat + off_lat, lng - off_lng
    right_top = lat + off_lat, lng + off_lng
    left_bottom = lat - off_lat, lng - off_lng
    right_bottom = lat - off_lat, lng + off_lng
    r = lambda x:(round(x[0], 4), round(x[1], 4))

    return r(left_top), r(right_top), r(left_bottom), r(right_bottom)

def main():
    import sys
    if len(sys.argv) < 5:
        print 'not enough params'
        sys.exit(0)
    #fp = [float(r) for r in sys.argv[1:3]]
    #tp = [float(r) for r in sys.argv[3:5]]
    ps = [float(r) for r in sys.argv[1:5]]
    print cal_distance(ps[0], ps[1], ps[2], ps[3])
    print get_offset_cube(ps[0], ps[1], 500)
    #left_top = fp

if __name__ == '__main__':
    main()
