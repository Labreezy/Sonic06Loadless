import queue
import sys
from datetime import timedelta

import cv2
from threading import Thread
from bs4 import BeautifulSoup
from main_06 import *

TOTAL_LOADS_MS = 0
RTA_OFFSET_MS = 1667
RUN_LEN_MS = (39*60+44)*1000
RUN_LEN_TRUE_MS = RUN_LEN_MS - 1000
CURR_RTA_MS = 0
IS_PAUSED = True
LAST_START = -1
LAST_END = -1
F_VALS = {}


frame_ts_queue = queue.Queue(maxsize=50)

fpath = ""
grabber_done = False
total_loads_ms = 0
def ls_to_ms(tstr):
    h, m, s = list(map(float, tstr.split(":")))
    return int((3600*h+60*m+s)*1000)

class FrameGrabberThread(Thread):
    def __init__(self, fpath):

        super().__init__(daemon=True)
        self.fpath = fpath

    def run(self):
        global grabber_done, RTA_OFFSET_MS, RUN_LEN_MS
        stream = cv2.VideoCapture(self.fpath)
        stream.set(cv2.CAP_PROP_POS_MSEC, RTA_OFFSET_MS)

        end_ms = RTA_OFFSET_MS + RUN_LEN_MS
        ctime_ms = RTA_OFFSET_MS
        while ctime_ms < end_ms:
            (ret, frame) = stream.read()
            if not ret:
                stream.release()
                print("NOT RET UH OH?")
                grabber_done = True
                return
            ctime_ms = stream.get(cv2.CAP_PROP_POS_MSEC)
            frame_ts_queue.put((frame, ctime_ms))
        print("GRABBER DONE GRABBING")
        stream.release()
        grabber_done = True


class ProcessorThread(Thread):
    def __init__(self,features,isloading_f,gamedims):
        super().__init__(daemon=True)
        self.gamedims = gamedims
        self.features = features
        self.is_loading = isloading_f

    def run(self):
        global grabber_done, TOTAL_LOADS_MS
        x1,y1,w,h = self.gamedims
        x2 = x1+w
        y2 = y1+h
        fvals = {f.name: 0 for f in self.features}
        last_pause_ms = 0
        last_is_paused = False
        is_paused = False
        n_frames_processed = 0
        while True:

            (frame, ctime) = frame_ts_queue.get(True)
            ctime_s = ctime/1000
            crop_frame = frame[y1:y2,x1:x2]
            rsz_frame = cv2.resize(crop_frame, (1280,720))
            for f in self.features:
                f.add_reading(rsz_frame,ctime_s)
                vals = f.get_vals(now=ctime_s)
                fvals[f.name] = np.mean(vals)
            is_paused = self.is_loading(fvals)
            if not is_paused and last_is_paused:
                print(f"START AT {ctime_s} s")
                TOTAL_LOADS_MS += (ctime - last_pause_ms)
            if is_paused and not last_is_paused:
                print(f"STOP AT {ctime_s} s")
                last_pause_ms = ctime
            last_is_paused = is_paused
            n_frames_processed += 1
            if grabber_done and frame_ts_queue.empty():
                print("DONE PROCESSING")
                break








x1,y1,x2,y2 = (21,15,21+1037,15+584)
def is_loading(fvals):
    if fvals["black"] >= .91:
        if fvals["gold"] >= .6:
            if fvals["green"] >= .8:
                return True
            return False
        return True
    if fvals["freeze"] <= 0.25:
        return True

test_features = [
    FeatureComparison("black", (40,80,107,20), normalized_l1, 0.5, color=(0, 0, 0)),
    FeatureComparison("gold", (600, 400, 67, 67), normalized_l1, 0.5, color=(255,190,5)),
    FeatureComparison("green", (1140, 368, 70, 70), normalized_l1, 0.5, (0x52,0x6b,0x29)),
    FeatureComparison("freeze", (447,160,190,343), peak_error_l1, 0.5, freeze=True),
]


def main():
    target_vidfile = sys.argv[1]
    gameplay_dims = (336,16,926,522)
    t1 = FrameGrabberThread(fpath=target_vidfile)
    t2 = ProcessorThread(features=test_features, isloading_f=is_loading, gamedims=gameplay_dims)
    print("starting")
    t1.start()
    t2.start()
    threads = [t1,t2]
    for t in threads:
        t.join()
    rta_td = timedelta(milliseconds=RUN_LEN_TRUE_MS)
    load_td = timedelta(milliseconds=TOTAL_LOADS_MS)
    lrt_td = rta_td - load_td
    print("Total Loads: " + str(load_td))
    print("Runtime: " + str(rta_td))
    print("LRT: " + str(lrt_td))



if __name__ == '__main__':
    main()








