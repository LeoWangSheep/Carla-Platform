# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import sys
import time
from DrivingAgent.Detect.LightColor import get_color
from DrivingAgent.Detect.BubbleSort import bubble_sort2, bubble_sort4

# Detect "Traffic Light" or "Object"
def yolo_detect(input_img,
                # pathIn = '',
                # pathOut = None,
                label_path ='./DrivingAgent/Detect/darknet-master/cfg/coco.names',
                config_path ='./DrivingAgent/Detect/darknet-master/cfg/yolov3-spp.cfg',
                weights_path ='./DrivingAgent/Detect/darknet-master/cfg/yolov3-spp.weights',
                confidence_thre = 0.4,
                nms_thre = 0.3,
                jpg_quality = 100,
                detect_mode = None):

    '''
    pathIn：Origin image path
    pathOut：Output image path
    label_path：Lable file path
    config_path：Model configuration path
    weights_path：Weight file path
    confidence_thre：0-1，confidence（probability/mark)threshold，retain vaule greater than this value
    nms_thre：Threshold for non-maximum suppression
    jpg_quality：Output image quality，greater value represent better quality
    '''

    #===== Object Detect Variable Initialization =====
    # Detected Object List
    detect_list=['person','bicycle','car','motorbike','bus','truck']
    # =>'car', 'bus', 'motorbike', 'bicycle', 'pedestrian'
    # Object Numbers
    count_list=[0,0,0,0,0,0,0,0,0,0] 
    # Label Detected and sort
    back_list=[]
    # x-axis, used for sort
    x_list=[]
    #count_person=count_bicycle=count_car=count_motorplane=count_aeroplane=count_bus=count_truck=count_light=count_stop=count_tvmonitor=0
    
    #===== Light Color Detect Variable Initialization =====
    #Detect Traffic light
    count_light=0	#number of light
    light_axis_x=[] #coordinate of ROI
    light_axis_y=[]
    light_axis_h=[]
    light_axis_w=[]

    # Load Label File
    LABELS = open(label_path).read().strip().split("\n")
    nclass = len(LABELS)
    #print(LABELS)
    # Randomly match the color of the bounding boxes for each category
    np.random.seed(42)
    COLORS = np.random.randint(0, 180, size=(nclass, 3), dtype='uint8')
    
    # Load the image and get its dimensions
    # base_path = os.path.basename(pathIn)
    #img = cv2.imread(pathIn)
    const_img = input_img
    input_img = input_img[:,:,:3]
    input_img = input_img.copy()
    img = input_img
    (H, W) = img.shape[:2]

    # Load the model configuration and weight files
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    
    # Gets the name of the YOLO output layer
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # print(ln)

    # Build the image into a BLOB, set the image size, and execute once
    # YOLO feedforward network calculation, get the boundary box and the corresponding probability
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # Detect time calculation
    detect_time = end-start

    # Initializes bounding box, confidence (probability), category
    boxes = []
    confidences = []
    classIDs = []
    #Create List, used to store traffic lights info(axis,etc)
    light_pick=[]
    # Iterate through each output layer(three layers)
    for output in layerOutputs:
        # Iterating through each test
        for detection in output:
            # Extract the category ID and confidence
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
    
            # Retained bounding greater than threshold 
            if confidence > confidence_thre:
                #return value back to original image, info(center-axis, width, height)
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                   
                # Left Top axis
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
    
                # Update the bounding box, confidence (probability), and category
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    
    # Use non-maximum suppression to suppress weak and overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_thre, nms_thre)
    
    # Make sure at least one bounding box
    if len(idxs) > 0:
        # Iterate through each bounding box
        for i in idxs.flatten():
            # Extract the coordinates of the bounding box
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            
            # Draws the bounding box and adds category labels and confidence in the upper left corner
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = '{}: {:.3f}'.format(LABELS[classIDs[i]], confidences[i])
            (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(img, (x, y-text_h-baseline), (x + text_w, y), color, -1)
            cv2.putText(img, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            #label write into list
            if (LABELS[classIDs[i]] != 'traffic light'):
                back_list.append(LABELS[classIDs[i]])
                x_list.append(x)
                #Bubble Sort
                x_list,back_list=bubble_sort2(x_list,back_list)
                for j in range(0,len(detect_list)):
                    if(LABELS[classIDs[i]]==detect_list[j]):
                        count_list[j]+=1           
            else:
            #traffic light label write into list
                count_light+=1
                light_axis_x.append(x)
                light_axis_y.append(y)
                light_axis_h.append(h)
                light_axis_w.append(w)
               # print(i,LABELS[classIDs[i]],'axis',x,y,w,h)
            #print('Center axis is','X:',(x+w)/2,' Y:',(y+h)/2)
                if (count_light>1):
                	light_axis_x,light_axis_y,light_axis_h,light_axis_w=bubble_sort4(light_axis_x,light_axis_y,light_axis_h,light_axis_w)
 
    # print(back_list)
    # print("Traffic Light number:",count_light)
    # for i in range(0,count_light-1):
        # print("Axis:",light_axis_x[i],light_axis_y[i],light_axis_h[i],light_axis_w[i])
    mid_light = round(count_light/2)
    # print('Center Traffic Light is No. ',mid_light)

    #====  Traffic Light Output ====
    if(detect_mode =="light"):
        light_color = get_color(const_img, 
                        light_axis_x[mid_light], light_axis_y[mid_light], 
                        light_axis_h[mid_light], light_axis_w[mid_light])
        color_list = []
        color_list.append(light_color)
        return color_list

    #====  Obejct Detect Output ====
    # Output Image
    base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    #Use Time as filename
    now = time.strftime("%Y-%m-%d(%H_%M_%S)",time.localtime(time.time()))
    #If dir not exist, create it
    if os.path.exists(base_path + '\\DrivingAgent\\Detect\\Object_Images')==False:
         os.mkdir(base_path + '\\DrivingAgent\\Detect\\Object_Images')
    output_filename = base_path + '\\DrivingAgent\\Detect\\Object_Images\\' + now +'.jpg'
    #Save image
    cv2.imwrite(output_filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])

    #Oject detected list
    detect_objects=[]
    for i in range(0, len(back_list)):
        if back_list[i] == "person":
            detect_objects.append("pedestrian")

        if back_list[i] == "bicycle":
            detect_objects.append("bicycle")

        if back_list[i] == "car":
            detect_objects.append("car")

        if back_list[i] == "motorbike":
            detect_objects.append("motorbike")

        if back_list[i] == "bus":
            detect_objects.append("bus")

        if back_list[i] == "truck":
            detect_objects.append("bus")       

    return detect_objects