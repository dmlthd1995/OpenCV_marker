#!/usr/bin/env python

from __future__ import print_function
import sys, getopt
import time

try:
	import cv2
	from ar_markers import detect_markers
except ImportError:
	raise Exception('Error: OpenCv is not installed')

prevTime = time.time()

def putFps(img):
    global prevTime 
    curTime = time.time() 
    sec = curTime - prevTime 
    prevTime = curTime 
    fps_val = 1/(sec)
    fps_txt = "%01.f" % fps_val
    cv2.putText(img, fps_txt, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))

def main(argv):
    cam_id = 0 #default 0
    fps_view = False
    try:
        opts, args = getopt.getopt(argv,"hc:f",["camera_id="])
    except getopt.GetoptError:
        print('default setting : cam id = 0, fps indication = disabled')

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -c < camera_id >f')
            sys.exit()
        elif opt in ("-c","--camera"):
            cam_id = int(arg)
        elif opt in ("-f", "--fps"):
            fps_view = True

    print('Press "q" to quit')
    capture = cv2.VideoCapture(cam_id)

    if capture.isOpened():  #try to get the first frame
        frame_captured, frame = capture.read()

    else:
        print('Failed to Open Camer %d' %cam_id)
        frame_captured = False

    while frame_captured:
        frame_captured, frame = capture.read()

        markers = detect_markers(frame)
    
        for marker in markers:
            marker.highlite_marker(frame)
            print ('Marker ID:',marker.id)

        if fps_view:
            putFps(frame)


        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()



if __name__=='__main__':
    main(sys.argv[1:])
