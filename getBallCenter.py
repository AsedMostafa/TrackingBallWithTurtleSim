#!/usr/bin/python3

import numpy as np
import cv2
import detectBall
import rospy
from std_msgs.msg import Float64MultiArray

cap = cv2.VideoCapture(-1)

def getFrameAndCenter():
    lower = np.array([17 , 127 , 113])
    upper = np.array([255 ,255, 255]) # find these bands with range detector file
    ballImage = detectBall.ballDetector()
    ret,frame=cap.read()
    binary = ballImage.toBinary(frame,lower,upper)
    dial = ballImage.enhanceBinary(binary,3,10)
    frame ,center , r = ballImage.getBallCoordinate(dial,frame)
    return(frame,center)
def Ball_center():
    rospy.init_node("ballCenter")
    pub = rospy.Publisher("/ballCenter",Float64MultiArray)
    rate = rospy.Rate(100)
    rospy.loginfo("publisher is working")
    while not rospy.is_shutdown():
        frame, center = getFrameAndCenter()
        dataInfo = Float64MultiArray()
        dataInfo.data = center

        if frame is None:
            break
        cv2.imshow("Frame",frame)

        key=cv2.waitKey(30)
        if key==27:
            break

    
        pub.publish(dataInfo)
        #rospy.spin()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
     Ball_center()
