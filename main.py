# project inspired by the computerphile traceroute map video
# link: https://youtu.be/75yKT3OuE44

import subprocess
import json
import urllib.request
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def getLoc(IP):
    url = "https://geolocation-db.com/json/" + IP
    response = urllib.request.urlopen(url)
    encoding = response.info().get_content_charset('utf8')
    json_data = json.loads(response.read().decode(encoding))
    if json_data["latitude"] == 'Not found' or json_data["latitude"] == 0.0:
        latitude = None
    else:
        latitude = json_data['latitude']
    if json_data["longitude"] == 'Not found' or json_data["longitude"] == 0.0:
        longitude = None
    else:
        longitude = json_data["longitude"]
    return latitude, longitude


def main():
    # 161.73.246.13 is the IP of Oxford Brookes university, good test case because it gives an overseas lat/long
    inputIP = input("What IPv4 address or domain name do you want to tracert?")

    while True:
        userLat = input("What is your latitude? If you don't know, input 30.39")
        try:
            userLat = float(userLat)
            if -90 < userLat < 90:
                break
            else:
                print("latitude must be a number between -90 and 90")
        except:
            print("latitude must be a number between -90 and 90")

    while True:
        userLon = input("What is your longitude? If you don't know, input -88.88")
        try:
            userLon = float(userLon)
            if -180 < userLon < 180:
                break
            else:
                print("longitude must be a number between -180 and 180")
        except:
            print("longitude must be a number between -180 and 180")


    p1 = subprocess.run(['tracert', '-d', '-4', inputIP], shell=True, capture_output=True, text=True)
    print(p1.stdout)
    fig = plt.figure(figsize=(10, 6), edgecolor='w')
    myMap = Basemap(projection='mill', lon_0=0, resolution='l')
    myMap.shadedrelief(scale=0.05)

    lastLat = userLat
    lastLon = userLon
    for line in p1.stdout.splitlines():
        line_list = line.split()
        if len(line_list) == 8:
            hopIP = line_list[7]
            (lat, lon) = getLoc(hopIP)

            if lat is None or lon is None:
                continue
            if (lastLat != lat) and (lastLon != lon):
                print(f"This IP {hopIP} is at these coordinates {lat, lon}")
                x, y = myMap(lon, lat)
                myMap.scatter(x, y, 10, marker='o', color='r')
                line, = myMap.drawgreatcircle(lastLon, lastLat, lon, lat, color='b')
                lastLat = lat
                lastLon = lon
        else:
            continue
    plt.show()


if __name__ == '__main__':
    main()
