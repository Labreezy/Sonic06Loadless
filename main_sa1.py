from main_06 import *
import cv2
import cv2_enumerate_cameras


class SA1VideoStreamCapture(VideoStreamCapture):
    def __init__(self, src=0, features=None, tcp_port=16834):
        super().__init__(src, features, tcp_port)
    def is_loading(self):
        if self.frame is None:
            return False
        curr_frame = self.frame
        #update features to current
        for f in self.features:
            f.add_reading(curr_frame)
            self.feature_dict[f.name] = np.mean(f.get_vals())


        if all([f > .981 for f in self.feature_dict.values()]):
            return True

LOAD_FEATURES_SA1 = [
    FeatureComparison("blacktop", (320,0,400,67), normalized_l1, 0.2, (0,0,0)),
    FeatureComparison("blackbot", (320,586,400,67), normalized_l1, 0.2, (0,0,0)),
]

if __name__ == '__main__':

    for caminfo in cv2_enumerate_cameras.enumerate_cameras(cv2.CAP_ANY):
        print(f"{caminfo.index+1}: {caminfo.name}")
    camnum = input("Camera number here:")

    capture = SA1VideoStreamCapture(int(camnum)-1,LOAD_FEATURES_SA1)
    print("Capture obtained")
    while True:
        capture.preview_frame()
        capture.update_timer()