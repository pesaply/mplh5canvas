#!/usr/bin/python

"""Simple receiver to collect png images from the test page rendered from the various HTML5 canvii
on the test page. Run this if you want to collect rendered versions of the HTML canvii generated by the test scripts."""

from mplh5canvas import simple_server, msgutil
import thread
import time
import base64

def request(request):
    while True:
        try:
            line = msgutil.receive_message(request).encode('utf-8')
            (filename, b64) = line.split(" ")
             # should be filename<space>base64png
            try:
                s = base64.b64decode(b64[22:])
                 # skip space and data:image/png;base64, header
            except Exception,e:
                print "Base64 decoding failed. Maybe not an image...",e
                break
            if s[0:5] == '\x89PNG\r':
                print "Base64 decoding passed. Writing image to ",filename
                f = open("./output/h5canvas_" + filename, "w")
                f.write(s)
                f.close()
        except Exception,e:
            print "Failed...",e
            break

wsserver = simple_server.WebSocketServer(('', 8123), request, simple_server.WebSocketRequestHandler)
wsthread = thread.start_new_thread(wsserver.serve_forever, ())
while True:
    time.sleep(1)