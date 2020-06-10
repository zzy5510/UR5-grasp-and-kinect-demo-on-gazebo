#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "ros/ros.h"
#include "std_msgs/String.h"


MainWindow::MainWindow(int argc, char** argv, QWidget *parent) :
  QMainWindow(parent),
  ui(new Ui::MainWindow),
  qnode(argc,argv)
{
  ui->setupUi(this);
}

MainWindow::~MainWindow()
{
  delete ui;
}


void MainWindow::on_butconnect_clicked()
{
   ROS_INFO("%s","begin to init.");
   qnode.init();
   ROS_INFO("%s","ready to send.");
}

void MainWindow::on_butsend_clicked()
{
  qnode.send("hello ros");
}

void MainWindow::on_butstop_clicked()
{
  qnode.send("stop");
}

void MainWindow::on_butreset_clicked()
{
   qnode.send("reset");
}


void MainWindow::on_butmove_clicked()
{
    qnode.send("move");
}

void MainWindow::on_up_clicked()
{
    QString str= ui->linedist->text();
    qnode.send("up");
    usleep(10000);
    qnode.send(str.toStdString());

}

void MainWindow::on_left_clicked()
{
  QString str= ui->linedist->text();
  qnode.send("left");
  usleep(10000);
  qnode.send(str.toStdString());
}

void MainWindow::on_right_clicked()
{
  QString str= ui->linedist->text();
  qnode.send("right");
  usleep(10000);
  qnode.send(str.toStdString());
}

void MainWindow::on_down_clicked()
{
  QString str= ui->linedist->text();
  qnode.send("down");
  usleep(10000);
  qnode.send(str.toStdString());
}

void MainWindow::on_forward_clicked()
{
  QString str= ui->linedist->text();
  qnode.send("forward");
  usleep(10000);
  qnode.send(str.toStdString());
}

void MainWindow::on_back_clicked()
{
  QString str= ui->linedist->text();
  qnode.send("back");
  usleep(10000);
  qnode.send(str.toStdString());
}
