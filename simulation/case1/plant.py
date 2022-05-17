from scipy.ndimage.filters import gaussian_filter
import numpy as np
import math

depth = ['water','soil']

def sunriseset(day, latitude):
    delta = math.radians(23.5 * math.sin(math.radians((day-80)*360/365) ))
    theta = math.radians(latitude)
    temp = - math.tan(delta) * math.tan(theta)
    w = math.acos(temp)
    wdegree = math.degrees(w) / 15
    sunrisetime = 12 - wdegree
    sunsettime = 12 + wdegree
    return sunrisetime, sunsettime

def sun(day, hour, latitude = 37.5):
    delta = 23.5 * math.sin(math.radians((day-80)*360/365))
    sunrisetime, sunsettime = sunriseset(day,latitude)
    sunshine = 0
    if hour <sunrisetime or hour>sunsettime:
        sunshine = 0
    else:
        sunshine = math.sin(math.radians(90 - latitude + delta)) * math.cos((hour-12)/(sunrisetime-sunsettime)*math.pi)
    angle = latitude - delta

    return sunshine

def createMap(size):
    tempmap = np.random.rand(len(depth),size,size)
    tempmap = gaussian_filter(tempmap, sigma=2)
    return tempmap

def tile(map):

    return map


print(createMap(40))