import os
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

# 定义VOC标注和图像目录
voc_annotation_dir = 'D:\mask\Mask_RCNN\DATASET_PATH\VOC2012\Annotations'
voc_image_dir = 'D:\mask\Mask_RCNN\DATASET_PATH\VOC2012\JPEGImages'

# 初始化COCO格式的数据集字典
coco_dataset = {
    "images": [],
    "annotations": [],
    "categories": []
}

# 定义COCO类别（您可能需要根据您的VOC标签进行调整）
voc_categories = ['tvmonitor', 'train', 'sofa', 'sheep', 'pottedplant', 'person', 'motorbike', 'horse', 'dog', 'diningtable', 'cow', 'chair', 'cat', 'car', 'bus', 'bottle', 'bird', 'bicycle', 'boat', 'aeroplane']# 示例类别

# 将VOC类别映射到COCO类别
category_id_map = {voc_category: i + 1 for i, voc_category in enumerate(voc_categories)}


annid=0
# 加载VOC标注并创建COCO标注和图像
for filename in os.listdir(voc_annotation_dir):
    # 加载VOC标注文件（XML解析）
    # 提取图像和标注信息

    annotation_file = os.path.join(voc_annotation_dir, filename)
    tree = ET.parse(annotation_file)
    root = tree.getroot()

    # 提取图像ID、宽度、高度、边界框和类别ID的示例代码
    # image_id = '{:05}'.format(image_id_counter)  # 您需要用唯一的图像ID替换这个值
    # width = 640    # 示例宽度，请替换为实际宽度
    # height = 480   # 示例高度，请替换为实际高度
    # bbox = [100, 200, 300, 400]  # 示例边界框（xmin、ymin、xmax、ymax）
    # voc_category = '猫'  # 示例VOC类别
    image_id = filename.split('.')[0]
    # 提取图像宽度和高度
    size_element = root.find('size')
    width_element = size_element.find('width')
    height_element = size_element.find('height')
    width = int(width_element.text)
    height = int(height_element.text)

    # 提取边界框和类别信息，假设只处理一个边界框和类别
    object_element = root.find('object')
    bbox_element = object_element.find('bndbox')
    xmin = int(float(bbox_element.find('xmin').text))
    ymin = int(float(bbox_element.find('ymin').text))
    xmax = int(float(bbox_element.find('xmax').text))
    ymax = int(float(bbox_element.find('ymax').text))

    bbox = [xmin, ymin, xmax, ymax]  # 边界框信息

    # 提取VOC类别
    voc_category = object_element.find('name').text

    # 创建COCO格式的标注
    annotation = {
        "id": annid,  # 您需要用唯一的标注ID替换这个值
        "image_id": image_id,
        "category_id": category_id_map[voc_category],
        "bbox": bbox,
        "area": bbox[2] * bbox[3],
        "iscrowd": 0
    }
    annid+=1

    # 将标注添加到COCO标注列表中
    coco_dataset["annotations"].append(annotation)

    # 创建COCO格式的图像信息
    image_info = {
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": str(image_id+".jpg")  # 示例文件名，请替换为实际文件名
    }

    # 将图像信息添加到COCO图像列表中
    coco_dataset["images"].append(image_info)

# 添加COCO类别
for i, voc_category in enumerate(voc_categories):
    coco_category = {
        "id": i + 1,
        "name": voc_category,
        "supercategory": "物体"  # 示例超类，请替换为实际超类
    }
    coco_dataset["categories"].append(coco_category)

# 将COCO数据集保存到JSON文件中
with open('coco_dataset.json', 'w') as f:
    json.dump(coco_dataset, f)
