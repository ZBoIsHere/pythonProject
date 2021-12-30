#!/usr/bin/python
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import actionlib
import rospy
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
import navipoint

PORT_NUMBER = 8081

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write('success access navi task plugin\n'.encode())
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        rospy.loginfo("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf8'))

        np1 = navipoint.json2MessageDomain(post_data.decode('utf8'))
        task = threading.Thread(target=send_navi_goal, args=[np1])
        task.start()

        ret = navipoint.MessageSendResultDomain()
        ret.robot_id = np1.robot_id
        ret.status = navipoint.SendSuccess
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(ret, default=lambda obj: obj.__dict__).encode())

def send_navi_goal(np):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = np.message.header.frame_id
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = np.message.pose.pose.position.x
    goal.target_pose.pose.position.y = np.message.pose.pose.position.y
    goal.target_pose.pose.position.z = np.message.pose.pose.position.z
    goal.target_pose.pose.orientation.x = np.message.pose.pose.orientation.x
    goal.target_pose.pose.orientation.y = np.message.pose.pose.orientation.y
    goal.target_pose.pose.orientation.z = np.message.pose.pose.orientation.z
    goal.target_pose.pose.orientation.w = np.message.pose.pose.orientation.w

    # Fill in the goal here
    client.send_goal(goal)
    doneBeforeTimeout = client.wait_for_result(rospy.Duration(1.0))
    if not doneBeforeTimeout:
        rospy.logerr("Action server not avil")
        rospy.signal_shutdown("Action server not avilable")
    else:
        ret = client.get_state()
        rospy.loginfo('task done : %s', ret.__str__())

try:
    rospy.init_node('send_navi_goal_client1')
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    rospy.loginfo('Started httpserver on port %d', PORT_NUMBER)
    server.serve_forever()

except KeyboardInterrupt:
    rospy.loginfo('^C received, shutting down the web server')
    server.socket.close()