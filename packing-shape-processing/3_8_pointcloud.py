import time

import numpy as np
import os
import trimesh
import torch

datatype = 'ycb' # apc ycb rss


targetF  = '8_{}_pointCloud_with_pose'.format(datatype)
sourceF  = '10_{}_vhacd_with_pose'.format(datatype)
# sourceF  = '14_{}_vhacd_with_pose'.format(datatype)
# targetF  = '11_{}_pointCloud_with_pose'.format(datatype)

# sourceF  = 'tetris3D_tolerance_middle_nomin_mass_vhacd'.format(datatype)
# targetF  = 'tetris3D_tolerance_middle_nomin_mass_vhacd_pointcloud'.format(datatype)
rootPath = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'
# rootPath = '../nomin'

sourceF = os.path.join(rootPath, sourceF)
targetF = os.path.join(rootPath, targetF)

sourceF = '../final_data/BoxMeshRebuttal/vhacd_with_pose'
targetF = '../final_data/BoxMeshRebuttal/pointCloud_with_pose'

if not os.path.exists(os.path.join(targetF)):
    os.makedirs(targetF)


pointcloud_size = 100000
for f in os.listdir(sourceF):

    name_in = os.path.join(sourceF, f)
    mesh = trimesh.load(name_in)  #
    # mesh.apply_translation(-mesh.center_mass)
    mesh.apply_translation(-mesh.bounds[0])
    s = time.time()
    points, face_idx = mesh.sample(pointcloud_size, return_index=True)
    e = time.time()
    print(e-s)
    filename = os.path.join(targetF, f[0:-4])
    np.savez(filename, points=points)
