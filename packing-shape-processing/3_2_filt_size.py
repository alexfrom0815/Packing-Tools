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
percentage = 0.8
# source_path = '0_apc_scale'
# target_path = '2_apc_filt' # nice counter 8

# source_path = '0_ycb_scale'
# target_path = '2_ycb_filt' # nice counter 36

source_path = '0_rss_scale'
target_path = '2_rss_filt' # nice counter 209

target_path = target_path + '_{}'.format(int(percentage * 10))

bin_dimension = [0.32, 0.32, 0.30]
bin_dimension = np.array(bin_dimension)
counter = 0

source_path = os.path.join(root, source_path)
target_path = os.path.join(root, target_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

for f in os.listdir(source_path):
    mesh = trimesh.load_mesh(os.path.join(source_path, f))
    transforms, probs = mesh.compute_stable_poses()
    mesh.apply_transform(transforms[0])

    grain = 40
    areaList = np.ones((grain)) * 1e10
    meshList = []
    Tz = extendMat(transforms3d.euler.euler2mat(0, 0, np.pi * 2 / grain, 'sxyz'))
    for i in range(grain):
        if mesh.extents[0] <= mesh.extents[1]:  # x 方向要少
            if mesh.center_mass[1] <= mesh.centroid[1]: #
                areaList[i] = mesh.extents[0] * mesh.extents[1]
        meshList.append(mesh.copy())
        mesh.apply_transform(Tz)
    mesh = meshList[int(np.argmin(areaList))]


    extents = mesh.extents
    if np.max(extents - bin_dimension * 0.8) > 0:
        print(extents)
        print(f)
    else:
        copyfile(os.path.join(source_path, f),  os.path.join(target_path, f))

    if np.max(extents - bin_dimension / 2) < 0 and np.min(extents - bin_dimension / 10) > 0:
        counter+=1
print('nice counter', counter)