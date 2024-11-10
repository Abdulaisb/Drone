import math

def m_to_lat(s_lat, s_lon, d_north, d_east):
    earth_rad = 6378137.0  # meters
    delta_lat = d_north / earth_rad
    new_lat = s_lat + math.degrees(delta_lat)

    delta_lon = d_east / (earth_rad * math.cos(math.radians(s_lat)))
    new_lon = s_lon + math.degrees(delta_lon)
    return new_lat, new_lon

def circular_pattern(start_lat, start_lon, alt, radius, passes, waypoints_per_pass):
    constant = "0\t3\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t"
    points = []
    points.append("1\t" + constant + "{:.8f}\t{:.8f}\t-1.000000\t1".format(start_lat, start_lon))

    waypoint_id = 2  # start from ID 2 as 1 is the home point
    for p in range(passes):
        current_radius = radius * (p + 1) / passes  # incremental radius
        for w in range(waypoints_per_pass):
            angle = (2 * math.pi / waypoints_per_pass) * w  # divide the circle evenly
            d_north = current_radius * math.cos(angle)
            d_east = current_radius * math.sin(angle)
            lat, lon = m_to_lat(start_lat, start_lon, d_north, d_east)
            points.append("{}\t{}{:.8f}\t{:.8f}\t{:.6f}\t1".format(waypoint_id, constant, lat, lon, alt))
            waypoint_id += 1  # increment waypoint ID for each new point

    return points

# Example usage:
output = open("circular_output.waypoints", "w")
output.write("QGC WPL 110\n")
output.write("0\t1\t0\t0\t0\t0\t0\t0\t0\t0\t0\t1\n")

start_latitude = 30.6427363
start_longitude = -96.3001643
altitude = 100
radius = 50  # radius in meters
passes = 5  # number of circular passes
waypoints_per_pass = 12  # number of waypoints per circular pass

waypoints = circular_pattern(start_latitude, start_longitude, altitude, radius, passes, waypoints_per_pass)

for w in waypoints:
    output.write(w + "\n")
output.close()
