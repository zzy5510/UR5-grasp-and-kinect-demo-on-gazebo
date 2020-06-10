#include <ros/ros.h>
#include <ros/network.h>
#include <string>
#include <std_msgs/String.h>
#include <sstream>
#include <qnode.h>

namespace qt_test
{
QNode::QNode(int argc, char** argv )
    : init_argc(argc), init_argv(argv)
{}

QNode::~QNode()
{
    if(ros::isStarted())
    {
        ros::shutdown();
        ros::waitForShutdown();
    }
    wait();
}

bool QNode::init()
{
    ros::init(init_argc,init_argv,"qtcommander");
    if (!ros::master::check())
    {
        return false;
    }
    ros::start();
    ros::NodeHandle n;
    chatter_publisher = n.advertise<std_msgs::String>("command", 1000);
    ros::Rate loop_rate(10);
    ROS_INFO("%s", "init finished");
    start();
    return true;
}

void QNode::send(const std::string s)
{
  ros::Rate loop_rate(10);
  int count = 0;
      while (ros::ok())
      {
          std_msgs::String msg;
          msg.data = s;
          chatter_publisher.publish(msg);
          ROS_INFO("Have sent %s",msg.data.c_str());
          ros::spinOnce();
          loop_rate.sleep();
          ++count;
          if(count>0)
          break;
      }
}

}
