import os

# 要重命名的文件夹路径
folder_path = "D:\Mask_RCNN\DATASET_PATH\Images"

# 获取文件夹中的所有文件名
files = os.listdir(folder_path)

counter = 1

# 遍历文件夹中的每个文件
for filename in files:
    # 原文件的完整路径
    old_file_path = os.path.join(folder_path, filename)
    formatted_counter = f"{counter:04d}"
    name, extension = os.path.splitext(filename)
    # 分解文件名，假设文件名格式为 "prefix_oldname_suffix"
    parts = filename.split("_")
    if len(parts) == 4:
        prefix, oldname, number1, number2 = parts

        # 修改要更改的部分（例如，在oldname后添加一些内容）
        newname = f"{prefix}_{formatted_counter}{extension}"

        # 新文件的完整路径
        new_file_path = os.path.join(folder_path, newname)

        # 使用os.rename()函数重命名文件
        os.rename(old_file_path, new_file_path)

        print(f"重命名文件: {filename} 为 {newname}")
    elif len(parts) == 3:
        prefix, number1, number2 = parts

        # 修改要更改的部分（例如，在oldname后添加一些内容）
        newname = f"{prefix}_{formatted_counter}{extension}"

        # 新文件的完整路径
        new_file_path = os.path.join(folder_path, newname)

        # 使用os.rename()函数重命名文件
        os.rename(old_file_path, new_file_path)

        print(f"重命名文件: {filename} 为 {newname}")

    counter += 1
