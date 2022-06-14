#!/usr/bin/python3

import numpy as np
import rospy
from turtlesim.msg import Pose
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist

class callBackFunctions:
    def __init__(self):
        pass 

    def getCenter(self, msg):
        self.position = msg.data
        print(self.position)

    def mainCallBack(self, msg):
        scaledTurtlePosition = (msg.x/(2*5.544445),msg.y/(2*5.544445),msg.theta)
        xPosition = self.position[0]/640
        yPosition = 1-self.position[1]/480
        scaledPosition = (xPosition, yPosition)
        publishVelocity(scaledTurtlePosition,scaledPosition)

def publishVelocity(current,goal):
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rot=Twist()
    theta = np.arctan2(goal[1] - current[1],goal[0] - current[0])

    x_vel = np.sqrt((goal[1]- current[1])**2 + (goal[0]- current[0])**2)

    rot.angular.x = 0
    rot.angular.y = 0
    rot.angular.z = 10 * (theta - current[2])
    rot.linear.x =  10 * x_vel
    rot.linear.y =  0
    rot.linear.z = 0
    pub.publish(rot)

def subscriber():
    rospy.init_node('makeTurtleMove')
    callBacks = callBackFunctions()
    sub_center = rospy.Subscriber('/ballCenter',Float64MultiArray,callback=callBacks.getCenter)
    sub_pose = rospy.Subscriber('/turtle1/pose',Pose,callback=callBacks.mainCallBack)
    rospy.spin()

if __name__=="__main__":
    subscriber()