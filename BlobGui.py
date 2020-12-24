import kivy
import cv2
import threading
from queue import Queue

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.texture import Texture

class BlobGui(App):
    def build(self):
        return Button(text="Blob Threshold Tuning")

class CaptureThread:
    def __init__(self, out_queue, vid_num=0):
        self.vc = cv2.VideoCapture(vid_num)
        if not self.vc.isOpened():
            raise Exception(f'Unable to open Video Capture Device specified ({vid_num})')
        self.oq = out_queue
    
    def __del__(self):
        self.vc.release()
    
    def getWidth(self):
        return self.vc.get(cv2.CAP_PROP_FRAME_WIDTH)

    def getHeight(self):
        return self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def getFPS(self):
        return self.vc.get(cv2.CAP_PROP_FPS)
    
    def runit(self,queue, mutex):
        while self.vc.isOpened():
            ret,frame = vc.read()
            if ret:
                #put frame in output-queue
                self.oq.put(frame)


if __name__ == "__main__":
    #First, setup the cv2 capture thread
    captured_queue= Queue()
    ct = CaptureThread(captured_queue)
    capture_thread = threading.Thread(target=ct.runit)
    BlobGui().run()
