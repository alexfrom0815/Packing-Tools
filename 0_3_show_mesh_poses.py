import transforms3d.euler
import trimesh
import torch
import os
import numpy as np

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss
# source_path = os.path.join(root, '5_{}_vhacd'.format(datatype))
source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_concave_scale'
pose_path   = os.path.join(root, '4_{}_min_area'.format(datatype))



board = trimesh.primitives.Box(extents = [1,2,0.1])
board.apply_translation([0,0,-0.05])
print(board.bounds)

# dirs = os.listdir(source_path)
# for PlyPath in dirs:
#     print(PlyPath)
#     objPath = os.path.join(source_path,PlyPath)
if True:
    objPath = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/ycb_no_vhacd/006_mustard_bottle_2.obj'

    # posePath = os.path.join(pose_path, PlyPath[0:-4] + '.pt')
    # transforms = torch.load(posePath)
    # for p in transforms:

    if True:
        mesh = trimesh.load(objPath)
        # mesh.apply_transform(p)
        # if PlyPath[0:8] == 'modelNet':
        #     mesh.apply_transform(extendMat(transforms3d.euler.euler2mat(0,-np.pi/2,0)))
        # else:
        #     mesh.apply_transform(extendMat(transforms3d.euler.euler2mat(np.pi/2,0,0)))

        mesh.apply_translation(-mesh.bounds[0])
        print(mesh.bounds)
        scene = trimesh.Scene([board, mesh])
        scene.show()