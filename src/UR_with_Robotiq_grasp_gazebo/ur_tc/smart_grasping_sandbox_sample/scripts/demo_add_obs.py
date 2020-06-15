#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
import moveit_commander
import geometry_msgs
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import  PlanningScene, ObjectColor
from tf.transformations import quaternion_from_euler

def set_posestamped(x,y,z,row,pitch,yaw):
    pose_target = PoseStamped()
    pose_target.header.frame_id='world'
    q = quaternion_from_euler(row, pitch, yaw )
    pose_target.pose.orientation.x = q[0]
    pose_target.pose.orientation.y = q[1]
    pose_target.pose.orientation.z = q[2]
    pose_target.pose.orientation.w = q[3]
    pose_target.pose.position.x = x
    pose_target.pose.position.y = y
    pose_target.pose.position.z = z
    return pose_target
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
    rospy.sleep(2)
    #先升高一段距离
    grasp.position.z += 0.1
    arm_group.set_pose_target(grasp)
    plan = arm_group.go()  
    #运动到放置位置
    arm_group.set_pose_target(place)
    plan = arm_group.go()
    hand_group.set_named_target("open")
    plan = hand_group.go()

# 初始化节点
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_grasp', anonymous=False)
robot = moveit_commander.robot.RobotCommander()

# 初始化场景对象
scene = PlanningSceneInterface()
scene_pub = rospy.Publisher('my_planning_scene', PlanningScene, queue_size=5)
rospy.sleep(1)

# 建立规划组
arm_group = moveit_commander.move_group.MoveGroupCommander("arm")
hand_group = moveit_commander.move_group.MoveGroupCommander("gripper")
arm_group.allow_replanning(True)

#设置物体名称
floor_id = 'floor'
obs_id= 'obs'
table_id= 'table'
pill_id='pill'
# 设置table、和box2的尺寸和位置
floor_size = [3, 3, 0.2]
obs_size=[0.05,0.4,0.1]
table_size=[0.913,0.913,0.04]
pill_size=[0.2,0.2,1]

floor_pose=set_posestamped(0,0,0,0,0,0)
obs_pose=set_posestamped(-0.094,0.072,0.825,0,0,0)
table_pose=set_posestamped(-0.159,0.184,0.752,0,0,0)
pill_pose=set_posestamped(0,-1,0.5,0,0,0)

#rospy.sleep(2)
scene.add_box(floor_id,floor_pose,floor_size)
scene.add_box(obs_id,obs_pose,obs_size)
scene.add_box(table_id,table_pose,table_size)
scene.add_box(pill_id,pill_pose,pill_size)
rospy.sleep(1)

# 设定UR的目标位置和姿态
grasp_1=set_pose(0.12, -0.14, 0.84, 0, 0, 0)
grasp_2=set_pose(0.27, -0.14, 0.84, 0, 0, 0)
grasp_3=set_pose(0.02, -0.03, 0.84, 0, 0, 0)
grasp_4=set_pose(0.19,  0.03, 0.84, 0, 0, 0)
grasp_5=set_pose(0,     0.08, 0.84, 0, 0, 0)
grasp_6=set_pose(0.26,  0.16, 0.84, 0, 0, 0)

place_1=set_pose(-0.2,  -0.15, 1.2,  0, 0, 0)
place_2=set_pose(-0.4,  -0.15, 1.2, -0, 0, 0)
place_3=set_pose(-0.2,  -0,    1.2,  0, 0, 0)
place_4=set_pose(-0.4,  -0,    1.2,  0, 0, 0)
place_5=set_pose(-0.2,   0.15, 1.2,  0, 0, 0)
place_6=set_pose(-0.4,   0.15, 1.2, -0, 0, 0)

grasp_and_place(grasp_1, place_1, arm_group, hand_group)
grasp_and_place(grasp_2, place_2, arm_group, hand_group)
grasp_and_place(grasp_3, place_3, arm_group, hand_group)
grasp_and_place(grasp_4, place_4, arm_group, hand_group)
grasp_and_place(grasp_5, place_5, arm_group, hand_group)
grasp_and_place(grasp_6, place_6, arm_group, hand_group)

rospy.sleep(2)
moveit_commander.roscpp_initializer.roscpp_shutdown()

