#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import logging
import json
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

class NaviPoint:
    frame_id = "map"
    x1 = 0.0
    y1 = 0.0
    z1 = 0.0
    x2 = 0.0
    y2 = 0.0
    z2 = 0.0
    w2 = 1.0

    def __init__(self, frame_id, x1, y1, z1, x2, y2, z2, w2):
        self.frame_id = frame_id
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.w2 = w2

    def displayNaviPoint(self):
        print ("frame_id: %s, x1: %f, y1: %f, z1: %f\nx2: %f, y2: %f, z2: %f, w2: %f\n" % (self.frame_id, self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.w2))

def dict2point(d):
    return NaviPoint(d['frame_id'], d['x1'], d['y1'], d['z1'], d['x2'], d['y2'], d['z2'], d['w2'])

PORT_NUMBER = 8081

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        # Send the html message
        self.wfile.write("zhangbo")
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print post_data
        logging.error("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf8'))
        np1 = json.loads(post_data.decode('utf8'), object_hook=dict2point)
        result = send_navi_goal(np1)
        if result:
            rospy.logerr("Goal exec done")

        #self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        self.send_response(201)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write("zhangboshuai\n")

    # import roslib
    # roslib.load_manifest('my_pkg_name')

def send_navi_goal(NaviPoint):
    rospy.init_node('send_navi_goal_client')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = NaviPoint.frame_id
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = NaviPoint.x1
    goal.target_pose.pose.position.y = NaviPoint.y1
    goal.target_pose.pose.position.z = NaviPoint.z1
    goal.target_pose.pose.orientation.x = NaviPoint.x2
    goal.target_pose.pose.orientation.y = NaviPoint.y2
    goal.target_pose.pose.orientation.z = NaviPoint.z2
    goal.target_pose.pose.orientation.w = NaviPoint.w2

    # Fill in the goal here
    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not avil")
        rospy.signal_shutdown("Action server not avilable")
    else:
        return client.get_result()

try:
    #Create a web server and define the handler to manage the
    #incoming request
    #np = NaviPoint('map', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    #np.displayNaviPoint()
    #print (json.dumps(np, default=lambda obj: obj.__dict__))

    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
