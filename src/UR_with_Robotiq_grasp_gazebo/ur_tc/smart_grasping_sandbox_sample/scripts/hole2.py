#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
import moveit_commander
import geometry_msgs
from tf.transformations import quaternion_from_euler

moveit_commander.roscpp_initializer.roscpp_initialize(sys.argv)
rospy.init_node('move_group_grasp', anonymous=True)
robot = moveit_commander.robot.RobotCommander()

arm_group = moveit_commander.move_group.MoveGroupCommander("arm")
hand_group = moveit_commander.move_group.MoveGroupCommander("gripper")


pose_target = geometry_msgs.msg.Pose()
q = quaternion_from_euler(0, 0, 0)
pose_target.orientation.x = q[0]
pose_target.orientation.y = q[1]
pose_target.orientation.z = q[2]
pose_target.orientation.w = q[3]

pose_target.position.x = 0
pose_target.position.y = -0.2
pose_target.position.z = 1.1
arm_group.set_pose_target(pose_target)
plan = arm_group.go()

pose_target.position.x = 0
pose_target.position.y = -0.2
pose_target.position.z = 0.9
arm_group.set_pose_target(pose_target)
plan = arm_group.go()

dis=(0.09-0.0196)/2
posi=[dis,dis]
hand_group.set_joint_value_target(posi)
plan = hand_group.go()
rospy.sleep(2)

x=-0.02378
y= 0.13758

pose_target.position.x = x-0.05
pose_target.position.y = y
pose_target.position.z= 1
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("1")

pose_target.position.x = x-0.05/(2**0.5)
pose_target.position.y = y+0.04/(2**0.5)

arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("1.5")


pose_target.position.x = x
pose_target.position.y = y+0.04
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("2")

pose_target.position.x = x+0.03/(2**0.5)
pose_target.position.y = y+0.04/(2**0.5)
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("2.5")

pose_target.position.x = x+0.03
pose_target.position.y = y
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("3")

pose_target.position.x = x+0.03/(2**0.5)
pose_target.position.y = y-0.02/(2**0.5)
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("3.5")

pose_target.position.x = x
pose_target.position.y = y-0.02
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("4")

pose_target.position.x = x-0.01/(2**0.5)
pose_target.position.y = y-0.02/(2**0.5)
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("4.5")

pose_target.position.x = x-0.01
pose_target.position.y = y
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("5")

pose_target.position.x = x-0.005
pose_target.position.y = y+0.005
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("5.5")

pose_target.position.x = x
pose_target.position.y = y
arm_group.set_pose_target(pose_target)
plan = arm_group.go()
rospy.loginfo("6")


pose_target.position.x = x
pose_target.position.y = y
pose_target.position.z = 0.89
arm_group.set_pose_target(pose_target)
plan = arm_group.go()

hand_group.set_named_target("open")
plan = hand_group.go()

pose_target.position.x = -0.02
pose_target.position.y = 0.137
pose_target.position.z = 1.3
arm_group.set_pose_target(pose_target)
plan = arm_group.go()


rospy.sleep(1)
moveit_commander.roscpp_initializer.roscpp_shutdown()
