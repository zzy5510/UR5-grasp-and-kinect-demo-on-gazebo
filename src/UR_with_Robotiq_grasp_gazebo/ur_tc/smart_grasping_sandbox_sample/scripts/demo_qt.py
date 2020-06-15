#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
import moveit_commander
import geometry_msgs
from tf.transformations import quaternion_from_euler
from std_msgs.msg import String

def wait_for_command(arm_group):
    rospy.loginfo("start to recevice command")
    command=rospy.wait_for_message("command",String,timeout=None)
    if command.data=="stop":
        arm_group.stop()
        rospy.loginfo("stop the arm")
        rospy.sleep(0.5)
        moveit_commander.roscpp_initializer.roscpp_shutdown()
    else:
        rospy.loginfo("continue to moving")


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
    plan = arm_group.go(wait = False)
    wait_for_command(arm_group)

    #运动到抓取位置
    grasp.position.z -= 0.1
    arm_group.set_pose_target(grasp)
    plan = arm_group.go()
    hand_group.set_named_target("close")
    plan = hand_group.go()
    #先升高一段距离
    #grasp.position.z += 0.1
    #arm_group.set_pose_target(grasp)
    #plan = arm_group.go() 

    #运动到放置位置
    arm_group.set_pose_target(place)
    plan = arm_group.go(wait = False)
    wait_for_command(arm_group)
    hand_group.set_named_target("open")
    plan = hand_group.go()

# 初始化节点
moveit_commander.roscpp_initializer.roscpp_initialize(sys.argv)
rospy.init_node('move_group_grasp', anonymous=True)
robot = moveit_commander.robot.RobotCommander()
# 建立规划组
arm_group = moveit_commander.move_group.MoveGroupCommander("arm")
hand_group = moveit_commander.move_group.MoveGroupCommander("gripper")

# 回到初始位置
arm_group.set_named_target("home")
plan = arm_group.go()
hand_group.set_named_target("open")
plan = hand_group.go()
end_effector_link = arm_group.get_end_effector_link()

while not rospy.is_shutdown():
    rospy.loginfo("please send command.")
    command=rospy.wait_for_message("command",String,timeout=None)
    
    #重置位置
    if command.data=="reset":
        arm_group.set_named_target("home_j")
        plan = arm_group.go()
        rospy.loginfo("arm has been reset.")
        continue

    #开始运动
    elif command.data=="move":
        grasp_1=set_pose(0.15, 0,    1.08, -1.5707, 0, -1.5707)
        grasp_2=set_pose(0.15, 0.15, 1.08, -1.5707, 0, -1.5707)
        grasp_3=set_pose(0,    0,    1.08, -1.5707, 0, -1.5707)
        grasp_4=set_pose(0,    0.15, 1.08, -1.5707, 0, -1.5707)

        place_1=set_pose(-0.25,0,    1.2,  -1.5707, 0, -1.5707)
        place_2=set_pose(-0.25,0.15, 1.2,  -1.5707, 0, -1.5707)
        place_3=set_pose(-0.4, 0,    1.2,  -1.5707, 0, -1.5707)
        place_4=set_pose(-0.4, 0.15, 1.2, - 1.5707, 0, -1.5707)

        grasp_and_place(grasp_1, place_1, arm_group, hand_group)
        grasp_and_place(grasp_2, place_2, arm_group, hand_group)
        grasp_and_place(grasp_3, place_3, arm_group, hand_group)
        grasp_and_place(grasp_4, place_4, arm_group, hand_group)
        continue

    #向前移动
    elif command.data=="forward":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(1,float(dist.data)/1000, end_effector_link)
        arm_group.go()

    #向前移动
    elif command.data=="forward":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(1,float(dist.data)/1000, end_effector_link)
        arm_group.go()
    
    #向后移动
    elif command.data=="back":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(1,-float(dist.data)/1000, end_effector_link)
        arm_group.go()


    #向左移动
    elif command.data=="left":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(0,float(dist.data)/1000, end_effector_link)
        arm_group.go()


    #向右移动
    elif command.data=="right":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(0,-float(dist.data)/1000, end_effector_link)
        arm_group.go()


    #向上移动
    elif command.data=="up":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(2,float(dist.data)/1000, end_effector_link)
        arm_group.go()

    #向前移动
    elif command.data=="down":
        dist=rospy.wait_for_message("command",String,timeout=None)
        arm_group.shift_pose_target(2,-float(dist.data)/1000, end_effector_link)
        arm_group.go()

    #无效指令    
    else : 
        rospy.loginfo("invalid insturction. Please send again.")
        continue

rospy.sleep(1)
moveit_commander.roscpp_initializer.roscpp_shutdown()

