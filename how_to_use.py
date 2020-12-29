import scr.RemoveBg as rm
import scr.AddBg as add
import cv2

obj, mask = rm.RemoveBg().remove_background(rm.RemoveBg().url_to_image('https://i.ytimg.com/vi/m9_uc4ggQyk/maxresdefault.jpg'), rm.Algorithm['Laplacian'] ,6)
result = add.AddBg(obj,mask,'https://travelgear.vn/blog/wp-content/uploads/2019/08/dia-diem-du-lich-va-canh-dep-nhat-ban.jpg',1)

cv2.imwrite('result.jpg',result)
