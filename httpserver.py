#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import logging
import json

class NaviPoint:
    x = 0.0
    y = 0.0
    x = 0.0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def displayNaviPoint(self):
        print ("x: %f, y: %f, z: %f\n" % (self.x, self.y, self.z))

def dict2point(d):
    return NaviPoint(d['x'], d['y'], d['z'])


PORT_NUMBER = 8080

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
        print type(np1)


        #self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        self.send_response(201)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write("zhangboshuai\n")

try:
    #Create a web server and define the handler to manage the
    #incoming request

    np = NaviPoint(0.1, 0.2, 0.3)
    np.displayNaviPoint()

    print (json.dumps(np, default=lambda obj: obj.__dict__))

    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()