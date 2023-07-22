import os
import trimesh
import numpy as np
import transforms3d
from shutil import copyfile

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'
percentage = 0.6

datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss

source_path = '0_{}_scale'.format(datatype)

# process_path = '7_{}_vhacd_with_pose'.format(datatype)
# target_path = '9_{}_vhacd_with_pose_filt'.format(datatype) # nice counter 209

process_path = '8_{}_pointCloud_with_pose'.format(datatype)
target_path = '9_{}_pointCloud_with_pose_filt'.format(datatype) # nice counter 209

target_path = target_path + '_{}'.format(int(percentage * 10))

bin_dimension = [0.32, 0.32, 0.30]
bin_dimension = np.array(bin_dimension)
counter = 0

process_path = os.path.join(root, process_path)
source_path = os.path.join(root, source_path)
target_path = os.path.join(root, target_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

valid = []
for f in os.listdir(source_path):
    mesh = trimesh.load_mesh(os.path.join(source_path, f))
    transforms, probs = mesh.compute_stable_poses()
    mesh.apply_transform(transforms[0])

    extents = mesh.extents
    if np.max(extents - bin_dimension * 0.6) > 0:
        print(extents)
        print(f)
    else:
        valid.append(f.split('.')[0])
        # copyfile(os.path.join(source_path, f),  os.path.join(target_path, f))

    # if np.max(extents - bin_dimension / 2) < 0 and np.min(extents - bin_dimension / 10) > 0:
    #     counter+=1

for f in os.listdir(process_path):
    if f[0:-6] in valid:
        copyfile(os.path.join(process_path, f),  os.path.join(target_path, f))

