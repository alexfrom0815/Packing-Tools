import trimesh
import numpy as np
import os

# dataCate = ['pointCloud_with_pose']
dataCate = ['vhacd_with_pose']
bco = ['board', 'concave', 'objects']
root = '/home/hang/Documents/GitHub/IRBPP/data/final_data'
# subname = 'IR_apc_mass'
subname = 'IR_mix_mass'
# subname = 'tetris3D_tolerance_large_mass'
# subname = 'tetris3D_tolerance_middle_mass'
# subname = 'IR_concaveArea2_mass'


for cate in dataCate:
    subPath = os.path.join(root, subname, cate)

    for file in os.listdir(subPath):
        filePath = os.path.join(subPath, file)
        print(filePath)
        if file.endswith('npz'):
            pcd = np.load(filePath)['points']
            print(np.min(pcd, axis=0))
            print(np.max(pcd, axis=0))
        elif file.endswith('obj'):
            mesh = trimesh.load(filePath)
            print(mesh.bounds[0])

    # for dirs in os.listdir(subPath):
    #     for subFile in os.listdir(os.path.join(subPath, dirs)):
    #         subFilePath = os.path.join(subPath, dirs, subFile)
    #         print(subFilePath)
    #         if subFilePath.endswith('npz'):
    #             pcd = np.load(subFilePath)['points']
    #             print(np.min(pcd, axis=0))
    #             print(np.max(pcd, axis=0))
    #         elif subFilePath.endswith('obj'):
    #             mesh = trimesh.load(subFilePath)
    #             print(mesh.bounds[0])