import pybullet

import time
import pybullet as p
import pybullet_data as pd
import os
import trimesh
p.connect(p.DIRECT)

# t = time.localtime()
# while True:
#     t = time.localtime()
#     if t.tm_hour > 2 and t.tm_hour < 3:
#         break
#     print(t.tm_hour)
#     time.sleep(10)


# VHACD should be the last step
# datatype = 'concave' # apc ycb rss

# datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss
# datatype = 'concaveArea' # apc ycb rss
datatype = 'abc_good' # apc ycb rss

# sourceF  = '6_{}_mesh_with_pose'.format(datatype)
# targetF  = '7_{}_vhacd_with_pose'.format(datatype)

sourceF  = '9_{}_mass_mesh_with_pose'.format(datatype)
# sourceF  = '13_{}_nomin_mesh_with_pose'.format(datatype)
targetF  = '10_{}_vhacd_with_pose'.format(datatype)
# targetF  = '14_{}_vhacd_with_pose'.format(datatype)

rootPath = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'
# rootPath = '../nomin'

sourceF = os.path.join(rootPath, sourceF)
targetF = os.path.join(rootPath, targetF)

if not os.path.exists(os.path.join(targetF)):
    os.makedirs(targetF)

for f in os.listdir(sourceF):
    name_in = os.path.join(sourceF, f)
    triIn = trimesh.load(name_in)

    f = f.replace('.off', '.obj')
    name_out = os.path.join(targetF, f)
    triIn.export(name_out)

    name_log = os.path.join(targetF, "")

    p.vhacd(name_out, name_out, '')
    triOut = trimesh.load(name_out)
    triIn.apply_scale(triIn.scale / triOut.scale )
    triIn.export(name_out)

    p.vhacd(name_out, name_out, '')
    triIn = trimesh.load(name_in)
    triOut = trimesh.load(name_out)
    print('scale', triIn.scale / triOut.scale)

