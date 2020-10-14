# -*- coding: utf-8 -*-
import cv2
import numpy as np
import collections
 
# Define Dictionary store color up & low
#e.g.：{Color: [min, max]}
#{'red': [array([160,  43,  46]), array([179, 255, 255])]}
 
def getColorList():
    dict = collections.defaultdict(list)
 
    # Red1
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['Red']=color_list
 
    # Red2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['Red'] = color_list

    # Yellow
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['Yellow'] = color_list
 
    # Green
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['Green'] = color_list

    return dict


def get_color(frame,x,y,h,w):
    #Find ROI
    frame = frame[y:y+h,x:x+w]

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])
        # cv2.imwrite(d+'.jpg',mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary,None,iterations=2)
        # Adaptive for opencv 4.x version.
        # Opencv 3.x version，findContours return one more value - "img" at the beginning
        cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum+=cv2.contourArea(c)
        if sum > maxsum : 
            maxsum = sum
            color = d
    # print("detected color is:"+color)
    return color
 

