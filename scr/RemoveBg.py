import cv2
import matplotlib.pyplot as plt
import numpy as np
import urllib.request as get

class RemoveBg:
    """
    Remove Background 🌲

    To create a mask, call remove_backround function.
    """
    def __init__(self):
        self.disc = lambda d: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d, d))
        pass

    def remove_background(self, url, sigmoi):
        """
        url: path to file 👉
        sigmoi: value of sigmoi for all channels 
        """

        img = self.url_to_image(url)

        grace = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # find edge        
        gd = self.calc_energy(img)
        _, gd = cv2.threshold(gd, 127, 255, cv2.THRESH_BINARY)
        gd = np.uint8(gd)
        gd = cv2.morphologyEx(gd, cv2.MORPH_OPEN, self.disc(5))
        
        # localize biggest rectangle that contain all edge
        x,y,w,h = cv2.boundingRect(gd)
        mask = np.ones(grace.shape, np.uint8) * 255
        cv2.rectangle(mask, (x,y),(x+w, y+h), 0, -1)

        # Statistics
        std = cv2.meanStdDev(hsv, mask=mask)
        mask = np.zeros(grace.shape, np.uint8)
        select = [std[0] - sigmoi*std[1], std[0] + sigmoi*std[1]]
        mask = 255 - cv2.inRange(hsv, select[0], select[1])
        
        return mask

    def calc_energy(self, img):
        filter_du = np.array([
            [1.0, 2.0, 1.0],
            [0.0, 0.0, 0.0],
            [-1.0, -2.0, -1.0],
        ])

        filter_dv = np.array([
            [1.0, 0.0, -1.0],
            [2.0, 0.0, -2.0],
            [1.0, 0.0, -1.0],
        ])

        img = img.astype('float32')
        convolved = np.absolute(cv2.filter2D(img,-1,filter_du)) + np.absolute(cv2.filter2D(img,-1,filter_dv))

        energy_map = convolved.sum(axis=2)
        return energy_map

    def url_to_image(self, url):
	    resp = get.urlopen(url)
	    image = np.asarray(bytearray(resp.read()), dtype="uint8")
	    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	    # return the image
	    return image


