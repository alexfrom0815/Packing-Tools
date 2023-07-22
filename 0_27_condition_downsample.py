import os

import torch
import trimesh
import pymeshlab

ms = pymeshlab.MeshSet()

source = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/abc_origin_for_draw'
# source = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/abc_origin_for_draw_downsample_50000'
# source = '/home/dell/zhaohang/IRBPP/picture/BlenderToolbox/meshes/packing/abc_origin_for_draw_50000'
# target = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/abc_origin_for_draw_downsample_50000'
# target = '/home/dell/zhaohang/IRBPP/picture/BlenderToolbox/meshes/packing/abc_origin_for_draw_50000'

# paths = os.listdir(source)

paths = torch.load('/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_abc_good/dicPath.pt')
print(paths)
paths = list(paths.values())

triangleNum = 50000
largeMesh = []
drawMesh = []
for p in paths:
    PlyPath = os.path.join(source, p)

    originMesh = trimesh.load(PlyPath)
    # print('originMesh: is_convex {}, is_watertight {}, triangles number {}'.format(originMesh.is_convex, originMesh.is_watertight, len(originMesh.triangles)))
    if len(originMesh.vertices) >= triangleNum:
        largeMesh.append(p)
        # savepath = os.path.join(target,  p)
        # ms.load_new_mesh(PlyPath)
        # ms.simplification_quadric_edge_collapse_decimation(targetfacenum = triangleNum, preservenormal = True, preserveboundary = True, preservetopology = True)
        # ms.save_current_mesh(savepath)
        #
        # downMesh = trimesh.load(savepath)
        # print('downMesh: is_convex {}, is_watertight {}, triangles number {}'.format(downMesh.is_convex, downMesh.is_watertight, len(downMesh.triangles)))
    else:
        drawMesh.append(p)
        print(p, len(originMesh.vertices))
        print('originMesh: is_convex {}, is_watertight {}, triangles number {}'.format(originMesh.is_convex, originMesh.is_watertight, len(originMesh.triangles)))

# drawDict = {}
# for i in range(len(drawMesh)):
#     drawDict[i] = drawMesh[i]
# paths = torch.save(drawDict, '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_abc_good/dicDraw.pt')
