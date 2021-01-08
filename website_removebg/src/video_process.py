import AddBg as add
import RemoveBg as rm
import cv2
import numpy as np

def cal_hist(img_vec):
    hist = np.zeros(256, np.int)
    values, counts = np.unique(img_vec, return_counts=True)
    for i, val in enumerate(values):
        hist[val] = counts[i]
    return hist

def lerp(v0, v1, t):
    return (1-t)*v0+t*v1
def process_video(video_object_path = None, background_path = None):

    if video_object_path == None:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(video_object_path)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        obj, mask = rm.RemoveBg().remove_background(frame, rm.Algorithm['Canny'], 6)
        result = add.AddBg(obj,mask,background_path,0.8)
        # Bước 2: Covert sang hệ màu HSV
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        mean = cv2.mean(rm.RemoveBg().url_to_image(background_path))
        
        print(mean)
        t = 0.2
        value = (1-t)*hsv[:,:, 2] + t*mean[2]
        value = np.uint8(value)
        
        img_result = cv2.merge((hsv[:,:,0], hsv[:, :, 1], value))

        # # Bước 3: Cân bằng histogram cho kênh V --> V*
        # value_vec = value.reshape(-1)

        # hist = cal_hist(value_vec)
        # # plt.bar(range(0,256), hist)

        # cdf = np.cumsum(hist)

        # cdf_min = np.min(cdf)
        # h = (cdf - cdf_min) / (cdf[-1] - cdf_min) * 255
        # h = h.astype(np.int)

        # value_eq = np.copy(value)
        # for v in range(256):
        #     value_eq[value==v] = h[v]

        # value_vec = value_eq.reshape(-1)
        # hist = cal_hist(value_vec)
        # # plt.bar(range(0,256), hist)

        # # Bước 4: Ráp lại thành kênh màu HSV*
        # hsv[:, :, 2] = value_eq
        # Bước 5: Convert về RGB
        img_result = cv2.cvtColor(img_result, cv2.COLOR_HSV2BGR)




        # Display the resulting frame
        cv2.imshow('frame', img_result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

process_video(video_object_path = 'GREEN_SCREEN_ANIMALS__ALPACA.mov', background_path='https://png.pngtree.com/thumb_back/fw800/back_pic/04/19/67/44582c6d6aa377e.jpg')