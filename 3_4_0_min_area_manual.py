import torch
import trimesh
import os
import numpy as np
import transforms3d

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

# 其实不用每个shape都做一个vhacd, 只要对主要的shape做vhacd就好了
# 3_3 和 3_4
# 3_4 其实可以挪到 3_6 后面去, 不过现在先不用折腾了, 冗余就冗余吧, 写文章的时候注意

root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'concave' # apc ycb rss
datatype = 'concaveArea' # apc ycb rss


source_path = os.path.join(root, '0_{}_scale'.format(datatype))
target_path = os.path.join(root, '4_{}_min_area'.format(datatype))

if not os.path.exists(target_path):
    os.makedirs(target_path)

dirs = os.listdir(source_path)


for PlyPath in dirs:
    print(PlyPath)
    objPath = os.path.join(source_path,PlyPath)
    originMesh = trimesh.load(objPath)

    minTransforms = []

    grain = 360 * 4
    areaList = np.ones((grain)) * 1e10

    rotList = []
    for angleIdx in range(grain):
        rotMesh = originMesh.copy()
        Tz = extendMat(transforms3d.euler.euler2mat(0, 0, angleIdx * np.pi * 2 / grain, 'sxyz'))
        rotMesh.apply_transform(Tz)
        areaList[angleIdx] = rotMesh.extents[0] * rotMesh.extents[1]
        rotList.append(Tz)

    bestAngle = int(np.argmin(areaList))
    bestRot = rotList[bestAngle]

    minTransforms.append(bestRot)

    torch.save(minTransforms, os.path.join(target_path, PlyPath[0:-4] + '.pt'))


