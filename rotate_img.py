import cv2
import numpy as np
import functions.function as func
import time
import matplotlib.pyplot as plt
import os
file_list = os.listdir('D:/cmd_prac/deblur_tool-NAFNet-/upload/output')
img_num00 = 0
for file in file_list:
    try:        
        img = cv2.imread('D:/cmd_prac/deblur_tool-NAFNet-/upload/output/%s' % file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # img = ~ cv2.inRange(img, (0, 0, 25), (180, 65, 255)) #camera
        img = ~ cv2.inRange(img, (0, 0, 67), (180, 43, 255)) #iphone
        img = cv2.medianBlur(img, 3)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # img = cv2.erode(img, kernel) # 擴張
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
        # img = cv2.dilate(img, kernel) # 侵蝕
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        # img = cv2.erode(img, kernel) 
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # img = cv2.dilate(img, kernel)
        img = cv2.resize(img, dsize=(img.shape[1] // 5 * 3, img.shape[0] // 5 * 3), interpolation=cv2.INTER_CUBIC) # 將圖片縮小一些
        


        # img = ~ cv2.inRange(img, (0, 0, 67), (180, 43, 255))
        # img = cv2.medianBlur(img, 2)
        # # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        # # img = cv2.dilate(img, kernel) # 侵蝕
        # # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # # img = cv2.erode(img, kernel) # 擴張
        # img = cv2.resize(img, dsize=(img.shape[1] // 5 * 3, img.shape[0] // 5 * 3), interpolation=cv2.INTER_CUBIC) # 將圖片縮小一些
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        img = func.mix_rotate(img) # 旋轉圖片
        # ============================================上下邊界
        h, w = img.shape[0:]
        sum_h = np.zeros(h)
        for i in range(h):
            for j in range(w):
                if img[i][j] == 0: # 0 = black, 255 = white
                    sum_h[i] += 1 # 紀錄整張圖片每個row的黑點數
        avg_total = 0 # 有黑點的row的數量
        avg = 0 # 平均黑點數
        for i in range(h):
            if sum_h[i] != 0:
                avg += sum_h[i]
                avg_total += 1
        avg /= avg_total

        top_avg = avg / 4 # 用來找切割圖片的上緣
        under_avg = avg / 3 * 2 # 用來找切割圖片的下緣

        top_bound = 0
        under_bound = 0
        for i in range(0, h, 1):
            if sum_h[i] >= top_avg: # 由上而下第一個符合條件的row
                top_bound = i
                break
        for i in range(h-1, -1, -1): # 由下而上第一個符合條件的row
            if sum_h[i] >= under_avg:
                under_bound = i
                break
        # ============================================上下邊界

        img_list = func.cut_the_num(img[top_bound:under_bound, :]) # 只取上下邊界之間的pixel進入cut_the_num中 回傳一個存個別數字的list
        # cv2.imshow('img0', img[top_bound:under_bound, :])
        # cv2.waitKey(0)
        for index, i in enumerate(img_list):
            # i[0] = cut_img, i[1] = x_little
            h, w = i[0].shape[0:]
            if (100 - w) % 2 != 0 and (100 - h) % 2 != 0 : # 將回傳得個別數字padding成100 * 100得圖片
                i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2 + 1, (100 - h) // 2, (100 - w) // 2 + 1, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
            elif (100 - h) % 2 != 0 :
                i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2 + 1, (100 - h) // 2, (100 - w) // 2, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
            elif (100 - w) % 2 != 0 :
                i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2, (100 - h) // 2, (100 - w) // 2 + 1, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
            else :
                i[0] = cv2.copyMakeBorder(i[0], (100 - h) // 2, (100 - h) // 2, (100 - w) // 2, (100 - w) // 2, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
                
            i[0] = cv2.resize(i[0], (28, 28), interpolation = cv2.INTER_LINEAR) # 變成28*28的圖片
            # cv2.imshow('img', i[0])
            # cv2.waitKey(0)
            # cv2.imwrite('D://deblur9/num_tf_%d_%d.jpg' % (img_num00, index), i)
            # cv2.imwrite('D://tesseract_data_generate/1008/num_tf_%d_%d.jpg' % (img_num00, i[1]), i[0])
            cv2.imwrite('D:/cmd_prac/rotated_img/rotated_img_%d_%d.jpg' % (img_num00, i[1]), i[0])
        # =================================================================================================
        img_num00 += 1
    except :
        img_num00 += 1
