import json
import os

img_path = r'D:\mask\Mask_RCNN\DATASET_PATH\coco2017\Images'
name_id = {}
for img_name in os.listdir(img_path):
    id = img_name.lstrip('0')
    id = id[:-4]
    id = int(id)
    name_id[id] = img_name

json_path = r'D:\mask\Mask_RCNN\DATASET_PATH\coco2017\instances_val2017.json'
json_content = json.load(open(json_path, 'r', encoding='utf-8'))
anns = json_content['annotations']
ann_ids = []
for ann in anns:
    img_id = ann['image_id']
    if img_id not in ann_ids:
        ann_ids.append(img_id)

print(len(name_id), len(ann_ids))
for id in ann_ids:
    name_id.pop(id)
print(len(name_id))
for id, name in name_id.items():
    os.remove(os.path.join(img_path, name))
