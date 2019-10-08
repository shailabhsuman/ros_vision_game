# auto1
Single player game using ROS, OpenCV and turtlesim

# Theme of the game 
There are two turtles - husband and wife in the scene. Wife turtle needs some me time while husband turtle will follow her. Wife turtle can be controlled by you using camera. Make her swim away from husband. The longer she is alone the more points you have. I scored 67, how much can you? 

# What you need
All you need to play this game is a green round object. 

# Install turtlebot
sudo apt-get install ros-kinetic-turtlesim
sudo apt-get install ros-kinetic-ros-tutorials ros-kinetic-geometry-tutorials

# How to play
Open two terminals and launch following files
1. roslaunch src/auto1/launch/turtle_game.launch
2. roslaunch turtle_tf turtle_tf_demo.launch

# What to expect
Three windows will pop up. One would be the view of the camera of the computer, another would be ros turtlesim window and third would your score. Once you are done, restart the game using launch files to play again 
 
# OpenCV initial inspiration and credits
https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
