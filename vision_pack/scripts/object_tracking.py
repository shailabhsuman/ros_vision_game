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
	pub=rospy.Publisher('/turtle1/pose',Pose,queue_size=1)
	rate = rospy.Rate(20)

	colorLower = (20, 100, 100)
	colorUpper = (64, 255, 255)
	pts = deque(maxlen=32)
	goal_pose = Pose()

	camera = cv2.VideoCapture(0)

	while not rospy.is_shutdown():
		(grabbed, frame) = camera.read()
		frame = imutils.resize(frame, width=600)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, colorLower, colorUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			Moment = cv2.moments(c)
			center = (int(Moment["m10"]/ Moment["m00"]),int(Moment["m01"]/Moment["m00"]))
			#normalizing value for turtlesim			
			goal_pose.x = int(Moment["m10"] *2/ (100* Moment["m00"]))
			goal_pose.y = int(Moment["m01"] *2 / (100*Moment["m00"]))
			pub.publish(goal_pose)
			rate.sleep()
			if radius > 15:
				cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
		pts.appendleft(center)
		for i in xrange(1, len(pts)):
			if pts[i - 1] is None or pts[i] is None:
				continue
			thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

		cv2.imshow("Frame", frame)
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
