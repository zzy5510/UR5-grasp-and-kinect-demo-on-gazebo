#include "ros/ros.h"
#include "std_msgs/String.h"
#include "test_msg/newmsg2.h"
#include <sstream>


int main(int argc, char *argv[])
{
	ros::init(argc, argv, "cppp");
	ros::NodeHandle n;

	/**
	 * The advertise() function is how you tell ROS that you want to
	 * publish on a given topic name. This invokes a call to the ROS
	 * master node, which keeps a registry of who is publishing and who
	 * is subscribing. After this advertise() call is made, the master
	 * node will notify anyone who is trying to subscribe to this topic name,
	 * and they will in turn negotiate a peer-to-peer connection with this
	 * node.  advertise() returns a Publisher object which allows you to
	 * publish messages on that topic through a call to publish().  Once
	 * all copies of the returned Publisher object are destroyed, the topic
	 * will be automatically unadvertised.
	 *
	 * The second parameter to advertise() is the size of the message queue
	 * used for publishing messages.  If messages are published more quickly
	 * than we can send them, the number here specifies how many messages to
	 * buffer up before throwing some away.
	 */
	ros::Publisher chatter_pub = n.advertise<test_msg::newmsg2>("chatter", 1000);

	ros::Rate loop_rate(10);
	float position_x[4]  ={0.15,0.15,0,   0   };
	float position_y[4]  ={0,   0.15,0,   0.15};
	float position_yaw[4]={0,   0,   0,   0   };

	/**
	 * A count of how many messages we have sent. This is used to create
	 * a unique string for each message.
	 */
	int count = 0;
	while (ros::ok())
	{
		/**
		 * This is a message object. You stuff it with data, and then publish it.
		 */
		test_msg::newmsg2 msg;
		for(int i=0;i<4;i++)
		{
			msg.x[i]=position_x[i];
			msg.y[i]=position_y[i];
			msg.yaw[i]=position_yaw[i];
			msg.depth[i]=0;
			msg.width[i]=0;
		}
		std::cout<<msg.x[0]<<' '<<msg.y[0]<<' '<<msg.yaw[0];

		/**
		 * The publish() function is how you send messages. The parameter
		 * is the message object. The type of this object must agree with the type
		 * given as a template parameter to the advertise<>() call, as was done
		 * in the constructor above.
		 */
		chatter_pub.publish(msg);

		ros::spinOnce();

		loop_rate.sleep();
		++count;
        if(count>10)
        break;
	}

	return 0;
}
