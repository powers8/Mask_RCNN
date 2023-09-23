from ast import If
from PIL import Image
import os
import glob
import json
import base64
import math

# 数据集路径
path = "D:\mask\Mask_RCNN\crop\small_images"
# 生成数据的保存路径
save_path = "D:\mask\Mask_RCNN\crop\small_images"
# 当前数据集图片格式
file_format = ".png"
# 替换格式jpg -> json
replace_format = ".json"
# 左右翻转文件名附加字符
LR = "lr_"
# 上下翻转文件名附加字符
TB = "tb_"

# 转angel度文件名附加字符
R90 = "r90_"
# 转180度文件名附加字符
R180 = "r180_"
# 转270度文件名附加字符
R270 = "r270_"

# 获取数据集目录的图片数据集
img_list = glob.glob(os.path.join(path, "*.png"))
# print(img_list)


# print("左右翻转-start")
# # 1.遍历图片
# for i in range(len(img_list)):
#     # 图片路径
#     img_path = img_list[i]
#     # print(img_path)
#     # 对应json路径
#     json_path = img_list[i].replace(file_format, replace_format)
#     # print(json_path)
#     # exit()
#     # 判断json文件是否存在
#     is_exists = os.path.exists(json_path)
#     if is_exists:
#         # 打开json文件
#         f = open(json_path, encoding='utf-8')
#         # 读取json
#         setting = json.load(f)
#         # 获取当前图片尺寸
#         width = setting['imageWidth']
#         height = setting['imageHeight']
#         # 获取中轴
#         mid_width = width / 2
#         mid_height = height / 2
#
#         print("中轴：x-" + str(mid_width) + ",y-" + str(mid_height))
#         # 2.遍历shapes
#         for i2 in range(len(setting['shapes'])):
#             # 3.遍历每个shapes的点
#             for i3 in range(len(setting['shapes'][i2]['points'])):
#                 temp_x = setting['shapes'][i2]['points'][i3][0]
#                 temp_y = setting['shapes'][i2]['points'][i3][1]
#                 if temp_x > mid_width:
#                     dis = temp_x - mid_width
#                     new_x = mid_width - dis
#                 elif temp_x < mid_width:
#                     dis = mid_width - temp_x
#                     new_x = mid_width + dis
#                 else:
#                     new_x = temp_x
#                 new_y = temp_y
#                 setting['shapes'][i2]['points'][i3][0] = new_x
#                 setting['shapes'][i2]['points'][i3][1] = new_y
#         # 从json获取文件名
#         file_name = setting['imagePath']
#         head, tail = os.path.split(file_name)
#         # print(file_name, '\t', head, '\t', tail)
#         # 修改json文件名
#         setting['imagePath'] = os.path.join("..\lr_img", LR + tail)
#         # str = setting['imagePath']
#         img_save_path = os.path.join("D:\mask\Mask_RCNN\crop\lr_img", LR + tail)
#         # print(img_save_path)
#         # exit()
#         json_save_path = img_save_path.replace(file_format, replace_format)
#         # print(json_save_path)
#         # exit()
#         # 图片转换
#         pri_image = Image.open(img_path)
#         # 左右镜面翻转FLIP_LEFT_RIGHT
#         pri_image.transpose(Image.FLIP_LEFT_RIGHT).save(img_save_path)
#         # 将转换后的图片进行base64加密
#         with open(img_save_path, 'rb') as f:
#             setting['imageData'] = base64.b64encode(f.read()).decode()
#         string = json.dumps(setting)
#         # 将修改后的json写入文件
#         with open(json_save_path, 'w', encoding='utf-8') as f:
#             f.write(string)
#             f.close()
#         print(img_path + "-------转换完成")
#         setting = None
#     else:
#         print(json_path + "-------文件不存在")
# print("左右翻转-end")

# # 原理同上
# print("上下翻转-start")
# for i in range(len(img_list)):
#     img_path = img_list[i]
#     json_path = img_list[i].replace(file_format, replace_format)
#     is_exists = os.path.exists(json_path)
#     if is_exists:
#         f = open(json_path, encoding='utf-8')
#         setting = json.load(f)
#         width = setting['imageWidth']
#         height = setting['imageHeight']
#         mid_width = width / 2
#         mid_height = height / 2
#
#         for i2 in range(len(setting['shapes'])):
#             for i3 in range(len(setting['shapes'][i2]['points'])):
#                 temp_x = setting['shapes'][i2]['points'][i3][0]
#                 temp_y = setting['shapes'][i2]['points'][i3][1]
#                 if temp_y > mid_height:
#                     dis = temp_y - mid_height
#                     new_y = mid_height - dis
#                 elif temp_y < mid_height:
#                     dis = mid_height - temp_y
#                     new_y = mid_height + dis
#                 else:
#                     new_y = temp_y
#                 new_x = temp_x
#                 setting['shapes'][i2]['points'][i3][0] = new_x
#                 setting['shapes'][i2]['points'][i3][1] = new_y
#
#         file_name = setting['imagePath']
#         head, tail = os.path.split(file_name)
#         setting['imagePath'] = os.path.join("..\tb_img", TB + tail)
#         img_save_path = os.path.join(r"D:\mask\Mask_RCNN\crop\tb_img", TB + tail)
#         print(img_save_path)
#         json_save_path = img_save_path.replace(file_format, replace_format)
#         pri_image = Image.open(img_path)
#         # 上下镜面翻转FLIP_TOP_BOTTOM
#         pri_image.transpose(Image.FLIP_TOP_BOTTOM).save(img_save_path)
#         with open(img_save_path, 'rb') as f:
#             setting['imageData'] = base64.b64encode(f.read()).decode()
#         string = json.dumps(setting)
#         with open(json_save_path, 'w', encoding='utf-8') as f:
#             f.write(string)
#             f.close()
#         print(img_path + "-------转换完成")
#         setting = None
#     else:
#         print(json_path + "-------文件不存在")
# print("上下翻转-end")


def rolationer(path, save_path, file_format, replace_format, descritions, angel):
    print("反时针旋转%s度-start" % angel)
    # 1.遍历图片
    for i in range(len(img_list)):
        # 图片路径
        img_path = img_list[i]
        # 对应json路径
        json_path = img_list[i].replace(file_format, replace_format)
        # 判断json文件是否存在
        is_exists = os.path.exists(json_path)
        if is_exists:
            # 打开json文件
            f = open(json_path, encoding='utf-8')
            # 读取json
            setting = json.load(f)
            # 获取当前图片尺寸
            width = setting['imageWidth']
            height = setting['imageHeight']
            # 获取中轴
            mid_width = width / 2
            mid_height = height / 2

            print("中轴：x-" + str(mid_width) + ",y-" + str(mid_height))
            # 2.遍历shapes
            for i2 in range(len(setting['shapes'])):
                # 3.遍历每个shapes的点
                for i3 in range(len(setting['shapes'][i2]['points'])):
                    temp_x = setting['shapes'][i2]['points'][i3][0]
                    temp_y = setting['shapes'][i2]['points'][i3][1]

                    new_x = (temp_x - mid_width) * math.cos(math.radians(angel)) - (temp_y - mid_height) * math.sin(
                        math.radians(angel)) + mid_width
                    new_y = (temp_x - mid_width) * math.sin(math.radians(angel)) + (temp_y - mid_height) * math.cos(
                        math.radians(angel)) + mid_height

                    setting['shapes'][i2]['points'][i3][0] = new_x
                    setting['shapes'][i2]['points'][i3][1] = new_y
            # 从json获取文件名
            file_name = setting['imagePath']
            # 修改json文件名
            # setting['imagePath'] = descritions + file_name
            head, tail = os.path.split(file_name)
            # print(file_name,"************", head, "*****************", tail)
            setting['imagePath'] = os.path.join("..\\"+descritions+"img", descritions + tail)
            s = setting['imagePath']
            # print(s)

            img_save_path = os.path.join("D:\mask\Mask_RCNN\crop\\" + descritions + "img", descritions + tail)
            json_save_path = img_save_path.replace(file_format, replace_format)
            # print(img_save_path, json_save_path)
            # exit()
            # 图片转换
            pri_image = Image.open(img_path)
            # 左右镜面翻转FLIP_LEFT_RIGHT,反时针旋转angel度 Image.ROTATE_90,反时针旋转180 Image.ROTATE_180 反时针旋转270度 Image.ROTATE_270
            if angel == 90:

                pri_image.transpose(Image.ROTATE_270).save(img_save_path)
            elif angel == 180:
                pri_image.transpose(Image.ROTATE_180).save(img_save_path)
            elif angel == 270:
                pri_image.transpose(Image.ROTATE_90).save(img_save_path)
            else:
                print('输入正确的角度！')
                return
            # 将转换后的图片进行base64加密
            with open(img_save_path, 'rb') as f:
                setting['imageData'] = base64.b64encode(f.read()).decode()
            string = json.dumps(setting)
            # 将修改后的json写入文件
            with open(json_save_path, 'w', encoding='utf-8') as f:
                f.write(string)
                f.close()
            print(img_path + "-------转换完成")
            setting = None
        else:
            print(json_path + "-------文件不存在")
    print("反时针旋转%s度-end" % angel)


rolationer(path, save_path, file_format, replace_format, R90, 90)
rolationer(path, save_path, file_format, replace_format, R180, 180)
rolationer(path, save_path, file_format, replace_format, R270, 270)
