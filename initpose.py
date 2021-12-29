'''
from geometry_msgs.msg import PoseWithCovarianceStamped
import rospy
def __pub_initial_position(self, x, y, theta):
        initpose = PoseWithCovarianceStamped()
        initpose.header.stamp = rospy.get_rostime()
        initpose.header.frame_id = "map"
        initpose.pose.pose.position.x = x
        initpose.pose.pose.position.y = y
        quaternion = self.__yaw_to_quat(theta)

        initpose.pose.pose.orientation.w = quaternion[0]
        initpose.pose.pose.orientation.x = quaternion[1]
        initpose.pose.pose.orientation.y = quaternion[2]
        initpose.pose.pose.orientation.z = quaternion[3]
        self.__initialpose_pub.publish(initpose)
        return
'''

#!/usr/bin/env python
import rospy
import math
import time
import random
from tf import transformations
from geometry_msgs.msg import PoseWithCovarianceStamped
class PoseSetter(rospy.SubscribeListener):
    def __init__(self, pose):
        self.pose = pose
    def peer_subscribe(self, topic_name, topic_publish, peer_publish):
        p = PoseWithCovarianceStamped()
        p.header.frame_id = "map"
        p.pose.pose.position.x = self.pose[0]
        p.pose.pose.position.y = self.pose[1]
        (p.pose.pose.orientation.x,
        p.pose.pose.orientation.y,
        p.pose.pose.orientation.z,
        p.pose.pose.orientation.w) = transformations.quaternion_from_euler(0, 0, self.pose[2])
        p.pose.covariance[6*0+0] = 0.5 * 0.5
        p.pose.covariance[6*1+1] = 0.5 * 0.5
        p.pose.covariance[6*3+3] = math.pi/12.0 * math.pi/12.0
        peer_publish(p)
def initpose():
    pub = rospy.Publisher("initialpose", PoseWithCovarianceStamped, queue_size=10)
    rospy.init_node('pose_setter1', anonymous=True)
    pose1 = PoseWithCovarianceStamped()
    pose1.header.frame_id = 'map'
    pose1.header.stamp = rospy.Time.now()
    #pose1.pose.pose.position.x = float(random.randint(1,5))
    pose1.pose.pose.position.y = 1.0
    pose1.pose.pose.orientation.w = 1.0
    #pub.publish(PoseSetter(pose))
    while not rospy.is_shutdown():
        pose1.pose.pose.position.x = float(random.randint(-5, 5))
        pose1.pose.pose.orientation.x = float(random.randint(-90, 90))
        pose1.pose.pose.orientation.y = float(random.randint(-90, 90))
        pub.publish(pose1)
        rospy.loginfo('pub pose')
        time.sleep(5)

if __name__ == '__main__':
    try:
        initpose()
    except rospy.ROSInterruptException:
        pass
