#!/usr/bin/env python
'''listener ROS Node'''
import rospy
from std_msgs.msg import String
from control_msgs.msg import FollowJointTrajectoryActionResult

def callback_continue(data):
    pub = rospy.Publisher('command', String, queue_size=10)
    rospy.loginfo("an execution finished and i send continue")
    pub.publish("continue")

def listener():
    '''listener Subscriber'''
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    rospy.loginfo("i begin to listen")
    rospy.Subscriber("/arm_controller/follow_joint_trajectory/result",FollowJointTrajectoryActionResult, callback_continue)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()