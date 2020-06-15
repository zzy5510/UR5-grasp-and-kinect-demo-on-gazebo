#!/usr/bin/env python
'''listener ROS Node'''
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import  PointCloud2

def listener():
    '''listener Subscriber'''

    rospy.init_node('listener', anonymous=True)
    rospy.loginfo("i begin to listen")
    point_static=rospy.wait_for_message('camera/depth/points',PointCloud2,timeout=None)
    pub=rospy.Publisher('pclstatic',PointCloud2,queue_size=0)
    loop=rospy.Rate(2)
    while not rospy.is_shutdown():
    #count=0
    #while count<10:
        current_time = rospy.get_rostime()
        seconds = rospy.get_time()
        point_static.header.stamp=current_time
        pub.publish(point_static)
        rospy.loginfo("i send static pcl in time %i %i",current_time.secs, current_time.nsecs)
        loop.sleep()
	#count=count+1

if __name__ == '__main__':
    listener()
