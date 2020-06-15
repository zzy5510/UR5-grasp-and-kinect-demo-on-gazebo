#!/usr/bin/env python
from sensor_msgs.msg import JointState
import rospy

def callback(data):
    rospy.loginfo(rospy.get_caller_id()+'sensor_effort%s',data.data)

def effort_receiver():
    rospy.init_node('effort_receiver', anonymous=True)
    rospy.Subscriber('/joint_states', JointState,callback)
    rospy.spin()

if __name__=='__main__':
    effort_receiver()
