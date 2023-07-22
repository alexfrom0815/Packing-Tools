import trimesh
import os
import pymeshlab

root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss

source_path = '2_{}_filt_8'.format(datatype)
target_path = '2_{}_exp'.format(datatype)

source_path = os.path.join(root, source_path)
target_path = os.path.join(root, target_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

ms = pymeshlab.MeshSet()
for f in os.listdir(source_path):
    f = f[0:-4]
    mesh = trimesh.load(os.path.join(source_path, f + '.obj'))
    print('before',len(mesh.faces), len(mesh.vertices))

    ms.load_new_mesh(os.path.join(source_path, f + '.obj'))
    ms.remove_duplicate_vertices()
    ms.remove_duplicate_faces()
    ms.save_current_mesh(os.path.join(target_path, f + '.obj'))

    mesh = trimesh.load(os.path.join(target_path, f + '.obj'))
    print('after',len(mesh.faces), len(mesh.vertices))
