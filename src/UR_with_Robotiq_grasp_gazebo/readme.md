# UR robot arm with Robotiq gripper grasp simulation in Gazebo

## Platform

```ubuntu16.04``` ``` ros-kinetic```  ```gazebo7``` 

## Install

```cd YourWorkspace/src```

``` git clone https://github.com/JingyuYang1997/UR_with_Robotiq_grasp_gazebo.git```

```cd ../.. ```

```catkin_make```

```source devel/setup.zsh```

Some dependencies such as Moveit should be installed for compilation. Do it according to your compilation debug instructions.

## Demo

```roslaunch smart_grasping_sandbox_sample main.launch ```

```roslaunch urwh_moveit_config urwh_planning_example_execution.launch```

```rosrun smart_grasping_sandbox_sample grasping_demo.py```

then you will get the result like below:

![](./figures/grasp_demo.gif)
