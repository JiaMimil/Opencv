#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
 
def callback(data):
    global bridge
    cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    gs_frame = cv2.GaussianBlur(cv_img, (5, 5), 0)
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    erode_hsv = cv2.erode(hsv, None, iterations=1)
    inRange_hsv = cv2.inRange(erode_hsv, np.array([0, 43, 46]), np.array([10, 255, 255]))
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    max_cnt = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_cnt)
#这样框起来不带倾斜角
    cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    text = "%s,%s"%(x+w/2,y+h/2)
    cv2.putText(cv_img, text, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("frame" , cv_img)
    cv2.waitKey(1)
    try:  
        processed_image_msg = bridge.cv2_to_imgmsg(cv_img, "bgr8")  
        processed_image_pub.publish(processed_image_msg)  
    except CvBridgeError as e:  
        print(e)  

if __name__ == '__main__':
    rospy.init_node('img_process_node', anonymous=True)
    bridge = CvBridge()
    processed_image_pub = rospy.Publisher('/image_view/processed_image', Image, queue_size=10)  
    rospy.Subscriber('/image_view/image_raw', Image, callback)


    rospy.spin()
