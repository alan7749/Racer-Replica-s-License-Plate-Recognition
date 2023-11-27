import subprocess
import os
os.environ['TF_CPP_MIN__LOG_LEVEL'] = '2'
import sys
import tensorflow as tf
from tensorflow import keras
from keras import layers, regularizers
from keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
from keras.datasets import mnist

# yolov7有截到重機車牌的frame 我們再把它以照片的方式存下來

# camera on ========
print('done camera_on')
# ==================

# # delete the raw img directory
# if os.path.exists('D:/newpic2510'):
#     file_list = os.listdir('D:/newpic2510')
#     for file in file_list:
#         os.remove('D:/newpic2510/' + file)
# if os.path.exists('D:/newpic2510'):
#     os.rmdir('D:/newpic2510')
#     os.mkdir('D:/newpic2510')
# if not os.path.exists('D:/newpic2510'):
#     os.mkdir('D:/newpic2510')
# print('done delete the raw img directory')
# #===================

# # video2img ========
# p = subprocess.Popen("python video2img.py", shell=True, stdout=subprocess.PIPE, cwd = 'D:/video2pic/')
# print('done video2img')
# #===================

# delete the exp directory
if os.path.exists('D:/cmd_prac/yolov7_crop_tool/runs/detect/exp'):
    file_list = os.listdir('D:/cmd_prac/yolov7_crop_tool/runs/detect/exp')
    for file in file_list:
        os.remove('D:/cmd_prac/yolov7_crop_tool/runs/detect/exp/' + file)
if os.path.exists('D:/cmd_prac/yolov7_crop_tool/runs/detect/exp'):
    os.rmdir('D:/cmd_prac/yolov7_crop_tool/runs/detect/exp')
print('done delete the exp directory')
#===================

# yolov7 cut =======
# with subprocess.Popen("python detect.py --weights best4.pt --conf 0.5 --img-size 640 --source D:/1114/IMG_2003.MOV --device 0", shell=True, stdout=subprocess.PIPE, cwd = 'D:/YOLOv7_crop_tool/yolov7') as p:
#     print('done yolov7_crop')
with subprocess.Popen("python detect.py --weights best4.pt --conf 0.5 --img-size 640 --source D:/1114/IMG_2003.MOV --device 0", shell=True, stdout=subprocess.PIPE, cwd = 'D:/cmd_prac/yolov7_crop_tool/') as p:
    print('done yolov7_crop')
    # ~ 1988 2006
    # 1994 ~ 1996
    # 2001 ~ 2005

# with subprocess.Popen("python detect.py --weights best4.pt --conf 0.5 --img-size 640 --source D:/1113/IMG_1834.MOV --device 0", shell=True, stdout=subprocess.PIPE, cwd = 'D:/YOLOv7_crop_tool/yolov7') as p:
#     print('done yolov7_crop')

# with subprocess.Popen("python detect.py --weights best4.pt --conf 0.5 --img-size 640 --source D:/2910/IMG_1505.MOV --device 0", shell=True, stdout=subprocess.PIPE, cwd = 'D:/YOLOv7_crop_tool/yolov7') as p:
#     print('done yolov7_crop')
    # 2510 90
    # 2310 86
    # 2310 85(video prob)
    # 2410 80(useless video)
    # 2410 82(yolo prob)
    # 2410 83(num classify prob NEED REVISE!!)
    # 2910 94(num classify and TF dataset prob NEED REVISE!!)
    # 1509 (x)
    # 1507 (x)
    # 1504 (x)

#===================

# delete the upload/output directory

if os.path.exists("D:/cmd_prac/deblur_tool-NAFNet-/upload/output"):
    file_list = os.listdir("D:/cmd_prac/deblur_tool-NAFNet-/upload/output")
    for file in file_list:
        os.remove('D:/cmd_prac/deblur_tool-NAFNet-/upload/output/' + file)
if os.path.exists('D:/cmd_prac/deblur_tool-NAFNet-/upload/output'):
    os.rmdir('D:/cmd_prac/deblur_tool-NAFNet-/upload/output')
    os.mkdir('D:/cmd_prac/deblur_tool-NAFNet-/upload/output')
if not os.path.exists('D:/cmd_prac/deblur_tool-NAFNet-/upload/output'):
    os.mkdir('D:/cmd_prac/deblur_tool-NAFNet-/upload/output')
print('done delete the upload/output directory')
#===================

# deblur img =======
with subprocess.Popen("python deblur_model.py", shell=True, stdout=subprocess.PIPE, cwd = 'D:/cmd_prac/deblur_tool-NAFNet-/') as p:
    print('done deblur_img')
# ==================

# delete the ./rotated_img directory
if os.path.exists('./rotated_img'):
    file_list = os.listdir('./rotated_img')
    for file in file_list:
        os.remove('./rotated_img/' + file)
if os.path.exists('./rotated_img'):
    os.rmdir('./rotated_img')
    os.mkdir('./rotated_img/')
elif not os.path.exists('./rotated_img'):
    os.mkdir('./rotated_img/')
print('done delete the ./rotated_img directory')
#===================

# rotate img =======
with subprocess.Popen("python rotate_img.py", shell=True, stdout=subprocess.PIPE) as p:
    print('done rotate_img')
# ==================

# model predict ====
# tf_model = keras.models.load_model('1114_num_model')
# classify_model = keras.models.load_model('1105_num_classify_model')
# tf_model = keras.models.load_model('1119_num_model10')
# classify_model = keras.models.load_model('1119_num_classify_model4')
tf_model = keras.models.load_model('11201_num_model2') # ok
classify_model = keras.models.load_model('1122_num_classify_model2') # no ok
pre_file_num_0 = 0
pre_file_num_1 = -1
plate_list = []
num_list = []
if os.path.exists('./rotated_img'):
    file_list = os.listdir('./rotated_img')
    file_list.sort(key=lambda x:int(x.split('_')[2]))
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
    for file in file_list:
        re = -100
        re_idx = -1
        result_num = -1
        img = cv2.imread('rotated_img/%s' % file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.expand_dims(img, axis=0)
        result = tf_model.predict(img)
        # print('shape : ', result.shape)
        if(result[0][0] > result[0][1]): # T > F
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
        else :
            os.remove("./rotated_img/%s" % file)
            # os.rename('rotated_img/%s' % file, 'D:/1113/after 1113/%s' % file)
        print('done model_predict')
print('==============================')
# ==================

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
        # for item in max_idx_list:
            # print(plate_list[item])
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
# print(tree.tree)
for i in plate_list:
    tree.append(i)
# print(tree.tree)
result = []
for item in tree.tree:
    max_val = max(item, key=item.get)
    result.append(max_val)
print(result)

# statistic plate ==
# with subprocess.Popen("python statistic.py", shell=True, stdout=subprocess.PIPE) as p:
#     print('done statistic')
# ==================
# import sys
# sys.exit()
