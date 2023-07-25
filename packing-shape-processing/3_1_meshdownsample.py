import os
import trimesh
import pymeshlab

# Downsample the meshes to specified triangle number since the original reconstructed meshes have too many triangles.

ms = pymeshlab.MeshSet()
root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/'
datatype = 'ycb' # apc ycb rss
source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_abc_obj'
target_path ='1_{}_downsample'.format(datatype)
target_path = os.path.join(root, target_path)

base_path = os.path.join(root,source_path)
paths = os.listdir(base_path)

triangleNum = [2500]

for resolution in triangleNum:
    if not os.path.exists(os.path.join(target_path, str(resolution))):
        os.makedirs(os.path.join(target_path, str(resolution)))

for p in paths:
    PlyPath = os.path.join(base_path, p)

    for resolution in triangleNum:

        savepath = os.path.join(target_path, str(resolution),  p)
        ms.load_new_mesh(PlyPath)
        ms.simplification_quadric_edge_collapse_decimation(targetfacenum = resolution, preservenormal = True, preserveboundary = True, preservetopology = True)
        ms.save_current_mesh(savepath)

        originMesh = trimesh.load(PlyPath)
        print('originMesh: is_convex {}, is_watertight {}, triangles number {}'.format(originMesh.is_convex, originMesh.is_watertight, len(originMesh.triangles)))

        downMesh = trimesh.load(savepath)
        print('downMesh: is_convex {}, is_watertight {}, triangles number {}'.format(downMesh.is_convex, downMesh.is_watertight, len(downMesh.triangles)))
