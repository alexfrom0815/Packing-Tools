import os
import sys

import numpy as np

sys.path.append('../../')
from environment.physics0.Interface import Interface
import pybullet as p
import torch
import transforms3d
import time
import pyquaternion



bin_dimension = [0.8, 0.8, 0.30]
root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'apc' # apc ycb rss
# datatype = 'ycb' # apc ycb rss
# datatype = 'rss' # apc ycb rss

source_path = os.path.join(root, '5_{}_vhacd'.format(datatype))
pose_path   = os.path.join(root, '4_{}_min_area'.format(datatype))
target_path = os.path.join(root, '6_{}_stable'.format(datatype))
# source_path = '/home/hang/Documents/GitHub/IRBPP/data/datas/BoxMeshLargeArea_vhacd'
# source_path = '/home/hang/Documents/GitHub/IRBPP/data/datas/256'
# source_path = '/home/hang/Documents/GitHub/IRBPP/data/datas/256_vhacd'
# source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/2_apc_filt_8'
# source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_apc_scale'
# source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_apc_exp'
source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/6_apc_mesh_with_pose'

objPath = os.path.join(root, source_path)
interface = Interface(bin=bin_dimension, foldername=objPath, visual=True, scale=[1, 1, 1])

if not os.path.exists(target_path):
    os.makedirs(target_path)

for obj in os.listdir(objPath):
    obj = obj[0:-4]
    print(obj)
    obj = 'kong_air_dog_squeakair_tennis_ball_0'
    validT = []

    # posePath = os.path.join(pose_path, obj + '.pt')
    # transforms = torch.load(posePath)
    # for T in transforms:
        # quat = transforms3d.quaternions.mat2quat(T[0:3, 0:3])
        # quat = [quat[1], quat[2], quat[3], quat[0]]  # Saved in xyzw
    if True:
        id = interface.addObject(obj,
                                 targetFLB = [0.4,0.4,0],
                                 # rotation = quat,
                                 linearDamping = 0.5,
                                 angularDamping = 0.5)

        _, vertices = p.getMeshData(id)
        vertices = np.array(vertices)

        aabbBefore = interface.get_wraped_AABB(id)
        _, orienBefore, positionBefore = interface.get_Wraped_Position_And_Orientation(id, getPosBase = True)

        succeeded, valid = interface.simulateToQuasistatic(linearTol=0.01, angularTol=0.01, maxBatch=10)
        aabbAfter = p.getAABB(id)
        if aabbAfter[0][2] < -0.01:
            print(aabbAfter)
        _, orienAfter,  positionAfter = interface.get_Wraped_Position_And_Orientation(id,  getPosBase = True)

        interface.removeBody(id)

        q1 = pyquaternion.Quaternion([orienBefore[3], *orienBefore[0:3]])  # wxyz
        q2 = pyquaternion.Quaternion([orienAfter[3], *orienAfter[0:3]])
        r_diff = pyquaternion.Quaternion.absolute_distance(q1, q2)

        t_diff = np.linalg.norm(np.array(positionBefore) - np.array(positionAfter))

        if r_diff > 0.1 or t_diff > 0.05:
            continue
        # validT.append(T)
    # if len(validT) != 0:
    #     torch.save(validT, os.path.join(target_path, obj + '.pt'))


