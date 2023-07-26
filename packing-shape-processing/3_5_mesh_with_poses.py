import torch
import trimesh
import os
import numpy as np
import transforms3d
import time

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'ycb' #

source_path  = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_abc_draw'

pose_path = os.path.join(root, '4_{}_min_area'.format(datatype))
target_path = os.path.join(root, '9_{}_for_draw'.format(datatype))

if not os.path.exists(target_path):
    os.makedirs(target_path)

dirs = os.listdir(source_path)

board = trimesh.primitives.Box(extents = [1,1,0.001])
board.apply_translation([0,0,-0.0005])

for PlyPath in dirs:
    print(PlyPath)
    objPath = os.path.join(source_path,PlyPath)
    posePath = os.path.join(pose_path, PlyPath[0:-4] + '.pt')
    if not os.path.exists(posePath):
        continue
    originMesh = trimesh.load(objPath)

    transforms = torch.load(posePath)
    minTransforms = []
    for tranIdx in range(len(transforms)):
        stableMesh = originMesh.copy()
        stableMesh.apply_transform(transforms[tranIdx])
        stableMesh.apply_translation(-stableMesh.center_mass)
        filename = os.path.join(target_path, PlyPath[0:-4] +  '_{}.obj'.format(tranIdx))
        stableMesh.export(filename)

