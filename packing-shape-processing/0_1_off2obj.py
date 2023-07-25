import trimesh
import os

# If the original data is in off format, use this script to convert it to obj format.

# Change the root path to your own path
root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'ycb' # apc ycb rss

source_path = '0_{}_scale'.format(datatype)
target_path = '0_{}_scale'.format(datatype)

source_path = os.path.join(root, source_path)
target_path = os.path.jo in(root, target_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

for f in os.listdir(source_path):
    f = f[0:-4]
    mesh = trimesh.load(os.path.join(source_path, f + '.off'))
    mesh.export(os.path.join(target_path, f + '.obj'))