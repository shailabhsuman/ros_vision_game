#ifndef TURTLECL_H
#define TURTLECL_H
#include <ros/ros.h>
#include <turtlesim/Pose.h>
#include <geometry_msgs/Twist.h>
#include <math.h>

namespace goto_goals {   class gotoGoals {

  public:
    gotoGoals();
    void velocity_calc();
    turtlesim::Pose current_pose;
    turtlesim::Pose goal_pose;

  private:
    ros::NodeHandle nh_;
    ros::NodeHandle nh_private_;

    ros::Subscriber pose_subscriber;
    ros::Subscriber goal_pose_subscriber;
    ros::Publisher vel_publisher;

    void poseCallback(const turtlesim::PoseConstPtr &msg);
    void goalPoseCallback(const turtlesim::PoseConstPtr &msg);

    geometry_msgs::Twist cmd_vel;

    float kp_linear, kp_angular, tol, mag;   
};
}
#endif
