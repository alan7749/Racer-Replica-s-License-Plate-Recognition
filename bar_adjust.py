import cv2
import numpy as np
import functions.function as func


cv2.namedWindow('img')
hl = 0
hh = 0
sl = 0
sh = 0
vl = 0
vh = 0
def nothing(x):
    pass
cv2.createTrackbar('hl', 'img', 0, 180, nothing)
cv2.createTrackbar('hh', 'img', 0, 180, nothing)
cv2.createTrackbar('sl', 'img', 0, 255, nothing)
cv2.createTrackbar('sh', 'img', 0, 255, nothing)
cv2.createTrackbar('vl', 'img', 0, 255, nothing)
cv2.createTrackbar('vh', 'img', 0, 255, nothing)

while(1):
    img = cv2.imread('D:/deblur_model/NAFNet/upload/output/frame_34.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hl = cv2.getTrackbarPos('hl', 'img')
    hh = cv2.getTrackbarPos('hh', 'img')
    sl = cv2.getTrackbarPos('sl', 'img')
    sh = cv2.getTrackbarPos('sh', 'img')
    vl = cv2.getTrackbarPos('vl', 'img')
    vh = cv2.getTrackbarPos('vh', 'img')
    img = ~ cv2.inRange(img, (hl, sl, vl), (hh, sh, vh))
    
    # img = ~ cv2.inRange(img, (0, 0, 25), (180, 65, 255))
    # img = ~ cv2.inRange(img, (0, 0, 67), (180, 43, 255))
    img = ~ cv2.inRange(img, (0, 0, 93), (180, 43, 255))
    # img = cv2.medianBlur(img, 3)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    # img = cv2.resize(img, dsize=(img.shape[1] // 5 * 3, img.shape[0] // 5 * 3), interpolation=cv2.INTER_CUBIC) # 將圖片縮小一些
    # img = func.mix_rotate(img) # 旋轉圖片


    # h, w = img.shape[0:]
    # sum_h = np.zeros(h)
    # for i in range(h):
    #     for j in range(w):
    #         if img[i][j] == 0: # 0 = black, 255 = white
    #             sum_h[i] += 1 # 紀錄整張圖片每個row的黑點數
    # avg_total = 0 # 有黑點的row的數量
    # avg = 0 # 平均黑點數
    # for i in range(h):
    #     if sum_h[i] != 0:
    #         avg += sum_h[i]
    #         avg_total += 1
    # avg /= avg_total

    # top_avg = avg / 4 # 用來找切割圖片的上緣
    # under_avg = avg / 3 * 2 # 用來找切割圖片的下緣

    # top_bound = 0
    # under_bound = 0
    # for i in range(0, h, 1):
    #     if sum_h[i] >= top_avg: # 由上而下第一個符合條件的row
    #         top_bound = i
    #         break
    # for i in range(h-1, -1, -1): # 由下而上第一個符合條件的row
    #     if sum_h[i] >= under_avg:
    #         under_bound = i
    #         break
    # # ============================================上下邊界

    # img_list = func.cut_the_num(img[top_bound:under_bound, :]) # 只取上下邊界之間的pixel進入cut_the_num中 回傳一個存個別數字的list
    # print(len(img_list))
    # cv2.imshow('img0', img[top_bound:under_bound, :])
    # cv2.waitKey(0)
    # cv2.imshow('img0', img_list[0][0])
    # cv2.waitKey(0)
    # cv2.imshow('img0', img_list[1][0])
    # cv2.waitKey(0)
    # cv2.imshow('img0', img_list[2][0])
    # cv2.waitKey(0)
    # cv2.imshow('img0', img_list[3][0])
    # cv2.waitKey(0)
    # for index, i in enumerate(img_list):
    #     # i[0] = cut_img, i[1] = x_little
    #     h, w = i[0].shape[0:]
    #     print(h, w)
    #     if (100 - w) % 2 != 0 and (100 - h) % 2 != 0 : # 將回傳得個別數字padding成200 * 200得圖片
    #         i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2 + 1, (100 - h) // 2, (100 - w) // 2 + 1, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
    #     elif (100 - h) % 2 != 0 :
    #         i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2 + 1, (100 - h) // 2, (100 - w) // 2, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
    #     elif (100 - w) % 2 != 0 :
    #         i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2, (100 - h) // 2, (100 - w) // 2 + 1, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
    #     else :
    #         i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2, (100 - h) // 2, (100 - w) // 2, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
            
    #     i[0] = cv2.resize(i[0], (28, 28), interpolation = cv2.INTER_LINEAR) # 變成28*28的圖片
    #     cv2.imshow('img', i[0])
    #     cv2.waitKey(0)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()