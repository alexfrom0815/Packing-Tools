import os
from shutil import copyfile
import trimesh

# 下一步, 整理文件

# # YCB SORT
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/YCB_dataset/YCB_data'
# target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/YCB_dataset/YCB_obj'
#
# for f in os.listdir(source):
#     filePath = os.path.join(source, f, 'google_16k', 'textured.obj')
#     if os.path.exists(filePath):
#         copyfile(filePath,  os.path.join(target, f + '.obj'))

# modelNetSort
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_modelNet_off'
# target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_modelNet_off'
# if not os.path.exists(target):
#     os.makedirs(target)
#
# data = 'modelNet'
# for cate in os.listdir(source):
#     for t_v in os.listdir(os.path.join(source, cate)):
#         for item in os.listdir(os.path.join(source, cate, t_v)):
#             itemPath = os.path.join(source, cate, t_v, item)
#             copyfile(itemPath,  os.path.join(target, data + '_' + item))

# shapeNetSort
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_shapeNet_off'
# target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_shapeNet_off'

source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_abc_obj'
target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_abc_off'

if not os.path.exists(target):
    os.makedirs(target)

data = 'shapeNet'
# for cate in os.listdir(source):
#     for dirs in os.listdir(os.path.join(source, cate)):
#         print(dirs)
#         itemPath = os.path.join(source, cate, dirs, 'models', 'model_normalized.obj')
#         mesh = trimesh.load(itemPath)
#         mesh.export(os.path.join(target, data + '_' + cate + '_' + dirs + '.obj'))

for item in os.listdir(source):
    itemPath = os.path.join(source, item)
    mesh = trimesh.load(itemPath)
    mesh.export(os.path.join(target, item.replace('.obj', '.off')))