#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
import moveit_commander
import geometry_msgs
from tf.transformations import quaternion_from_euler
from test_msg.msg import newmsg2

xx=[]
yy=[]
yawyaw=[]

def set_pose(x, y, z, row, pitch, yaw):
    pose_target = geometry_msgs.msg.Pose()
    q = quaternion_from_euler(row, pitch, yaw )
    pose_target.orientation.x = q[0]
    pose_target.orientation.y = q[1]
    pose_target.orientation.z = q[2]
    pose_target.orientation.w = q[3]
    pose_target.position.x = x
    pose_target.position.y = y
    pose_target.position.z = z
    return pose_target

def grasp_and_place(grasp, place,arm_group, hand_group):
    #先运动到预抓取位置  
    grasp.position.z += 0.1
    arm_group.set_pose_target(grasp)
    plan = arm_group.go()
    #运动到抓取位置
    grasp.position.z -= 0.1
    arm_group.set_pose_target(grasp)
    plan = arm_group.go()
    hand_group.set_named_target("close")
    plan = hand_group.go()
    #先升高一段距离
    grasp.position.z += 0.1
    arm_group.set_pose_target(grasp)
    plan = arm_group.go()  
    #运动到放置位置
    arm_group.set_pose_target(place)
    plan = arm_group.go()
    hand_group.set_named_target("open")
    plan = hand_group.go()

def listener():
    '''listener Subscriber'''

    rospy.init_node('listener', anonymous=False)
    rospy.loginfo("ready for getting data %s")
    data=rospy.wait_for_message("/chatter",newmsg2,timeout=None)
    rospy.loginfo("x= %s"+str(data.x[0])+"y= %s"+str(data.y[0])+"yaw= %s"+str(data.yaw[0]))
    xx.extend(data.x)
    yy.extend(data.y)
    yawyaw.extend(data.yaw)

listener()
# 初始化节点
moveit_commander.roscpp_initializer.roscpp_initialize(sys.argv)
#rospy.init_node('move_group_grasp', anonymous=True)
robot = moveit_commander.robot.RobotCommander()
# 建立规划组
arm_group = moveit_commander.move_group.MoveGroupCommander("arm")
hand_group = moveit_commander.move_group.MoveGroupCommander("gripper")

# 回到初始位置
arm_group.set_named_target("home_j")
plan = arm_group.go()
hand_group.set_named_target("open")
plan = hand_group.go()

# 设定UR的目标位置和姿态
grasp_1=set_pose(xx[0],yy[0], 1.08, -1.5707, 0, -1.5707)
grasp_2=set_pose(xx[1],yy[1], 1.08, -1.5707, 0, -1.5707)
grasp_3=set_pose(xx[2],yy[2], 1.08, -1.5707, 0, -1.5707)
grasp_4=set_pose(xx[3],yy[3], 1.08, -1.5707, 0, -1.5707)

place_1=set_pose(0.15,-0.3,  1.2,  -1.5707, 0, -1.5707)
place_2=set_pose(0.15,-0.15, 1.2,  -1.5707, 0, -1.5707)
place_3=set_pose(0,   -0.3,  1.2,  -1.5707, 0, -1.5707)
place_4=set_pose(0,   -0.15, 1.2, - 1.5707, 0, -1.5707)

grasp_and_place(grasp_1, place_1, arm_group, hand_group)
#grasp_and_place(grasp_2, place_2, arm_group, hand_group)
#grasp_and_place(grasp_3, place_3, arm_group, hand_group)
#grasp_and_place(grasp_4, place_4, arm_group, hand_group)

rospy.sleep(2)
moveit_commander.roscpp_initializer.roscpp_shutdown()


