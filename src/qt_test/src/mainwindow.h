#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <qnode.h>
using namespace qt_test;
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
  Q_OBJECT

public:
  explicit MainWindow(int argc, char** argv,QWidget *parent = 0);
  ~MainWindow();

private slots:
  void on_butconnect_clicked();

  void on_butsend_clicked();

  void on_butstop_clicked();

  void on_butreset_clicked();

  void on_butmove_clicked();

  void on_up_clicked();

  void on_left_clicked();

  void on_right_clicked();

  void on_down_clicked();

  void on_forward_clicked();

  void on_back_clicked();

private:
  Ui::MainWindow *ui;
  QNode qnode;
};

#endif // MAINWINDOW_H
