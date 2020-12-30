import cv2
import threading
from queue import Queue

from PIL import Image
from PIL import ImageTk
import tkinter as tk
import sys

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
    vc = cv2.VideoCapture(0)
    if not vc.isOpened():
        print("Can't open the video stream.  Quitting!")
        sys.exit()
    ret,frame = vc.read()
    if not ret:
        print("Can't get an image from the video stream. Quitting!")
        sys.exit()

    window = tk.Tk()

    #Take the image and turn it into something tkinter can use
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    tmp_im = Image.fromarray(image)
    disp_im = ImageTk.PhotoImage(tmp_im)

    im_spot = tk.Label(image=disp_im)
    im_spot.image = disp_im
    im_spot.grid(column=0, row=0)
    window.mainloop()

    '''
    #First, setup the cv2 capture thread
    captured_queue= Queue()
    ct = CaptureThread(captured_queue)
    capture_thread = threading.Thread(target=ct.runit)
    BlobGui().run()
    '''