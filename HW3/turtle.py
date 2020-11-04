#! /usr/bin/env python
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber
import math

class Follower:
    def __init__(self):
        self.pose = Pose()
        self.pub = Publisher('/leo/cmd_vel', Twist, queue_size=10)
        self.sub1 = Subscriber('/turtle1/pose', Pose, self.follow)
        self.sub2 = Subscriber('/leo/pose', Pose, self.get_pos)
        
      
    def get_pos(self, pose):
        self.pose = pose
        
    def follow(self, pose):
        twist = Twist()
        distance = math.sqrt((pose.y - self.pose.y) ** 2 + (pose.x - self.pose.x)**2)
        
	angle = math.atan2(pose.y - self.pose.y, pose.x - self.pose.x) - self.pose.theta
	while angle > math.pi:
	    angle -= 2 * math.pi
	while angle < - math.pi:
	    angle += 2 * math.pi
	twist.linear.x = min(distance, 2)
	twist.angular.z = angle

	if distance > 1e-1:
            self.pub.publish(twist)  
                
if __name__ == '__main__':
    rospy.init_node('follower')
    Follower()
    rospy.spin()
