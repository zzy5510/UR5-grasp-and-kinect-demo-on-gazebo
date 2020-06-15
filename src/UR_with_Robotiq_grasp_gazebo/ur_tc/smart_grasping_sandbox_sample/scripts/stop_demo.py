#! /usr/bin/env python
import sys
import rospy
import moveit_commander
import geometry_msgs

moveit_commander.roscpp_initializer.roscpp_initialize(sys.argv)
rospy.init_node('move_group_grasp', anonymous=True)
robot = moveit_commander.robot.RobotCommander()

arm_group = moveit_commander.move_group.MoveGroupCommander("arm")
hand_group = moveit_commander.move_group.MoveGroupCommander("gripper")

arm_group.set_named_target("home_j")
plan = arm_group.go()
hand_group.set_named_target("open")
plan = hand_group.go()

arm_group.set_named_target("home_l")
plan = arm_group.go(wait = False)
rospy.sleep(1)
arm_group.stop()



moveit_commander.roscpp_initializer.roscpp_shutdown()
