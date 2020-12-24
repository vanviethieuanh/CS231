import cv2
import matplotlib.pyplot as plt
import numpy as np
import urllib.request as get

def AddBg(obj, mask, bg, scale):
    """
    docstring
    """
    h, w, _ = bg.shape
    oH, oW, _ = obj.shape

    height = np.int(h * scale)
    width = np.int((height / oH) * oW)

    obj = cv2.resize(obj, (width, height))
    mask = cv2.resize(mask, (width, height))

    mask = cv2.merge((mask,mask,mask))

    position = (np.uint8((w-oW)/2), h - height)

    region = bg[position[1]:position[1]+height, position[0]: position[0]+width]
    add = region * (1-(mask/255)) + obj * (mask/255)

    bg[position[1]:position[1]+height, position[0]: position[0]+width] = add.astype('uint8')

    return bg
    pass
