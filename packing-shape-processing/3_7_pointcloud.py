import time
import numpy as np
import os
import trimesh

datatype = 'ycb' # apc ycb rss


targetF  = '8_{}_pointCloud_with_pose'.format(datatype)
sourceF  = '10_{}_vhacd_with_pose'.format(datatype)
rootPath = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

sourceF = os.path.join(rootPath, sourceF)
targetF = os.path.join(rootPath, targetF)

if not os.path.exists(os.path.join(targetF)):
    os.makedirs(targetF)


pointcloud_size = 100000
for f in os.listdir(sourceF):

    name_in = os.path.join(sourceF, f)
    mesh = trimesh.load(name_in)  #
    mesh.apply_translation(-mesh.center_mass)
    s = time.time()
    points, face_idx = mesh.sample(pointcloud_size, return_index=True)
    e = time.time()
    print(e-s)
    filename = os.path.join(targetF, f[0:-4])
    np.savez(filename, points=points)
