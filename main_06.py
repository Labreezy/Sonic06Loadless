import winsound

import cv2
import cv2_enumerate_cameras
import numpy as np
from time import time, sleep
import socket
import sys
from threading import Thread

BEEP_ON_PAUSE = False
LOAD_CHANGES = []
LAST_LOAD_START = -1
class VideoStreamCapture06(object):
    def __init__(self, src=0, features=None, from_file=False, tcp_port=16834, seek_start_ms=0):
        self.capture = cv2.VideoCapture(src)
        if not from_file:
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("localhost", tcp_port))
        else:
            self.seek_start = seek_start_ms
            self.capture.set(cv2.CAP_PROP_POS_MSEC, seek_start_ms)
            self.splits = []
            self.curr_split_index = 0
        self.timer_paused = False
        self.thread = Thread(target=self.update_frame, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status = True
        self.frame = None
        self.features = features
        self.feature_dict = {f.name: 0 for f in self.features}
    def update_frame(self):
        while True:
            if self.capture.isOpened():
                self.status, self.frame = self.capture.read()
            # a little under 1f @ 60 fps
            sleep(.01)

    def is_loading(self):
        if self.frame is None:
            return False
        curr_frame = self.frame
        #update features to current
        for f in self.features:
            f.add_reading(curr_frame)
            self.feature_dict[f.name] = np.mean(f.get_vals())

        #actual loading math
        if self.feature_dict["black"] >= .910:
            if self.feature_dict["gold"] >= .60:
                if self.feature_dict["green"] >= .8:
                    return True
                return False
            return True
        if self.feature_dict["freeze"] <= 0.25:
            return True
        return False


    def preview_frame(self):
        if self.frame is None:
            return
        cv2.imshow('Capture Preview', self.frame)
        key = cv2.waitKey(1)
        #27 = Escape
        if key == 27:
            self.capture.release()
            cv2.destroyAllWindows()
            sys.exit(1)



    def update_timer(self):
        global BEEP_ON_PAUSE
        self.sock.send(b"gettimerphase\r\n")
        curr_phase = self.sock.recv(128)
        if curr_phase == b"Running\n" or BEEP_ON_PAUSE:
            load_res = self.is_loading()
            if load_res and not self.timer_paused:

                self.sock.send(b"pausegametime\n")
                self.timer_paused = True
                print("PAUSING IGT")
                if BEEP_ON_PAUSE:
                    winsound.MessageBeep()
            if not load_res and self.timer_paused:
                self.sock.send(b"unpausegametime\n")
                self.timer_paused = False
                print("UNPAUSING IGT")
        else:
            if self.timer_paused:
                self.sock.send(b"unpausegametime\n")
                self.timer_paused = False
        sleep(.025)

        def update_timer_offline(self):
            load_res = self.is_loading()



def create_blank(w, h, rgb_color=(0,0,0)):

    image = np.zeros((h,w,3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def normalized_l1(im1, im2):
    return 1-cv2.norm(im1/255, im2/255, normType=cv2.NORM_L1)/(np.prod(im1.shape))

def peak_error_l1(im1, im2):
    diff = np.abs(im1 - im2)/255
    avgs = diff.sum(axis=2)/3
    return np.max(avgs)

class FeatureComparison():
    def __init__(self, name, dims, sim_metric, keep_s, color=(0,0,0), freeze=False):
        self.name = name
        self.x1, self.y1, w, h = dims
        self.x2 = self.x1 + w
        self.y2 = self.y1 + h
        self.freeze = freeze
        self.sim_metric = sim_metric
        self.keep_s = keep_s
        self.readings = []
        if not freeze:
            self.cmp = create_blank(w,h,color)
        else:
            self.cmp = create_blank(w,h)

    def get_vals(self, now=None):
        if now is None:
            self.clean_readings()
        else:
            self.clean_readings_custom_now(now)
        return [r[0] for r in self.readings]

    def clean_readings_custom_now(self, now):
        self.readings = list(filter(lambda r: now - r[1] <= self.keep_s, self.readings))
    def clean_readings(self):
        now = time()
        self.readings = list(filter(lambda r: now-r[1] <= self.keep_s, self.readings))

    def add_reading(self,in_frame,now=None):
        subframe = in_frame[self.y1:self.y2,self.x1:self.x2]
        sim = self.sim_metric(subframe,self.cmp)
        if self.freeze:
            self.cmp = subframe

        if now is None:
            self.clean_readings()
            self.readings.append((sim,time()))
        else:
            self.clean_readings_custom_now(now)
            self.readings.append((sim,now))


LOAD_FEATURES = [
        FeatureComparison("black", (40, 80, 107, 20), normalized_l1, 0.5, color=(0, 0, 0)),
        FeatureComparison("gold", (600, 400, 67, 67), normalized_l1, 0.5, color=(255, 190, 5)),
        FeatureComparison("green", (1140, 368, 70, 70), normalized_l1, 0.5, color=(0x52, 0x6b, 0x29)),
        FeatureComparison("freeze", (447, 160, 190, 343), peak_error_l1, 0.5, freeze=True),
    ]


if __name__ == '__main__':
    if len(sys.argv) == 1:
        for caminfo in cv2_enumerate_cameras.enumerate_cameras(cv2.CAP_ANY):
            print(f"{caminfo.index+1}: {caminfo.name}")
        camnum = input("Camera number here:")

        capture = VideoStreamCapture06(int(camnum) - 1, LOAD_FEATURES)
        print("Capture obtained")
        while True:
            capture.preview_frame()
            capture.update_timer()


