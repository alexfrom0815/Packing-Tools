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

# datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss

datatype = 'abc' # apc ycb rss


source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_abc_obj'
target_path = os.path.join(root, '9_{}_mesh_pose_draw'.format(datatype))

if not os.path.exists(target_path):
    os.makedirs(target_path)

dirs = os.listdir(source_path)

board = trimesh.primitives.Box(extents = [1,1,0.001])
board.apply_translation([0,0,-0.0005])

for PlyPath in dirs:
    print(PlyPath)
    objPath = os.path.join(source_path,PlyPath)

    originMesh = trimesh.load(objPath)
    print(len(originMesh.vertices))

    # # transforms = torch.load(posePath)
    # transforms, _ = originMesh.compute_stable_poses()
    # transforms = transforms[0:3]
    # # probs = probs[0:10]
    #
    # minTransforms = []
    # for tranIdx in range(len(transforms)):
    #     stableMesh = originMesh.copy()
    #     stableMesh.apply_transform(transforms[tranIdx])
    #
    #     grain = 360 * 4
    #     areaList = np.ones((grain)) * 1e10
    #
    #     rotList = []
    #     # meshList = []
    #     for angleIdx in range(grain):
    #         rotMesh = stableMesh.copy()
    #         Tz = extendMat(transforms3d.euler.euler2mat(0, 0, angleIdx * np.pi * 2 / grain, 'sxyz'))
    #         rotMesh.apply_transform(Tz)
    #         areaList[angleIdx] = rotMesh.extents[0] * rotMesh.extents[1]
    #         rotList.append(Tz)
    #         # rotMesh.apply_translation([0,0,0.05 * angleIdx])
    #         # meshList.append(rotMesh)
    #     bestAngle = int(np.argmin(areaList))
    #     bestRot = rotList[bestAngle]
    #
    #     rotMesh = stableMesh.copy()
    #     rotMesh.apply_transform(bestRot)
    #     rotMesh.apply_translation(-rotMesh.bounds[0])
    #     # scene = trimesh.Scene([board, rotMesh])
    #     # # scene = trimesh.Scene([board, *meshList])
    #     # scene.show()
    #
    #     finalTransform = np.dot(bestRot, transforms[tranIdx])
    #     minTransforms.append(finalTransform)
    # for idx, T in enumerate(minTransforms):
    #     minMesh = originMesh.copy()
    #     minMesh.apply_transform(T)
    #     minMesh.apply_translation(-minMesh.bounds[0])
    #     minMesh.export( PlyPath[0:-4] +  '_{}.obj'.format(idx))
    # # torch.save(minTransforms, os.path.join(target_path, PlyPath[0:-4] + '.pt'))


