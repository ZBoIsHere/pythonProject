from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from RobotCommander import RobotCommander
import json
import actionlib
import rospy
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

def executor(task_id):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    task = taskGroup[task_id.__str__()]
    command = task['command']
    nextTaskId = task['next']
    theta = task['theta']
    qua = quaternion_from_euler(0, 0, theta)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = task['x']
    goal.target_pose.pose.position.y = task['y']
    goal.target_pose.pose.position.z = task['z']
    goal.target_pose.pose.orientation.x = qua[0]
    goal.target_pose.pose.orientation.y = qua[1]
    goal.target_pose.pose.orientation.z = qua[2]
    goal.target_pose.pose.orientation.w = qua[3]

    client.send_goal(goal)

    state = client.wait_for_result()
    if state == actionlib.SimpleGoalState.PENDING:
        rospy.logerr("Action server not avil")
        rospy.signal_shutdown("Action server not avilable")
    else:
        rospy.loginfo('task done : %s', state)

    if command > 0:
        with RobotCommander as rc:
            rc.sendSimple(command)

    return nextTaskId

#with open('../waypoints.json', 'r') as load_f:
with open('../turtlebot3waypoints.json', 'r') as load_f:
    taskGroup = json.load(load_f)

def initialRobo():
    with RobotCommander() as rc:
        rc.stand_down_up()
        rospy.sleep(5.0)
        rc.start_force_mode()
        rospy.sleep(2.0)
        rc.motion_start_stop()
        rospy.sleep(2.0)

if __name__ == '__main__':
    rospy.init_node('task_executor')
    #initialRobo()
    TASK_NUM = taskGroup['0']['total']
    print('task num %d', TASK_NUM)
    '''
    doneTaskNum = 0
    nextTaskId = 1
    while doneTaskNum < TASK_NUM:
        nextTaskId = executor(nextTaskId)
        doneTaskNum += 1
    '''
    stopTask = False
    nextTaskId = 1
    while not stopTask:
        nextTaskId = executor(nextTaskId)