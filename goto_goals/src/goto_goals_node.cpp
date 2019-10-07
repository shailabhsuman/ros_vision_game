#include "ros/ros.h"
#include "goto_goals/goto_goals.h"


int main(int argc, char** argv)
{
  ros::init(argc,argv,"goto_goals_node");
  ros::NodeHandle nh;
  ros::Duration(2).sleep();

  goto_goals::gotoGoals hello;
  hello.velocity_calc();
  ros::spin();
}
