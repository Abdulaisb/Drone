import math

# Command Preambles
waypoint = "0\t3\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t"
takeoff = "0\t3\t22\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t"
land = "0\t3\t21\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t"
yaw_command = "0\t3\t115\t"

def m_to_lat(s_lat, s_lon, d_north, d_east):
    earth_rad = 6378137.0  # Earth's radius in meters
    delta_lat = d_north / earth_rad
    new_lat = s_lat + math.degrees(delta_lat)
    
    delta_lon = d_east / (earth_rad * math.cos(math.radians(s_lat)))
    new_lon = s_lon + math.degrees(delta_lon)
    return new_lat, new_lon

def courier(start_lat, start_lon, alt, targetx, targety):
    points = []
    # Takeoff
    points.append(f"1\t{takeoff}{start_lat:.8f}\t{start_lon:.8f}\t{alt:.6f}\t1")
    # Spin 3 times
    yaw_steps = 12  # Steps per spin
    total_yaw_angle = 360 * 3  # 3 Rotations
    yaw_rate = 30  # Degrees per second
    for i in range(yaw_steps):
        yaw_angle = (total_yaw_angle / yaw_steps) * (i + 1)
        points.append(f"{len(points) + 1}\t{yaw_command}{yaw_angle:.6f}\t{yaw_rate:.6f}\t1\t0.000000\t1")
    # Go to target location
    t_lat, t_lon = m_to_lat(start_lat, start_lon, targetx, targety)
    points.append(f"{len(points) + 1}\t{waypoint}{t_lat:.8f}\t{t_lon:.8f}\t{alt:.6f}\t1")
    # Approach Target
    points.append(f"{len(points) + 1}\t{waypoint}{t_lat:.8f}\t{t_lon:.8f}\t{1:.6f}\t1")
    # Spin 3 times
    for i in range(yaw_steps):
        yaw_angle = (total_yaw_angle / yaw_steps) * (i + 1)
        points.append(f"{len(points) + 1}\t{yaw_command}{yaw_angle:.6f}\t{yaw_rate:.6f}\t1\t0.000000\t1")
    # Return to start
    points.append(f"{len(points) + 1}\t{waypoint}{start_lat:.8f}\t{start_lon:.8f}\t{alt:.6f}\t1")
    # Land at start
    points.append(f"{len(points) + 1}\t{land}{start_lat:.8f}\t{start_lon:.8f}\t0.000000\t1")
    
    return points

def fertilization(start_lat, start_lon, alt, width, height, crosses):
    points = []
    points.append(f"1\t{takeoff}{start_lat:.8f}\t{start_lon:.8f}\t{alt:.6f}\t1")
    
    # Generate fertilization pattern waypoints
    for i in range(crosses):
        y1 = i * height / crosses
        y2 = y1 + (height / crosses) / 2
        y3 = y1 + (height / crosses)
        
        lat1, lon1 = m_to_lat(start_lat, start_lon, y1, width)
        lat2, lon2 = m_to_lat(start_lat, start_lon, y2, width)
        lat3, lon3 = m_to_lat(start_lat, start_lon, y2, 0)
        lat4, lon4 = m_to_lat(start_lat, start_lon, y3, 0)
        
        points.append(f"{i*4+2}\t{waypoint}{lat1:.8f}\t{lon1:.8f}\t{alt:.6f}\t1")
        points.append(f"{i*4+3}\t{waypoint}{lat2:.8f}\t{lon2:.8f}\t{alt:.6f}\t1")
        points.append(f"{i*4+4}\t{waypoint}{lat3:.8f}\t{lon3:.8f}\t{alt:.6f}\t1")
        points.append(f"{i*4+5}\t{waypoint}{lat4:.8f}\t{lon4:.8f}\t{alt:.6f}\t1")

    latf, lonf = m_to_lat(start_lat, start_lon, height, width)
    points.append(f"{crosses*4+2}\t{waypoint}{latf:.8f}\t{lonf:.8f}\t{alt:.6f}\t1")
    points.append(f"{crosses*4+3}\t{land}{start_lat:.8f}\t{start_lon:.8f}\t0.000000\t1")
    
    return points

# Write waypoints to output file
output = open("output.waypoints", "w")
output.write("QGC WPL 110\n")
output.write("0\t1\t0\t0\t0\t0\t0\t0\t0\t0\t0\t1\n")
# Veteran's Field Coordinates
start_latitude = 30.6427363
start_longitude = -96.3001643
altitude = 15
# Courier Mission
waypoints = courier(start_latitude, start_longitude, altitude, 15, 10)

for w in waypoints:
    output.write(w + "\n")
output.close()
