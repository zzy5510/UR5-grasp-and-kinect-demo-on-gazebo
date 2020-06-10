#!/usr/bin/env python
'''listener ROS Node'''
import rospy
from std_msgs.msg import String
from test_msg.msg import newmsg2

def callback(data):
    '''listener Callback Function'''
    rospy.loginfo(rospy.get_caller_id() + "I heard %s"+ str(data.x)+ " "+str(data.y)+ " "+str(data.yaw))

def listener():
    '''listener Subscriber'''
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", newmsg2, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()