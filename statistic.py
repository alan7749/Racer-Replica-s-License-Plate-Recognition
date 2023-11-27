import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow import keras
from keras import layers, regularizers
from keras.preprocessing.image import ImageDataGenerator

file_list = os.listdir("./rotated_img")
file_list.sort(key=lambda x:int(x.split('_')[2]))
# print(file_list)
num_end = -1
num_base = -1
num_end_index = -1
num_base_index = -1
for index, file in enumerate(file_list):
    num0 = int(file.split('_')[2])
    if num_base is not num0:
        if num_base_index < num_end_index:
            tmp_list = file_list[num_base_index:num_end_index + 1]
            # print('before = ', tmp_list)
            tmp_list.sort(key=lambda x:int((x.split('.')[0]).split('_')[3]))
            file_list[num_base_index:num_end_index + 1] = tmp_list
            # print('after = ', file_list[num_base_index:num_end_index + 1])
            num_end_index = -1
            num_base_index = -1
            num_base = num0
            num_base_index = index
            
        elif  num_base_index >= num_end_index:
            num_base = num0
            num_base_index = index
        
    elif num_base == num0:
        num_end_index = index
# print(file_list)
# import sys
# sys.exit()
pre_file_num_0 = 0
pre_file_num_1 = -1
plate_list = []
num_list = []
# tf_model = keras.models.load_model('11201_num_model2')
# tf_model = keras.models.load_model('1105_num_model3')
classify_model = keras.models.load_model('1122_num_classify_model2')
pre_num_pixel = -1
for file in file_list:
    # print(file)
    img = cv2.imread('rotated_img/%s' % file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.expand_dims(img, axis=0)
    re = -100
    result_num = -1
    # result = tf_model.predict(img)  # big bug
    # if result[0][0] < result[0][1]: # false
    #     print(file)
    #     continue
    # else :
    result = classify_model.predict(img)
    for index, i in enumerate(result[0]):
        if i > re:
            re = i
            if index < 10:
                result_num = str(index)
            elif index == 10 :
                result_num = 'G'
            elif index == 11 :
                result_num = 'R'
            # elif index == 12 :
            #     result_num = 'G'
            # elif index == 13 :
            #     result_num = 'I'
            # elif index == 14 :
            #     result_num = 'R'
            # elif index == 15 :
            #     result_num = 'T'
            # elif index == 16 :
            #     result_num = 'Y'
    file = file.split(".")
    file_split = file[0].split("_")
    frame_num_0 = int(file_split[2]) # 哪張照片
    num_pixel = int(file_split[3]) # 哪個pixel
    if pre_file_num_0 is not frame_num_0: # 如果這回的frame跟上回的不一樣
        pre_num_pixel = -1
        # plate_list.append((num_list, pre_file_num_0))
        plate_list.append(num_list)
        pre_file_num_0 = frame_num_0
        num_list = []
        # num_list.append([result_num, num_pixel])
        num_list.append(result_num)
        pre_num_pixel = num_pixel
    else : # 跟上回的一樣
        if num_pixel - pre_num_pixel < 85: # 70要再改
            pre_num_pixel = num_pixel
            # num_list.append([result_num, num_pixel]) # 插入英文數字
            num_list.append(result_num) # 插入英文數字
        elif num_pixel - pre_num_pixel > 85: # 需要空一格的 # 70要再改
            pre_num_pixel = num_pixel
            # num_list.append('*') # 插入空格
            # num_list.append([result_num, num_pixel]) # 插入英文數字
            num_list.append(result_num) # 插入英文數字
    # pre_num_pixel
print(plate_list)

class replace_tree:
    def __init__(self, plate_list):
        self.plate_list = plate_list
        max_idx_list = []
        max_num = -1
        for index, num_list in enumerate(self.plate_list[0:len(self.plate_list)]):
            if max_num < len(num_list):
                max_idx_list = []
                max_num = len(num_list)
                max_idx_list.append(index)
            elif max_num == len(num_list):
                max_idx_list.append(index)
            else:
                pass
        self.tree = []
        self.count = []
        for item in max_idx_list:
            print(plate_list[item])
        for item in max_idx_list:
            self.append(plate_list[item])
            
    def append(self, num_list):
        if not self.tree:
            for num in num_list:
                self.tree.append({num:1})
        elif self.tree:
            unexisist_list = []
            flag = 0
            start = 0
            for num in num_list:
                for i in range(start, len(self.tree)):
                    if self.tree[i].get(num) != None and flag == 0:
                        # 將unexsist_list放到i前面
                        
                        # =======================================
                        for j in range(len(unexisist_list)):
                            if (i - 1 - j) < 0:
                                # insert到最前面
                                self.tree.insert(0, {unexisist_list.pop():1})
                                i += 1
                                # start += 1
                            elif (i - 1 - j) >= 0:
                                self.tree[i - 1 - j][unexisist_list.pop()] = 1
                        # =======================================

                        self.tree[i][num] = self.tree[i][num] + 1
                        start = i + 1
                        flag = 1
                        break
                    elif self.tree[i].get(num) != None and flag == 1:
                        self.tree[i][num] = self.tree[i][num] + 1
                        start = i + 1
                        flag = 1
                        break
                    elif self.tree[i].get(num) == None and flag == 1:
                        # 連續
                        self.tree[i][num] = 1
                        start = i + 1
                        break
                    elif self.tree[i].get(num) == None and flag == 0:
                        # 放到unexsist_list
                        if i == (len(self.tree) - 1):
                            unexisist_list.append(num)
                    else :
                        print('else')
tree = replace_tree(plate_list)
print(tree.tree)
for i in plate_list:
    tree.append(i)
print(tree.tree)

for item in tree.tree:
    max_val = max(item, key=item.get)
    print(max_val)