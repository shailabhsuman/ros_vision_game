#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String, Float64
from PyQt4 import QtGui
from PyQt4.QtGui import QLabel, QVBoxLayout, QHBoxLayout, QSlider, QPushButton, QProgressBar
from PyQt4.QtCore import Qt

class PyGui(QtGui.QWidget):

	def __init__(self):
	        super(PyGui, self).__init__()
	        self.setObjectName('PyGui')
	        self.pub = rospy.Publisher("Score", String, queue_size=10)
		self.game_subscriber = rospy.Subscriber('/gamecontrol',
							Float64, self.update_game)
	        rospy.init_node('pyqt_gui')
	        self.current_value = 0
		self.distance = 0.0
	        my_layout = QHBoxLayout()
        	my_btn = QPushButton()
        	my_btn.setText("Publisher")
        	my_btn.setFixedWidth(130)
        	my_btn.clicked.connect(self.publish_topic)
        	my_layout.addWidget(my_btn)
        	my_layout.addSpacing(50)
        	self.my_label = QLabel()
        	self.my_label.setFixedWidth(140)
        	self.my_label.setText("value: " + str(0))
        	self.my_label.setEnabled(False)
        	my_layout.addWidget(self.my_label)
        	my_slider = QSlider()
        	my_slider.setMinimum(0)
        	my_slider.setMaximum(99)
        	my_slider.setOrientation(Qt.Horizontal)
        	my_slider.valueChanged.connect(self.changeValue)
		#self.my_progress = QProgressBar()

        	my_vlay = QVBoxLayout()
        	#my_vlay.addWidget(self.my_progress)
        	layout = QVBoxLayout()
        	layout.addLayout(my_layout)
        	layout.addLayout(my_vlay)
        	self.setLayout(layout)
        	# self.show()

	def publish_topic(self):
	        self.pub.publish(str(self.current_value))

	def changeValue(self, value):
        	self.current_value = value

	def update_game(self, data):
	        self.my_label.setText(str(data))
		self.distance = data
 

if __name__ == "__main__":
    app=QtGui.QApplication(sys.argv)
    pyShow = PyGui()
    pyShow.show()
    sys.exit(app.exec_())
