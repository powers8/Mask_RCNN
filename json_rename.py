from PIL import Image
import os
import glob
import json
import base64
import math

# 数据集路径
path = "D:\mask\Mask_RCNN\crop\small_images"
# 当前数据集图片格式
file_format = ".png"
# 替换格式jpg -> json
replace_format = ".json"

# 获取数据集目录的图片数据集
img_list = glob.glob(os.path.join(path, "*.png"))

for i in range(len(img_list)):
    # 图片路径
    img_path = img_list[i]
    # print(img_path)
    # 对应json路径
    json_path = img_list[i].replace(file_format, replace_format)
    # print(json_path)
    # exit()
    # 判断json文件是否存在
    is_exists = os.path.exists(json_path)
    if is_exists:
        # 打开json文件
        f = open(json_path, encoding='utf-8')
        # 读取json
        setting = json.load(f)

        # 从json获取文件名
        file_name = setting['imagePath']
        head, tail = os.path.split(file_name)
        print(file_name, '\t', head, '\t', tail)
        # 修改json文件名
        setting['imagePath'] = os.path.join("..\lr_img", "lr_" + tail)
        img_save_path = os.path.join("D:\mask\Mask_RCNN\crop\lr_img", "lr_" + tail)
        json_save_path = img_save_path.replace(file_format, replace_format)
        string = json.dumps(setting)
        # 将修改后的json写入文件
        with open(json_save_path, 'w', encoding='utf-8') as f:
            f.write(string)
            f.close()
        exit()
