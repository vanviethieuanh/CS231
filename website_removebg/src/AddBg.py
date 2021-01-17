import cv2
import matplotlib.pyplot as plt
import numpy as np
import urllib.request as get


def AddBg(obj, mask, bg_url, scale):
    resp = get.urlopen(bg_url)
    bg = np.asarray(bytearray(resp.read()), dtype="uint8")
    bg = cv2.imdecode(bg, cv2.IMREAD_COLOR)

    # WHITE BALACE -----------------------------------------------------------------
    obj_hsl = cv2.cvtColor(obj, cv2.COLOR_BGR2HSL)
    bg_hsl = cv2.cvtColor(bg, cv2.COLOR_BGR2HSL)

    obj_mean = cv2.mean(obj_hsl, mask)
    bg_mean = cv2.mean(bg_hsl)

    lightness_dis = (bg_mean - obj_mean)[2]

    t = 0.4
    lightness = obj_hsl[:, :, 2] + t*lightness_dis[2]
    lightness = np.uint8(lightness)
    obj_hsl = cv2.merge((obj_hsl[:, :, 0], obj_hsl[:, :, 1], lightness))

    obj = cv2.cvtColor(obj_hsl, cv2.COLOR_HSL2BGR)
    # ------------------------------------------------------------------------------

    h, w, _ = bg.shape
    oH, oW, _ = obj.shape

    if (w/h) > (oW/oH):
        height = np.int(h * scale)
        width = np.int((height / oH) * oW)

        obj = cv2.resize(obj, (width, height))
        mask = cv2.resize(mask, (width, height))

        mask = cv2.merge((mask, mask, mask))

        position = (np.uint8((w-width)/2), h - height)

        region = bg[position[1]:position[1] +
                    height, position[0]: position[0]+width]
        add = region * (1-(mask/255)) + obj * (mask/255)

        bg[position[1]:position[1]+height, position[0]: position[0]+width] = add.astype('uint8')
    else:
        print((w/h), (oW/oH))
        width = np.int(w * scale)
        height = np.int((width / oW) * oH)
        print(width, height)

        obj = cv2.resize(obj, (width, height))
        mask = cv2.resize(mask, (width, height))

        mask = cv2.merge((mask, mask, mask))

        position = (np.uint8((w-width)/2), h - height)
        region = bg[position[1]:position[1] +
                    height, position[0]: position[0]+width]
        add = region * (1-(mask/255)) + obj * (mask/255)

        bg[position[1]:position[1]+height, position[0]: position[0]+width] = add.astype('uint8')
        pass

    return bg
    pass
