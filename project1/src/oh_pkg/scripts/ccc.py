#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time



def pose_callback(pose_message):
    global x_current, y_current, seta_current
    rospy.loginfo(str(pose_message.x) + ","+str(pose_message.y))
    x_current=pose_message.x
    y_current=pose_message.y
    seta_current=pose_message.theta


def go_to(x_goal,y_goal):
    global x_current , y_current , seta_current
    velocity_message=Twist()
    while (True):
        #beta=0.5
        beta=rospy.get_param("/beta")
        fi = rospy.get_param("/fi")
        distance=math.sqrt(((x_goal-x_current)**2)+((y_goal-y_current)**2))
        Xlinear_velocity=beta*distance

        #fi=4.0
        angle=math.atan2(y_goal-y_current,x_goal-x_current)
        Zangular_velocity=(angle-seta_current)*fi

        velocity_message.linear.x=Xlinear_velocity
        velocity_message.angular.z=Zangular_velocity
        pub.publish(velocity_message)
        
        if distance<0.01 :
            rospy.loginfo("arrived to the goal")   
            break

if __name__=='__main__':

    rospy.init_node("control")
    rospy.loginfo("node started")
    
    x_goal=rospy.get_param("/x_goal")
    y_goal=rospy.get_param("/y_goal")
    #x_goal=float(input("enter the X goal : "))
    #y_goal=float(input("enter the Y goal : "))
        

    pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    sub=rospy.Subscriber("/turtle1/pose",Pose , callback=pose_callback)
    time.sleep(2)

    go_to(x_goal,y_goal)