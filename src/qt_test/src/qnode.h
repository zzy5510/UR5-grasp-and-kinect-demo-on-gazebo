#ifndef QNODE_H
#define QNODE_H

#include <ros/ros.h>
#include "std_msgs/String.h"
#include <string>
#include <QThread>
#include <QStringListModel>

namespace qt_test
{
class QNode : public QThread
{
    Q_OBJECT
public:
    QNode(int argc, char** argv);
    virtual ~QNode();
    bool init();
    void send(const std::string s);
private:
    int init_argc;
    char** init_argv;
    ros::Publisher chatter_publisher;
};
}
#endif // QNODE_H
