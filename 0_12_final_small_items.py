import os
import numpy as np
import trimesh
from shutil import copyfile

root = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_mix_mass'
meshPath = 'vhacd_with_pose'
pointCloud = 'pointCloud_with_pose'

# target = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_concaveArea3_mass/vhacd_with_pose/objects'
target = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_concaveArea3_mass/pointCloud_with_pose/objects'

# concave area  0.05
# concave area1 0.08
# concave area2 0.04 - 0.08

if not os.path.exists(target):
    os.makedirs(target)

# 说找小item, 不一定要把找的范围也说出来啊
for item in os.listdir(os.path.join(root, meshPath)):
    mesh = trimesh.load(os.path.join(root, meshPath, item))
    if 'cup' in item:
        continue
    if np.max(mesh.extents) < 0.12 :
        if np.min(mesh.extents) > 0.06:

            print(mesh.extents)
            print('large', item)

            # copyfile(os.path.join(root, meshPath, item), os.path.join(target, item))

            item = item[0:-4] + '.npz'
            copyfile(os.path.join(root, pointCloud, item), os.path.join(target, item))