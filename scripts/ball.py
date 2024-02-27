import cv2
import numpy as np

img = cv2.imread('apple.png')

#v1=cv2.Canny(img,100,200)
#blur = cv2.blur(img,(3,3)) #fangkuang
#median = cv2.medianBlur(img,5) #median
#kernel = np.ones((3,3),np.uint8)
#tophat = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)
gs_frame = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
erode_hsv = cv2.erode(hsv, None, iterations=1)
inRange_hsv = cv2.inRange(erode_hsv, np.array([0, 43, 46]), np.array([10, 255, 255]))

cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
max_cnt = max(cnts, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(max_cnt)
#这样框起来不带倾斜角
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

text = "%s,%s"%(x+w/2,y+h/2)
cv2.putText(img, text, (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
