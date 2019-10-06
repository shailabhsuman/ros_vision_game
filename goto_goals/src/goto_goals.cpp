#include "goto_goals/goto_goals.h"

namespace goto_goals
{
  gotoGoals::gotoGoals() :
    nh_(ros::NodeHandle()),
    nh_private_(ros::NodeHandle("~"))
  {

    goal_pose_subscriber = nh_.subscribe<turtlesim::Pose>
                        ("/turtle/pose",10, &gotoGoals::goalPoseCallback, this);

    pose_subscriber = nh_.subscribe<turtlesim::Pose>
                        ("/turtle1/pose",10, &gotoGoals::poseCallback, this);

    vel_publisher = nh_.advertise<geometry_msgs::Twist>
                        ("/turtle1/cmd_vel",10, this);

    nh_private_.param<float>("p_gain_linear",kp_linear,1);
    nh_private_.param<float>("p_gain_ang",kp_angular,6);
    nh_private_.param<float>("tolerance",tol,0.5);

  }

  void gotoGoals::poseCallback(const turtlesim::PoseConstPtr &msg)
  {
    current_pose = *msg;
    float mag1, mag2;
    mag1 = pow((goal_pose.x - msg->x),2);
    mag2 = pow((goal_pose.y - msg->y),2);
    mag = sqrt(mag1 + mag2);
  }

  void gotoGoals::goalPoseCallback(const turtlesim::PoseConstPtr &msg)
  {
    goal_pose = *msg;
    if (goal_pose.x > 11.0){
	goal_pose.x = 11.0; 
    }
    if (goal_pose.y > 11.0){
	goal_pose.y = 11.0; 
    }    
  }

  void gotoGoals::velocity_calc()
  {
    ros::Rate loop_rate(5);
    //ROS_INFO("in velocity_cal %f",mag);
    while(ros::ok())
    {
      float velx, angx, angy;
      angx = goal_pose.x - current_pose.x;
      angy = goal_pose.y - current_pose.y;
      cmd_vel.linear.x = kp_linear * mag;
      cmd_vel.angular.z = kp_angular * (atan2(angy,angx) - current_pose.theta);
      ROS_INFO("%f %f",current_pose.x, goal_pose.x);
      vel_publisher.publish(cmd_vel);
      loop_rate.sleep();
      ros::spinOnce();
    }
    //ROS_INFO("in while %f",current_pose.x);

  }

}
