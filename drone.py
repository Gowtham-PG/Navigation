#!/usr/bin/python3.6

import time
import argparse
import json
import subprocess
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import sin, cos, sqrt, atan2, radians
from pymavlink import mavutil
import subprocess
import os
import piexif


file=open("/home/airosspace/Navigation/flight_log.txt","w")
file.write("-------------------------------------------------------------------------------------------\n")



def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())


def shutter(i):
    file_path = f"../Desktop/JetsonYolov5-main/images/droneim{i}.jpg"
    command = f"gphoto2 --capture-image-and-download --filename {file_path}"

    return_code = os.system(command)
    print(f"Return Code: {return_code}")
    file.write(f"{time_stamp()} shutter function: {return_code}\n")



'''def shutter(i):
    command=["gphoto2", "--capture-image-and-download", "--filename", f"../Desktop/JetsonYolov5-main/images/droneim{i}.jpg"]
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    
    print(stderr)
    return_code = process.returncode
    print(return_code)
    file.write(time_stamp() + " shutter function:" + str(return_code) + "")
'''

def insert_location_data(image_path, latitude, longitude):
    exif_dict = piexif.load(image_path)
    if "GPS" not in exif_dict:
        exif_dict["GPS"] = {}
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = _convert_to_dms(latitude)
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = _convert_to_dms(longitude)
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)
    file.write(time_stamp() + " exif added successfully\n")
    print("exif added successfully\n")


def _convert_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = int(((decimal_degrees - degrees) * 60 - minutes) * 60)
    return ((degrees, 1), (minutes, 1), (seconds, 1))



def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    file.write(time_stamp() + " Basic pre-arm checks\n")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        file.write(time_stamp() + " Waiting for vehicle to initialize...\n")
        time.sleep(1)

    print("Arming motors")
    file.write(time_stamp() + " Arming motors\n")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        file.write(time_stamp() + " Waiting for arming...\n")
        time.sleep(1)

    print("Taking off!")
    file.write(time_stamp() + " Taking off!\n")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        file.write(" Altitude: " + str(vehicle.location.global_relative_frame.alt) + "\n")
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            file.write(time_stamp() + " Reached target altitude\n")
            break
        time.sleep(1)


def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of Earth in meters
    R = 6371000

    # convert coordinates to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # calculate the differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # apply Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # calculate the distance
    distance = R * c
    return distance









parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

vehicle = connect(connection_string, wait_ready=True)





arm_and_takeoff(10)

#print("Set default/target airspeed to 3")
file.write(time_stamp() + " Set default/target airspeed to 3\n")
vehicle.airspeed = 10

waypoints = []

with open('optimal_path.json', 'r') as file:
    data = json.load(file)
    waypoints_data = data['waypoints']
    for waypoint_data in waypoints_data:
        waypoint = LocationGlobalRelative(waypoint_data['latitude'], waypoint_data['longitude'], waypoint_data['altitude'])
        waypoints.append(waypoint)
counter=0

print(waypoints)
#file.write(time_stamp() + str(waypoints))


for waypoint in waypoints:	  
    vehicle.simple_goto(waypoint, groundspeed=10)
    while vehicle.mode.name == "GUIDED":  # Wait for the drone to reach the waypoint
        file=open("/home/airosspace/Navigation/flight_log.txt","a")
        remaining_distance = calculate_distance(
            vehicle.location.global_relative_frame.lat,
            vehicle.location.global_relative_frame.lon,
            waypoint.lat,
            waypoint.lon
        )
        print("Distance to waypoint: ", remaining_distance)
        #file.write(time_stamp() +" Distance to waypoint: " + str(remaining_distance))
        if remaining_distance <= 1:  # Check if the drone has reached the waypoint
            print("Reached waypoint")
            file.write(time_stamp() + " Reached waypoint\n")   
            shutter(counter)
            time.sleep(3)
            print(waypoints)
            try:
                print(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
                insert_location_data(f"../Desktop/JetsonYolov5-main/images/droneim{counter}.jpg",vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
                os.rename(f"../Desktop/JetsonYolov5-main/images/droneim{counter}.jpg",f"../Desktop/JetsonYolov5-main/captured/droneim{counter}.jpg")
                counter+=1
                break
            except Exception as err:
                print(err)
                os.rename(f"../Desktop/JetsonYolov5-main/images/droneim{counter}.jpg",f"../Desktop/JetsonYolov5-main/captured/droneim{counter}.jpg")
                counter+=1		
                break
        #time.sleep(1)

new_latitude = 12.9712318
new_longitude = 80.0440130
new_altitude = 10

# Create a new waypoint
new_waypoint = LocationGlobalRelative(new_latitude, new_longitude, new_altitude)

# Append the new waypoint to the list
waypoints.append(new_waypoint)

# Go to the additional waypoint
vehicle.simple_goto(new_waypoint, groundspeed=10)
while vehicle.mode.name == "GUIDED":
    remaining_distance = calculate_distance(
        vehicle.location.global_relative_frame.lat,
        vehicle.location.global_relative_frame.lon,
        new_waypoint.lat,
        new_waypoint.lon
    )
    print("Distance to additional waypoint: ", remaining_distance)
    file.write(time_stamp() + " Distance to additional waypoint: " + str(remaining_distance) + "\n")
    if remaining_distance <= 1:
        print("Reached additional waypoint")
        file.write(time_stamp() + " Reached additional waypoint\n")
        break
    time.sleep(1)


# Land and disarm the drone
print("Landing...")
file.write(time_stamp() + " Landing...\n")
vehicle.mode = VehicleMode("LAND")

while True:
    current_altitude = vehicle.location.global_relative_frame.alt
    print(" Altitude: ", current_altitude)
    file.write(time_stamp() + " Altitude: " + str(current_altitude) + "\n")
    if current_altitude <= 0.2:
        print("Landed")
        file.write(time_stamp() + " Landed\n")
        vehicle.armed = False
        break
    time.sleep(1)


while vehicle.armed:  # Wait for the drone to disarm
    print("Waiting for disarming...")
    file.write(time_stamp() + " Waiting for disarming...\n")
    time.sleep(1)

print("Close vehicle object")
file.write(time_stamp() + " Close vehicle object\n")
vehicle.close()

if sitl:
    sitl.stop()


file.write(time_stamp() + " file removed")
file.write("-------------------------------------------------------------------------------------------\n")
file.close()
