import queue
import sys
from datetime import timedelta

import cv2
from threading import Thread
from bs4 import BeautifulSoup
from tqdm import tqdm

from main_06 import *
from main_unwiished import *

TOTAL_LOADS_MS = 0
RTA_OFFSET_MS = 0
RUN_LEN_MS = (240+55)*1000
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

def pretty_string_ts(ms):
    return str(timedelta(milliseconds=ms))

class ProcessorThread(Thread):
    def __init__(self,features,isloading_f,gamedims,logf):
        super().__init__(daemon=True)
        self.gamedims = gamedims
        self.features = features
        self.is_loading = isloading_f
        self.logf = logf

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
        old_stdout = sys.stdout
        t = tqdm(total=RUN_LEN_MS,bar_format="{l_bar}{bar} ETA: {remianing} Elapsed: {elapsed}")
        last_ctime = RTA_OFFSET_MS
        while True:

            (frame, ctime) = frame_ts_queue.get(True)
            ctime_s = ctime/1000
            frame_w, frame_h = frame.shape[:2]

            if not (w == frame_w and h == frame_h):
                crop_frame = frame[y1:y2,x1:x2]
                frame = cv2.resize(crop_frame, (1280,720))
            for f in self.features:
                f.add_reading(frame,ctime_s)
                vals = f.get_vals(now=ctime_s)
                fvals[f.name] = np.mean(vals)
            is_paused = self.is_loading(fvals)
            if not is_paused and last_is_paused:
                print(f"Loaded From {pretty_string_ts(last_pause_ms)} -> {pretty_string_ts(ctime)}")
                print(fvals)
                TOTAL_LOADS_MS += (ctime - last_pause_ms)
            if is_paused and not last_is_paused:
                last_pause_ms = ctime
            last_is_paused = is_paused
            t.update(ctime-last_ctime)
            n_frames_processed += 1
            if grabber_done and frame_ts_queue.empty():
                print("DONE PROCESSING")
                break








x1,y1,x2,y2 = (370,29,370+881,29+661)
def is_loading(fvals):
    return fvals['mainglobe'] >= 0.88 and fvals['black_above'] >= 0.97

test_features = []


def main():
    global RUN_LEN_MS, RTA_OFFSET_MS
    target_vidfile = sys.argv[1]
    #gameplay_dims = (370,29,881,661)
    x1 = int(input("X coordinate of top-left corner of gameplay")) or 0
    y1 = int(input("Y coordinate of top-left corner of gameplay")) or 0
    w = int(input("Width of gameplay")) or 1280
    h = int(input("Height of gameplay")) or 720
    run_start_str = input("Run Start (hh:mm:ss.uuu), decimals optional")
    RTA_OFFSET_MS = ls_to_ms(run_start_str)
    run_len_str = input("Run Length (hh:mm:ss.uuu), again")
    RUN_LEN_MS = ls_to_ms(run_len_str)
    old_stdout = sys.stdout
    log_path = target_vidfile+".txt"
    print("Saving Log to " + log_path)
    gameplay_dims = (x1,y1,w,h)

    globe_img = cv2.imread("globe_wii.png")
    test_features = [
        ImageFeatureComparison("mainglobe", (560, 270, 160, 160), normalized_l1, 0.5, globe_img),
        FeatureComparison("black_above", (560,150,160,160), normalized_l1, 0.2, color=(0,0,0))
    ]
    t1 = FrameGrabberThread(fpath=target_vidfile)
    t2 = ProcessorThread(features=test_features, isloading_f=is_loading, gamedims=gameplay_dims)
    print("starting")
    with open(log_path, "w") as logf:
        sys.stdout = logf
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
        print("Loadless: " + str(lrt_td))
    sys.stdout = old_stdout
    print("Total Loads: " + str(load_td))
    print("Runtime: " + str(rta_td))
    print("Loadless: " + str(lrt_td))


if __name__ == '__main__':
    main()





