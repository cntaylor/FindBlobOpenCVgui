import cv2
import threading
from queue import Queue

import PIL.Image
import PIL.ImageTk
import tkinter as tk
import sys


#This class shamelessly stolen from https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


if __name__ == "__main__":
    vc = MyVideoCapture(0)
    window = tk.Tk()
    ret,frame = vc.get_frame()

    if not ret:
        sys.exit("No frame captured :(")
    # Run a blob detection
    detector = cv2.SimpleBlobDetector()
    
    detect_im = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    keypoints = detector.detect(detect_im)
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]),(0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPONITS)

    #Take the image and turn it into something tkinter can use
    image = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2RGB)
    tmp_im = PIL.Image.fromarray(image)
    disp_im = PIL.ImageTk.PhotoImage(tmp_im)

    im_spot = tk.Label(image=disp_im)
    im_spot.grid(column=0, row=0)\

    window.mainloop()
