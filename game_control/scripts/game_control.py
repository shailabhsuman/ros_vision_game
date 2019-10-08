#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from std_msgs.msg import Float64


class GameControl:

    def __init__(self):
        rospy.init_node('game_controller', anonymous=True)

        self.gamecontrol_publisher = rospy.Publisher('gamecontrol',
						Float64, queue_size=10)

        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
						Pose, self.update_pose1)
	self.pose_subscriber = rospy.Subscriber('/turtle2/pose',
						Pose, self.update_pose2)

        self.pose1 = Pose()
	self.pose2 = Pose()
        self.rate = rospy.Rate(1)
	self.score = 0.0

    def update_pose1(self, data):
        self.pose1 = data
        self.pose1.x = round(self.pose1.x, 4)
        self.pose1.y = round(self.pose1.y, 4)

    def update_pose2(self,data):
        self.pose2 = data
        self.pose2.x = round(self.pose2.x, 4)
        self.pose2.y = round(self.pose2.y, 4)


    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose1.x), 2) +
                    pow((goal_pose.y - self.pose1.y), 2))


    def calculate_distance(self):
	while not rospy.is_shutdown():        
        	g_pose = Pose()

        	g_pose.x = self.pose2.x
		g_pose.y = self.pose2.y
	
		if self.euclidean_distance(g_pose) > 0.5:
			self.score = self.score + 1
		else:
			if self.score < 10:
				self.score = 0.0
			
        	self.gamecontrol_publisher.publish(self.score)
		self.rate.sleep()

        rospy.spin()

if __name__ == '__main__':
    try:
        x = GameControl()
	rospy.sleep(1)
        x.calculate_distance()
    except rospy.ROSInterruptException:
        pass
