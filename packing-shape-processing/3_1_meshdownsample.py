import os
import trimesh
import pymeshlab

# skip for now

ms = pymeshlab.MeshSet()

root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/'

datatype = 'abc' # apc ycb rss
# datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss

source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_abc_obj'
target_path ='1_{}_downsample'.format(datatype)
target_path = os.path.join(root, target_path)

base_path = os.path.join(root,source_path)
paths = os.listdir(base_path)

# triangleNum = [256, 1000]
triangleNum = [2500]
# triangleNum = [20000]

for resolution in triangleNum:
    if not os.path.exists(os.path.join(target_path, str(resolution))):
        os.makedirs(os.path.join(target_path, str(resolution)))

for p in paths:
    PlyPath = os.path.join(base_path, p)
    # if '00010150_e16846f702644627a0063c10_trimesh_000' not in p:
    #     continue

    for resolution in triangleNum:

        savepath = os.path.join(target_path, str(resolution),  p)
        ms.load_new_mesh(PlyPath)
        # 这个函数的效果非常好 参数说明见 https://pymeshlab.readthedocs.io/en/0.2/filter_list.html
        ms.simplification_quadric_edge_collapse_decimation(targetfacenum = resolution, preservenormal = True, preserveboundary = True, preservetopology = True)
        ms.save_current_mesh(savepath)

        originMesh = trimesh.load(PlyPath)
        print('originMesh: is_convex {}, is_watertight {}, triangles number {}'.format(originMesh.is_convex, originMesh.is_watertight, len(originMesh.triangles)))

        downMesh = trimesh.load(savepath)
        print('downMesh: is_convex {}, is_watertight {}, triangles number {}'.format(downMesh.is_convex, downMesh.is_watertight, len(downMesh.triangles)))
