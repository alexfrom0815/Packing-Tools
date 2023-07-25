import pybullet


import pybullet as p
import pybullet_data as pd
import os
import trimesh
p.connect(p.DIRECT)

# VHACD should be the last step

datatype = 'apc' # apc ycb rss
datatype = 'ycb' # apc ycb rss
datatype = 'rss' # apc ycb rss

# datatype = 'shapeNet' # apc ycb rss
# datatype = 'modelNet' # apc ycb rss

datatype = 'abc_good' # apc ycb rss

# sourceF  = '2_{}_filt_8'.format(datatype)
sourceF = '0_{}_scale'.format(datatype)
targetF  = '5_{}_vhacd'.format(datatype)

rootPath = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

sourceF = os.path.join(rootPath, sourceF)
targetF = os.path.join(rootPath, targetF)

if not os.path.exists(os.path.join(targetF)):
    os.makedirs(targetF)

for f in os.listdir(sourceF):
    name_in = os.path.join(sourceF, f)
    triIn = trimesh.load(name_in)

    f = f.replace('.off', '.obj')
    name_out = os.path.join(targetF, f)
    triIn.apply_translation(-triIn.center_mass)
    triIn.export(name_out)

    name_log = os.path.join(targetF, "")

    p.vhacd(name_out, name_out, '')
    # triOut = trimesh.load(name_out)
    # triIn.apply_scale(triIn.scale / triOut.scale )
    # triIn.apply_translation(-triIn.center_mass)
    # triIn.export(name_out)
    # 
    # p.vhacd(name_out, name_out, '')
    # triIn = trimesh.load(name_in)
    # triOut = trimesh.load(name_out)
    # print('scale', triIn.scale / triOut.scale)

