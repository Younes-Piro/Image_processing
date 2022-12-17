# import the necessary packages
import numpy as np
import cv2
import imutils
import csv


class ColorDescriptor:

    def __init__(self, bins, indexPath=None):
        # store the number of bins for the 3D histogram
        self.bins = bins
        self.indexPath = indexPath

    def describe(self, image):
        # convert the image to the HSV color space and initialize
        # the features used to quantify the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        # grab the dimensions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))
    # divide the image into four rectangles/segments (top-left,# top-right, bottom-right, bottom-left)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY),
                    (cX, w, cY, h), (0, cX, cY, h)]
        # construct an elliptical mask representing the center of the
        # image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        # loop over the segments
        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting
            # the elliptical center from it
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            # extract a color histogram from the image, then update the
            # feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        # extract a color histogram from the elliptical region and
        # update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        # return the feature vector
        return features

    def histogram(self, image, mask):
            # extract a 3D color histogram from the masked region of the
            # image, using the supplied number of bins per channel
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 256, 0, 256, 0, 256])
        # normalize the histogram if we are using OpenCV 2.4
        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        # otherwise handle for OpenCV 3+
        else:
            hist = cv2.normalize(hist, hist).flatten()
        # return the histogram
        return hist

    def color_moments (filename): 
        img=cv2.imread (filename)
        if img is None:
            return
        #Convert BGR to HSV colorspace
        HSV =cv2.cvtColor(img, cv2. COLOR_BGR2HSV)
        #Split the Channels-h,s,v
        h, s, v =cv2.split(HSV)
        #Initialize the color feature
        color_feature = []  

        #The first central moment-average
        H_mean = np.mean(h)
        S_mean = np.mean(s)
        V_mean = np.mean(v)
        color_feature.extend([H_mean, S_mean, V_mean])

        #The second central Moment-standard deviation
        H_STD = np.std(h)
        S_STD = np.std(s)
        V_STD = np.std(v)
        color_feature.extend([H_STD, S_STD, V_STD])

        #The third Central moment-the third root of the skewness
        h_skewness = np.mean(abs(h - H_mean) **3)
        H_thirdmoment = h_skewness**(1./3)
        s_skewness= np.mean(abs(s - S_mean) **3)
        S_thirdmoment = s_skewness**(1./3)
        v_skewness= np.mean(abs(v - V_mean) **3)
        V_thirdmoment = v_skewness**(1./3)
        color_feature.extend ([H_thirdmoment, S_thirdmoment, V_thirdmoment])
        return color_feature
        
    def calcDistance(self, queryFeatures):
        # initialize our dictionary of results
        results = {}
        # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)
            # loop over the rows in the index
            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                # and our query features
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)
                # now that we have the distance between the two feature
                # vectors, we can udpate the results dictionary -- the
                # key is the current image ID in the index and the
                # value is the distance we just computed, representing
                # how 'similar' the image in the index is to our query
                results[row[0]] = d
            # close the reader
            f.close()
        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        return results

    def chi2_distance(self, histA, histB, eps=1e-10):
                # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                          for (a, b) in zip(histA, histB)])
        # return the chi-squared distance
        return d
