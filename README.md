# 基于ROS和gazebo的仿真UR5机器人零件抓取放置系统使用指南

## 系统说明

本系统是我本科毕设搭建的一个基于ROS和gazebo的仿真UR5机械臂零件抓取系统，众多功能并不完善，有些地方还有一些bug，因此仅供各位参考辅助使用。因为在开发过程中遇到很多坑，无谓地浪费了很多时间，而且中文资料比较少，比如Moveit的制动功能、Moveit从相机获取障碍信息避障等等，所以开源出来，希望能帮到各位初学者。
**再次提醒：由于毕设后期本人时间不再充裕，再加上能力有限，本项目有很多不合理和错误的地方，仅供初学者辅助和参考使用**

## 系统配置

Ubuntu 16.04+ROSkinetic

## 依赖项

大部分依赖包都在UR_with_Robotiq_grasp_gazebo中的depends文件夹下，但不免会缺乏一些包。解决方案可在https://blog.csdn.net/a735148617/a
ticle/details/103627811中查看。

## 功能介绍

**ur_with_robotiq_grasp_gazebo：**
该包在https://github.com/JingyuYang1997/UR_with_Robotiq_grasp_gazebo是在工作的基础上完成的。原包并没有添加gazebo_grasp_plugin插件，导致gazebo中抓住时夹爪发生抖动。

该元功能包由5个包组成，**ur_desc**是机器人模型描述包，meshes文件夹包含了描述kinect相机、Robotiq夹爪模型的dae和stl文件。urdf文件夹下包含了项目中使用到的urdf文件。model.urdf为使用Robitiq夹爪的机器人模型，model2.urdf为使用自创二指夹爪的机器人模型。ur_with_kinect为包含kinect相机的模型，该模型文件中用到了gazebo_grasp_plugin，可以修复夹爪在 gazebo中抖动，抓取失败等问题，该包的详细信息见https://github.com/JenniferBuehler/gazebo-pkgs。

**robotiq_85_gripper**为robotiq85夹爪相关仿真、驱动、通信包，但因为其为转动关节，无法确定夹爪距离和关节转角之间的关系，已被本人弃用。

**urwh_moveit_config**为原包含robotiq的Moveit配置包，已弃用。

**confgi**为包含自创二指夹爪的Moveit配置包（吐槽名字的都给我拖下去）具体配置可在config文件夹下查看。controllers.yaml记录了机器人和夹爪的controller，均为follow_joint_trajectory。sensors_3d中记录了Moveit规划场景监听的点云信息。

**smart_grasping_sandbox_sample**是本包的重头戏。world文件夹包含了一些gazebo世界文件，smart_grasp_sandbox.world是原版包的世界文件。launch文件夹里包含一些启动文件。scripts包含一些python写的功能节点。
demo_qt.py结合qt界面使用，qt界面发送字符串消息，该节点会订阅，根据消息作出相应的动作。
demo_add_obs.py中实现了向moveit规划场景中添加障碍物的功能,之后再控制机器人抓取零件放置到指定地点。
listen_four_move.py会监听停止话题，可以在执行任务的过程中随时根据话题进行停止。
movetrans.py会监听/arm_controller/follow_joint_trajectory/result话题，即当机器人完成一次运动时，该节点会发送“continue”，使得listen_four_move可以继续运动下去。
pcltrans.py该节点在收到点云信息后将该信息保存，之后持续不断地发送该话题。
stop_demo.py会让机器人启动后突然停止，用作测试。

**grasp_msg：**
一种新建的rosmsg类型，用于传递抓取位姿。

**qt_test:**
实现了可视化界面，可以通过启动ROS节点，发送话题，来控制机器人运动。
可以使用

```bash
rosrun qt_test qt_test
```

来运行。

## 使用方法

首先，运行

```bash
roslaunch smart_grasping_sandbox_sample main.launch 
```

该命令会启动gazebo。需要注意的是，该launch只是封装，具体的加载urdf模型，导入world文件，加载控制器，都是在launch_simulation中干的。
运行

```bash
roslaunch confgi planning_with_pcl.launch 
```

该launch文件会启动planning_execution.launch，即moveit规划器的启动文件。之后会启动pcltrans.py，具体效果就是让moveit中的点云信息固定下来，不会随着机械臂的乱跑而变化。
那么，是在哪里设置了moveit订阅的点云话题呢？在confgi/config/sensors_3d.yaml中，该yaml会被sensor_manager.launch启动。而sensor_manager.launch的启动已经包含在planning_execution.launch里了。
之后，可以运行

```bash
rosrun rosrun smart_grasping_sandbox_sample demo_add_obs.py 
```

来看看效果啦。

## 写在最后

由于时间匆忙，该项目完成度不高，依旧有很多问题存在。总之，有问题多google，国内的资料相对较少，我的很多问题都是在google和rosanswer两个平台解决的。希望能帮到你！