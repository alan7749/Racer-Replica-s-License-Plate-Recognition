import cv2
import numpy as np
import matplotlib.pyplot as plt

imgshow_flag = 0
def reflection_remove(img):
    # cv2.imshow('img', img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # print(hsv[0][0])
    
    cv2.imshow('hsv', hsv)
    cv2.waitKey(0)
    # 多層遮罩互相互斥來讓數字顯現出來
    lower_color = (170, 95, 0)
    upper_color = (180, 120, 100)
    hsv1 = cv2.inRange(hsv, lower_color, upper_color)
    if imgshow_flag == 1:
        cv2.imshow('hsv1', hsv1)
        cv2.waitKey(0)

    lower_color = (160, 120, 70)
    upper_color = (180, 205, 110)
    hsv2 = cv2.inRange(hsv, lower_color, upper_color)
    if imgshow_flag == 1:
        cv2.imshow('hsv2', hsv2)
        cv2.waitKey(0)

    lower_color = (0, 0, 0)
    upper_color = (180, 255, 20)
    hsv3 = cv2.inRange(hsv, lower_color, upper_color)
    if imgshow_flag == 1:
        cv2.imshow('hsv3', hsv3)
        cv2.waitKey(0)

    hsv = cv2.blur(hsv, (3, 3))
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    if imgshow_flag == 1:
        cv2.imshow('hsv', hsv)
        cv2.waitKey(0)
    hsv = cv2.equalizeHist(hsv)
    if imgshow_flag == 1:
        cv2.imshow('hsv', hsv)
        cv2.waitKey(0)

    

    hsv = cv2.threshold(hsv, 100, 255, 0)
    if imgshow_flag == 1:
        cv2.imshow('hsv', hsv[1])
        cv2.waitKey(0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.blur(img, (5, 5))
    img = cv2.threshold(img, 40, 255, 1) # (55 70)
    if imgshow_flag == 1:
        cv2.imshow('img', img[1])
        cv2.waitKey(0)

    # 0 = black, 255 = white

    for i in range(img[1].shape[0]):
        for j in range(img[1].shape[1]):
            x = 0
            y = 0
            if img[1][i][j] == 255:
                x = 1
            if hsv[1][i][j] == 255:
                y = 1
            x = (not x) | (not y)
            if x == 1:
                img[1][i][j] = 0
    for i in range(img[1].shape[0]):
        for j in range(img[1].shape[1]):
            x = 0
            y = 0
            if img[1][i][j] == 255:
                x = 1
            if hsv1[i][j] == 255:
                y = 1
            x = x | y
            if x == 1:
                img[1][i][j] = 255

    for i in range(img[1].shape[0]):
        for j in range(img[1].shape[1]):
            x = 0
            y = 0
            if img[1][i][j] == 255:
                x = 1
            if hsv2[i][j] == 255:
                y = 1
            x = x | y
            if x == 1:
                img[1][i][j] = 255
    for i in range(img[1].shape[0]):
        for j in range(img[1].shape[1]):
            x = 0
            y = 0
            if img[1][i][j] == 255:
                x = 1
            if hsv3[i][j] == 255:
                y = 1
            x = x | y
            if x == 1:
                img[1][i][j] = 255
    return img[1]

def reflection_remove_copy(img):
    # cv2.imshow('img', img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # print(hsv[0][0])
    
    cv2.imshow('hsv', hsv)
    cv2.waitKey(0)
    # 多層遮罩互相互斥來讓數字顯現出來
    lower_color = (170, 100, 0)
    upper_color = (180, 120, 100)
    hsv1 = cv2.inRange(hsv, lower_color, upper_color)
    cv2.imshow('hsv1', hsv1)
    cv2.waitKey(0)

    hsv = cv2.blur(hsv, (3, 3))
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    cv2.imshow('hsv', hsv)
    cv2.waitKey(0)
    hsv = cv2.equalizeHist(hsv)
    cv2.imshow('hsv', hsv)
    cv2.waitKey(0)

    

    hsv = cv2.threshold(hsv, 110, 255, 0)
    cv2.imshow('hsv', hsv[1])
    cv2.waitKey(0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.blur(img, (5, 5))
    img = cv2.threshold(img, 40, 255, 1) # (55 70)
    cv2.imshow('img', img[1])
    cv2.waitKey(0)

    # 0 = black, 255 = white

    for i in range(img[1].shape[0]):
        for j in range(img[1].shape[1]):
            x = 0
            y = 0
            if img[1][i][j] == 255:
                x = 1
            if hsv[1][i][j] == 255:
                y = 1
            x = x | y
            if x == 1:
                img[1][i][j] = 255

    return img[1]

def _sort(data):
    for k in range(0, 3):
        for l in range(0, 3):
            if data[1][k] < data[1][l]:
                tmp = data[1][k]
                data[1][k] = data[1][l]
                data[1][l] = tmp

                tmp = data[0][k]
                data[0][k] = data[0][l]
                data[0][l] = tmp
    return data
def box_rotate(img): # 回傳angle
    theta_list = [[], [], [], [], [], [], [], [], [], []]
    contours, _ = cv2.findContours(img, 2, 2)
    for cnt in contours:
        width, height = cv2.minAreaRect(cnt)[1]
        if width* height > 600 : # 15000
        # if height > 60 or width > 60:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            if 0 not in box.ravel():

                # for i in range(4):
                #     cv2.line(img, tuple(box[i]), tuple(box[(i+1)%4]), 0)

                slope = np.abs((box[3][1] - box[2][1]) / (box[3][0] - box[2][0] + 1e-5))
                theta = np.arctan(slope) * 180 / np.pi
                if theta % 10 < 5:
                    idx = theta // 10
                elif theta % 10 >= 5:
                    idx = theta // 10 + 1
                idx = int(idx)
                theta_list[idx].append(theta)

    # cv2.imshow('box', img)
    # cv2.waitKey(0)
    # 四捨五入 10進位來分類 最多的分類 加總平均

    if imgshow_flag == 1:
        print(theta_list)
    

    try :
        larger_num = -1
        larger_idx = -1
        for count in enumerate(theta_list):
            if larger_num < len(count[1]):
                larger_num = len(count[1])
                larger_idx = count[0]
        if imgshow_flag == 1:
            print('larger_idx : ', larger_idx)
        
        total_theta = 0
        for theta_in_count in theta_list[larger_idx]:
            total_theta += theta_in_count
        total_theta /= larger_num
        if total_theta <= 50:  # +90
            # print('<= 50--------------------')
            # print('Box_rotate_angle : ', total_theta)
            total_theta = 90 - total_theta
            # print('Box_rotate_angle : ', total_theta)
            return total_theta, 1
        else: 
            # print('Box_rotate_angle : ', total_theta)
            return total_theta, 0
    except :
        if imgshow_flag == 1:
            print('here')
        total_theta = 90
        # print('Box_rotate_angle : ', total_theta)
        return total_theta, -1

def houghlinesp_rotate(img):


    # =============================================================================================================================
    
    lines = cv2.HoughLinesP(img, 1, np.pi / 180, 105, minLineLength=10, maxLineGap=150) # 傳回很多個兩點座標 用於連線 **需調參數**
    # lines = cv2.HoughLinesP(img, 1, np.pi / 180, 500, minLineLength=500, maxLineGap=150) # 傳回很多個兩點座標 用於連線 **需調參數**
    # https://medium.com/@bob800530/hough-transform-cf6cb8337eac  原理
    # https://blog.csdn.net/ftimes/article/details/106816736   cv2.HoughLinesP參數解釋
    # https://cloud.tencent.com/developer/article/1942907 
    
    # =============================================================================================================================

    
    
    angle_list = [[], [], [], [], [], [], [], [], [], []]
    for line in lines:
        x1, y1, x2, y2 = line[0]
        tmplen = ((y2-y1)**2 + (x2-x1)**2)**0.5
        tmpslope = np.abs((y1-y2) / (x1-x2+1e-5))
        # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3) #在圖上畫線
        # print(tmpslope, ' ', tmplen)
        angle = np.arctan(tmpslope)*180/np.pi
        if int(angle) % 10 < 5:
            angle_list[int(angle) // 10].append(angle)
        elif int(angle) % 10 >= 5:
            angle_list[int(angle) // 10 + 1].append(angle)
        
        larger_idx = -1
        larger_num = -1
        total_theta = 0
        for count in enumerate(angle_list):
            if larger_num < len(count[1]):
                larger_num = len(count[1])
                larger_idx = count[0]

        for theta_in_count in angle_list[larger_idx]:
            total_theta += theta_in_count
        total_theta /= larger_num
        
    # cv2.imshow('box', img)
    # cv2.waitKey(0)
    
    
    # print('Houghlinesp_rotate_angle : ', total_theta)

    return total_theta

def rotate_img(img):
    new_angle = 0
    new_angle1, staus = box_rotate(img) 
    new_angle2 = houghlinesp_rotate(img)

    new_angle = new_angle1 * 0.5 + new_angle2 * 0.5
    print('Final_angle : ', new_angle)

    h, w = img.shape
    center = (h//2, h//2)
    M = cv2.getRotationMatrix2D(center, -new_angle, 0.8)
    rotated = cv2.warpAffine(img, M, (h, h),flags=cv2.INTER_CUBIC, borderValue = (255, 255, 255))
    # cv2.imshow('img', rotated)
    # cv2.waitKey(0)
    return new_angle, staus

import ctypes
lib = ctypes.CDLL('./speedup_performance.so') # gcc -shared -fPIC speedup_performance.c -o speedup_performance.so
lib.mix_rotate_calculate.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))
lib.mix_rotate_calculate.restype = ctypes.POINTER(ctypes.c_int)

def mix_rotate(img):
    pre_angle, status = rotate_img(img)
    angle = 0
    
    h, w = img.shape
    center = (h//2, h//2)
    pre_avg = 0
    pre_plate_len = 0

    big_range_angle = 90
    little_range_angle = 0

    iter = 0
    while iter < 10: # 根據翻轉後的plate的總長和黑點分布來繼續下一次的迭代
        angle = (big_range_angle + little_range_angle) // 2 
        M = cv2.getRotationMatrix2D(center, -angle, 0.8) # 旋轉
        rotated = cv2.warpAffine(img, M, (h, h),flags=cv2.INTER_CUBIC, borderValue = (255, 255, 255))
        
        h, w = rotated.shape[:2]

        rotated_arr = (ctypes.POINTER(ctypes.c_int) * len(rotated))()
        for i, row in enumerate(rotated):
            rotated_arr[i] = (ctypes.c_int * len(row))(*row)
        
        avg = 0
        res = lib.mix_rotate_calculate(h, w, rotated_arr)
        plate_len = res[0]
        avg = res[1]
        # 用avg 和 plate_len來做二元搜尋要旋轉的角度
        if big_range_angle - little_range_angle < 3:
            # cv2.imwrite('./test_cut_img2/test%d.jpg' % img_num, rotated)
            break
        if avg >= pre_avg and plate_len >= pre_plate_len: 
            little_range_angle = angle
        elif avg < pre_avg or plate_len < pre_plate_len:
            big_range_angle = angle
        
        pre_avg = avg # 紀錄這次得出的avg給下次迭代用
        pre_plate_len = plate_len # 紀錄這次得出的plate_len給下次迭代用
        iter += 1

    # 藉由調整權重來的出最後的angle
    final_angle = 0
    if angle >= pre_angle and pre_angle <= 50:
        final_angle = angle * 0.4 + pre_angle * 1.25
    elif angle >= pre_angle and (angle == 89 or angle == 88 or angle == 90) and status != 1:
        final_angle = angle * 0.35 + pre_angle * 0.55
    elif angle >= pre_angle and (angle == 89 or angle == 88 or angle == 90) and status == 1:
        final_angle = angle * 0.35 + pre_angle * 0.85
    elif angle >= pre_angle:
        final_angle = angle * 0.65 + pre_angle * 0.35
    elif angle <= pre_angle:
        final_angle = angle * 0.35 + pre_angle * 0.65 # 0.65
    
    if final_angle > 89:
        final_angle = 89
    # print('pre_angle : ', pre_angle)
    # print('angle : ', angle)
    # print('final_ angle : ', final_angle)

    M = cv2.getRotationMatrix2D(center, -final_angle, 0.8) # 旋轉
    img = cv2.warpAffine(img, M, (h, h),flags=cv2.INTER_CUBIC, borderValue = (255, 255, 255))

    return img

def boxbox(img): # 用findcontour找輪廓再用minArearect框出字
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.erode(img, kernel)
    # cv2.imshow('contours', img)
    # cv2.waitKey(0)
    
    new = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))

    # # 拓寬照片加白框讓貼在照片邊緣的數字也能被框出來
    # new = np.zeros((img.shape[0] + 6, img.shape[1] + 6), dtype = np.uint8)
    # # cv2.imshow('new', new)
    # # cv2.waitKey(0)
    # for i in range(0, new.shape[0]):
    #     for j in range(0, new.shape[1]):
    #         # pass
    #         if i >= new.shape[0] - 3 or j >= new.shape[1] - 3:
    #             new[i][j] = 255
    #         elif i < 3 or j < 3:
    #             new[i][j] = 255
    #         else:
    #             new[i][j] = img[i-3][j-3]
    # ###########################################

    contours, _ = cv2.findContours(new, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        # 最小外界矩形的宽度和高度
        width, height = cv2.minAreaRect(cnt)[1]  #(中心,(寬,高),旋轉角度)
        # print('width*height = ', width* height)
        if height > 60 or width > 60 :
            # 最小的外接矩形
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
            box = np.int0(box)
            if 0 not in box.ravel():
                x_little = new.shape[1] # left
                x_big = 0 # right
                y_little = new.shape[0] # top
                y_big = 0 # bottom
                for i in range(4):
                    if x_little > box[i][0]:
                        x_little = box[i][0]
                    if x_big < box[i][0]:
                        x_big = box[i][0]
                    if y_little > box[i][1]:
                        y_little = box[i][1]
                    if y_big < box[i][1]:
                        y_big = box[i][1]  
                box[0][0] = x_little
                box[0][1] = y_little

                box[1][0] = x_big
                box[1][1] = y_little

                box[2][0] = x_big
                box[2][1] = y_big

                box[3][0] = x_little
                box[3][1] = y_big

                for i in range(4):
                    cv2.line(new, tuple(box[i]), tuple(box[(i+1)%4]), 0)  
                    # cv2.imshow('img1',  new)
                    # cv2.waitKey(0)
    return new
def pixel_distribution_cut(img):
    h, w = img.shape[:2]
    sum = np.zeros((h))
    for i in range(h):
        for j in range(w):
            if img[i][j] == 0: # 0 = black, 255 = white
                sum[i] += 1
    
    if imgshow_flag == 1:
        print(sum[:])

    ssum = 0
    total = 0
    for i in range(h):
        if sum[i] != 0:
            ssum += sum[i]
            total += 1
    ssum = ssum // total

    if imgshow_flag == 1:
        print(ssum)

    if imgshow_flag == 1:
        plt.bar(range(h),sum)
        plt.show()

    line_num = 1

    top_bound = -1
    under_bound = -1

    for i in range(h - 1): # 畫分割線
        if line_num == 1: # need to upgrade
            if sum[i] >= 0 and sum[i + 1] > ssum and i < h:
                # img = cv2.line(img, (0, i), (w, i), (0,0,255), 1)
                line_num += 1
                top_bound = i
        # elif line_num == 2:
        #     if sum[i] <= ssum and sum[i - 1] >= ssum and i < h:
        #         img = cv2.line(img, (0, i), (w, i), (0,0,255), 1)
        #         line_num += 1
        else :
            pass
    line_num = 1
    for i in range(h - 1, 0, -1): # 畫分割線
        # if line_num == 1:
        #     if sum[i] >= 0 and sum[i + 1] > ssum and i < h:
        #         img = cv2.line(img, (0, i), (w, i), (0,0,255), 1)
        #         line_num += 1
        if line_num == 1: # need to upgrade
            if sum[i] <= ssum and sum[i - 1] >= ssum and i < h:
                # img = cv2.line(img, (0, i), (w, i), (0,0,255), 1)
                line_num += 1
                under_bound = i
        else :
            pass
    
# ##################################################################################
    h, w = img.shape[:2]
    sum_w = np.zeros((w))
    for i in range(top_bound, under_bound, 1):
        for j in range(w):
            if img[i][j] == 0: # 0 = black, 255 = white
                sum_w[j] += 1
    
    if imgshow_flag == 1:
        print(sum_w[:])

    ssum = 0
    # for i in range(w):
    #     if sum_w[i] != 0:
    #         if sum_w[i] % 10 > 4:
    #             sum_w[i] = (sum_w[i] // 10 + 1) * 10
    #         elif sum_w[i] % 10 <= 4:
    #             sum_w[i] = (sum_w[i] // 10) * 10
    #         ssum += sum_w[i]
    #         total += 1
    ssum = ssum // total

    if imgshow_flag == 1:
        print(ssum)
    plt.bar(range(w),sum_w)
    plt.show()

    # for i in range(w - 1): # 畫分割線
    #         if sum_w[i] >= 0 and sum_w[i] < ssum and sum_w[i + 1] > ssum and i < h: # need to upgrade
    #                 img = cv2.line(img, (i, top_bound), (i, under_bound), (0,0,255), 1)

    line_num = 1
    previous_line_idx = 0
    the_big = 0
    idx_list = []
    for i in range(w):
        if sum_w[the_big] < sum_w[i]:
            the_big = i
    print('the_big : ', the_big)
    print('ssum : ', ssum * 2)

    print('w', w)
    for i in range(w - 1): # 畫分割線 list
        if sum_w[i] >= 0 and sum_w[i] < ssum * 2 + 10  and sum_w[i + 1] > ssum + 5 and i < h: # need to upgrade
            if line_num == 1:
                # img = cv2.line(img, (i, top_bound), (i, under_bound), (0,0,255), 1)
                idx_list.append(i)
                # print(i)
                previous_line_idx = i
                line_num += 1   
            elif line_num > 1:
                the_little = the_big # 這個區間的最小值
                for j in range(previous_line_idx + 1, i, 1):
                    if sum_w[the_little] > sum_w[j]:
                        the_little = j

                print('the_little : ', the_little)
                print('previous : ', previous_line_idx)
                print('diff : ', the_little - previous_line_idx)
                if the_little - previous_line_idx <= 0:#20  // 5 * 3: # need to upgrade
                    pass
                else:
                    # img = cv2.line(img, (the_little, top_bound), (the_little, under_bound), (0,0,255), 1)
                    idx_list.append(the_little)
                    # print(the_little)
                    print('line ======= here ', the_little, previous_line_idx)
                    previous_line_idx = i
                    # i = the_little
                    line_num += 1   
    cut_list = []
    for line in enumerate(idx_list): # 畫分界線
        if line[0] == 0:
            img = cv2.line(img, (line[1], 0), (line[1], h), (0,0,255), 1)
            cut_list.append(line[1])
            previous_line_idx = line[1]
        elif line[0] != 0 and line[1] - previous_line_idx > 0:#90 // 5 * 3: # need to upgrade
            img = cv2.line(img, (line[1], 0), (line[1], h), (0,0,255), 1)
            cut_list.append(line[1])
            previous_line_idx = line[1]
        else:
            pass
    return img
def cut_the_num(img):
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # img = cv2.erode(img, kernel)
    # cv2.imshow('contours', img)
    # cv2.waitKey(0)

    new = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value = (255, 255, 255))
    
    # # 拓寬照片加白框讓貼在照片邊緣的數字也能被框出來
    # new = np.zeros((img.shape[0] + 6, img.shape[1] + 6), dtype = np.uint8)
    # # cv2.imshow('new', new)
    # # cv2.waitKey(0)
    # for i in range(0, new.shape[0]):
    #     for j in range(0, new.shape[1]):
    #         # pass
    #         if i >= new.shape[0] - 3 or j >= new.shape[1] - 3:
    #             new[i][j] = 255
    #         elif i < 3 or j < 3:
    #             new[i][j] = 255
    #         else:
    #             new[i][j] = img[i-3][j-3]
    # # cv2.imshow('new', new)
    # ###########################################

    contours, _ = cv2.findContours(new, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    

    img_list = []
    for cnt in contours:
        # 最小外界矩形的宽度和高度
        width, height = cv2.minAreaRect(cnt)[1]  #(中心,(寬,高),旋轉角度)
        # print('width*height = ', width* height)
        if height > 45 or width > 45 :     #(以r2158.JPG 的號碼大小>9000)
            # 最小的外接矩形
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
            box = np.int0(box)
            if 0 not in box.ravel():
                x_little = new.shape[1] # left
                x_big = 0 # right
                y_little = new.shape[0] # top
                y_big = 0 # bottom
                for i in range(4):
                    # print('box[%d] = ' % i, end = '')
                    # print(box[i])
                    # print('box[%d] = ' % ((i+1)%4), end = '')
                    # print(box[(i+1)%4])
                    if x_little > box[i][0]:
                        x_little = box[i][0]
                    if x_big < box[i][0]:
                        x_big = box[i][0]
                    if y_little > box[i][1]:
                        y_little = box[i][1]
                    if y_big < box[i][1]:
                        y_big = box[i][1]  
                # print(x_little)
                # print(y_little)
                # print(x_big)
                # print(y_big)
                box[0][0] = x_little
                box[0][1] = y_little
                # print(box[0])
                box[1][0] = x_big
                box[1][1] = y_little
                # print(box[1])
                box[2][0] = x_big
                box[2][1] = y_big
                # print(box[2])
                box[3][0] = x_little
                box[3][1] = y_big
                # print(type(new))
                # (height, width)
                # print('======================')
                # print(box[3])
                new_img = new[y_little:y_big, x_little:x_big]
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                new_img = cv2.erode(new_img, kernel)
                img_data = [new_img, x_little]
                # cv2.imshow('cut', new_img)
                # cv2.waitKey(0)
                img_list.append(img_data)
                # for i in range(4):
                #     cv2.line(new, tuple(box[i]), tuple(box[(i+1)%4]), 0)  
                    # cv2.imshow('img1',  new)
                    # cv2.waitKey(0)
    return img_list

if __name__ == '__main__':
    img = cv2.imread('exp11/frame_16.jpg')
    cv2.imshow('img', img)
    cv2.waitKey(0)

    img = reflection_remove(img)
    
    # img = rotate_img(img)
    cv2.imshow('img', img)
    cv2.waitKey(0)