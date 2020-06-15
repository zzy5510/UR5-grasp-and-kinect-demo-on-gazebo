#! /usr/bin/env python
import sys
import rospy
import moveit_commander
import geometry_msgs
from std_msgs.msg import String

moveit_commander.roscpp_initializer.roscpp_initialize(sys.argv)
rospy.init_node('move_group_grasp', anonymous=True)
robot = moveit_commander.robot.RobotCommander()

arm_group = moveit_commander.move_group.MoveGroupCommander("arm")
hand_group = moveit_commander.move_group.MoveGroupCommander("gripper")

arm_group.set_named_target("home_j")
plan = arm_group.go()
hand_group.set_named_target("open")
plan = hand_group.go()

'''First to go to l'''
arm_group.set_named_target("home_l")
plan = arm_group.go(wait = False)
rospy.loginfo("wait for next command")

command=rospy.wait_for_message("command",String,timeout=None)
if command.data=="stop":
    arm_group.stop()
    rospy.sleep(0.5)
    moveit_commander.roscpp_initializer.roscpp_shutdown()

'''second to go to j'''
arm_group.set_named_target("home_j")
plan = arm_group.go(wait = False)
rospy.loginfo("wait for next command")

command=rospy.wait_for_message("command",String,timeout=None)
if command.data=="stop":
    arm_group.stop()
    rospy.sleep(0.5)
    moveit_commander.roscpp_initializer.roscpp_shutdown()

'''Third to go to l'''
arm_group.set_named_target("home_l")
plan = arm_group.go(wait = False)
rospy.loginfo("wait for next command")

command=rospy.wait_for_message("command",String,timeout=None)
if command.data=="stop":
    arm_group.stop()
    rospy.sleep(0.5)
    moveit_commander.roscpp_initializer.roscpp_shutdown()

moveit_commander.roscpp_initializer.roscpp_shutdown()
