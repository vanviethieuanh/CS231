import cv2
import matplotlib.pyplot as plt
import numpy as np
import urllib.request as get

def AddBg(obj, mask, bg_url, scale):
    resp = get.urlopen(bg_url)
    bg = np.asarray(bytearray(resp.read()), dtype="uint8")
    bg = cv2.imdecode(bg, cv2.IMREAD_COLOR)

    h, w, _ = bg.shape
    oH, oW, _ = obj.shape

    if (w/h) > (oW/oH):
        height = np.int(h * scale)
        width = np.int((height / oH) * oW)

        obj = cv2.resize(obj, (width, height))
        mask = cv2.resize(mask, (width, height))

        mask = cv2.merge((mask,mask,mask))

        position = (np.uint8((w-width)/2), h - height)

        region = bg[position[1]:position[1]+height, position[0]: position[0]+width]
        add = region * (1-(mask/255)) + obj * (mask/255)

        bg[position[1]:position[1]+height, position[0]: position[0]+width] = add.astype('uint8')
    else:
        print((w/h), (oW/oH))
        width = np.int(w * scale)
        height = np.int((width / oW) * oH)
        print(width, height)

        obj = cv2.resize(obj, (width, height))
        mask = cv2.resize(mask, (width, height))

        mask = cv2.merge((mask,mask,mask))

        position = (np.uint8((w-width)/2), h - height)
        region = bg[position[1]:position[1]+height, position[0]: position[0]+width]
        add = region * (1-(mask/255)) + obj * (mask/255)

        bg[position[1]:position[1]+height, position[0]: position[0]+width] = add.astype('uint8')
        pass

    return bg
    pass
