#import roslib
#roslib.load_manifest('my_pkg_name')
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseAction

if __name__ == '__main__':
    rospy.init_node('send_navi_goal_client')
    client = actionlib.SimpleActionClient('send_navi_goal', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseActionGoal()

    # Fill in the goal here
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))
    rospy.spin()
    rospy.signal_shutdown()