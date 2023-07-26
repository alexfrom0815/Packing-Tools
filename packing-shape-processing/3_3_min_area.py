import torch
import trimesh
import os
import numpy as np
import transforms3d

# Rotate the mesh to the poses with the minimum area.

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4


root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'ycb' # apc ycb rss

source_path = os.path.join(root, '0_{}_scale'.format(datatype))
pose_path   = os.path.join(root, '3_{}_stable_poses'.format(datatype))
target_path = os.path.join(root, '4_{}_min_area'.format(datatype))

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

        grain = 360 * 4
        areaList = np.ones((grain)) * 1e10

        rotList = []
        # meshList = []
        for angleIdx in range(grain):
            rotMesh = stableMesh.copy()
            Tz = extendMat(transforms3d.euler.euler2mat(0, 0, angleIdx * np.pi * 2 / grain, 'sxyz'))
            rotMesh.apply_transform(Tz)
            areaList[angleIdx] = rotMesh.extents[0] * rotMesh.extents[1]
            rotList.append(Tz)
            # rotMesh.apply_translation([0,0,0.05 * angleIdx])
            # meshList.append(rotMesh)
        bestAngle = int(np.argmin(areaList))
        bestRot = rotList[bestAngle]

        rotMesh = stableMesh.copy()
        rotMesh.apply_transform(bestRot)
        rotMesh.apply_translation(-rotMesh.bounds[0])


        finalTransform = np.dot(bestRot, transforms[tranIdx])
        minTransforms.append(finalTransform)

    torch.save(minTransforms, os.path.join(target_path, PlyPath[0:-4] + '.pt'))


