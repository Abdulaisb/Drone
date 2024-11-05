import math

def m_to_lat(s_lat, s_lon, d_north, d_east):
    earth_rad = 6378137.0 # metters
    delta_lat = d_north / earth_rad
    new_lat = s_lat + math.degrees(delta_lat)
    
    delta_lon = d_east / (earth_rad*math.cos(math.radians(s_lat)))
    new_lon  = s_lon + math.degrees(delta_lon)
    return new_lat, new_lon

output = open("output.waypoints", "w")
output.write("QGC\tWPL\t110\n")
output.write("0\t1\t0\t0\t0\t0\t0\t0\t0\t0\t0\t1\n")
constant = "0\t3\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t"


start_lat = 30.64259670
start_lon = -96.29951120
# field dimensions
width = 10
height = 30
crosses = 4
for i in range(crosses):
    # One cross means going from left to right
    # then up for height/crosses
    # then left
    # then up
    y1 = i * height/crosses
    y2 = y1 + (height/crosses)/2
    y3 = y1 + (height/crosses)
    lat1, lon1 = m_to_lat(start_lat,start_lon,y1,width)
    
    
    


waypoints = []
waypoints.append("1\t" + constant + str(start_lat) + "\t" + str(start_lon) + "\t-1.000000\t1")



for w in waypoints:
    output.write(w + "\n")
output.close()