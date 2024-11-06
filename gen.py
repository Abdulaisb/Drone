import math

def m_to_lat(s_lat, s_lon, d_north, d_east):
    earth_rad = 6378137.0 # metters
    delta_lat = d_north / earth_rad
    new_lat = s_lat + math.degrees(delta_lat)
    
    delta_lon = d_east / (earth_rad*math.cos(math.radians(s_lat)))
    new_lon  = s_lon + math.degrees(delta_lon)
    return new_lat, new_lon
def fertilization(start_lat,start_lon, alt, width, height, crosses):
    constant = "0\t3\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t"
    points = []
    points.append(("1\t" + constant + "{:.8f}\t{:.8f}\t-1.000000\t1").format(start_lat, start_lon))
    for i in range(crosses):
        # One cross means going from left to right
        # then up for height/crosses
        # then left
        # then up
        y1 = i * height/crosses
        y2 = y1 + (height/crosses)/2
        y3 = y1 + (height/crosses)
        lat1, lon1 = m_to_lat(start_lat,start_lon,y1,width)
        lat2, lon2 = m_to_lat(start_lat,start_lon,y2,width)
        lat3, lon3 = m_to_lat(start_lat,start_lon,y2,0)
        lat4, lon4 = m_to_lat(start_lat,start_lon,y3,0)
        points.append("{}\t{}{:.8f}\t{:.8f}\t{:.6f}\t1".format(i*4+2, constant, lat1, lon1,alt))
        points.append("{}\t{}{:.8f}\t{:.8f}\t{:.6f}\t1".format(i*4+3, constant, lat2, lon2,alt))
        points.append("{}\t{}{:.8f}\t{:.8f}\t{:.6f}\t1".format(i*4+4, constant, lat3, lon3,alt))
        points.append("{}\t{}{:.8f}\t{:.8f}\t{:.6f}\t1".format(i*4+5, constant, lat4, lon4,alt)) 
    latf,lonf = m_to_lat(start_lat,start_lon,height,width)
    points.append("{}\t{}{:.8f}\t{:.8f}\t{:.6f}\t1".format(crosses*4+2, constant, latf, lonf,alt)) 
    return points

output = open("output.waypoints", "w")
output.write("QGC WPL 110\n")
output.write("0\t1\t0\t0\t0\t0\t0\t0\t0\t0\t0\t1\n")


start_latitude = 30.6427363
start_longitude = -96.3001643
altitude = 100

waypoints = fertilization(start_latitude,start_longitude,altitude,70,100,8)

for w in waypoints:
    output.write(w + "\n")
output.close()