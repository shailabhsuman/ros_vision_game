#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from std_msgs.msg import Float32
from collections import deque
import argparse
import imutils
import sys
from turtlesim.msg import Pose


def talker():
	rospy.init_node('object_tracking', anonymous=True)
	pub=rospy.Publisher('/turtle/pose',Pose,queue_size=1)
	rate = rospy.Rate(1)

	colorLower = (20, 100, 100)
	colorUpper = (64, 255, 255)
	goal_pose = Pose()

	camera = cv2.VideoCapture(0)
	if not camera.isOpened():
    		raise Exception("Could not open video device")	
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

	while not rospy.is_shutdown():
		(grabbed, frame) = camera.read()
		frame = imutils.resize(frame)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, colorLower, colorUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		normalized_center = None
		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			Moment = cv2.moments(c)
			center = (int(Moment["m10"]/ Moment["m00"]),int(Moment["m01"]/Moment["m00"]))
			#normalizing value for turtlesim		
			normalized_center = (int(Moment["m10"]/(60 * Moment["m00"])),int(Moment["m01"]/(45 * Moment["m00"])))
			goal_pose.x = 10 - normalized_center[0]
			goal_pose.y = 10 - normalized_center[1]
			rospy.loginfo("Marker detected - keep smiling")
			pub.publish(goal_pose)
			#print(goal_pose)
			rate.sleep()
		else:
			rospy.loginfo("Marker is out of bound")
			pub.publish(goal_pose)
			#print(goal_pose)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			break

	rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
	video_capture.release()
	cv2.destroyAllWindows()
	pass
