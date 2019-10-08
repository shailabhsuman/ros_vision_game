#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String, Float64
from PyQt4 import QtGui
from PyQt4.QtGui import QLabel, QVBoxLayout, QHBoxLayout, QSlider, QPushButton, QProgressBar
from PyQt4.QtCore import Qt
from std_srvs.srv import Empty as EmptyServiceCall
import signal

class PyGui(QtGui.QWidget):

	def __init__(self):
	        super(PyGui, self).__init__()
	        self.setObjectName('PyGui')
	        self.pub = rospy.Publisher("/score", Float64, queue_size=10)
		self.game_subscriber = rospy.Subscriber('/gamecontrol',
							Float64, self.update_game)
	        rospy.init_node('pyqt_gui')
	        self.current_value = 0
		self.distance = 0.0
	        my_layout = QHBoxLayout()
        	#my_btn = QPushButton()
        	#my_btn.setText("Reset Score")
        	#my_btn.setFixedWidth(130)
        	#my_btn.clicked.connect(self.clear_area)
        	#my_layout.addWidget(my_btn)
        	#my_layout.addSpacing(50)
        	self.my_label = QLabel()
        	self.my_label.setFixedWidth(140)
        	self.my_label.setText("Score: " + str(0))
        	self.my_label.setEnabled(False)
        	my_layout.addWidget(self.my_label)
        	my_vlay = QVBoxLayout()
        	layout = QVBoxLayout()
        	layout.addLayout(my_layout)
        	layout.addLayout(my_vlay)
        	self.setLayout(layout)

	#def clear_area(self):
	#	self.distance.data = 0.0


	def update_game(self, data):
		self.distance = data
		self.my_label.setText("Score: " + str(self.distance.data))
 

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app=QtGui.QApplication(sys.argv)
	pyShow = PyGui()
	pyShow.show()
	sys.exit(app.exec_())

