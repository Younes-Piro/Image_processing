# import the necessary packages
import imutils
import cv2

class RGBHistogram:
    def __init__(self, bins):
        # stocke le nombre de cases que l’histogramme utilisera
        self.bins = bins

    def describe(self, image):

        hist = cv2.calcHist([image], [0, 1, 2],
        None, self.bins, [0, 256, 0, 256, 0, 256])

        # normalise avec OpenCV 2.4
        if imutils.is_cv2():
            hist = cv2.normalize(hist)

        else:
            hist = cv2.normalize(hist,hist)

        return hist.flatten()
