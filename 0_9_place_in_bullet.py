import os
import sys

import numpy as np

sys.path.append('../../')
from environment.physics0.Interface import Interface
import pybullet as p




bin_dimension = [0.8, 0.8, 0.30]

source_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_concave_scale'
objPath = source_path
interface = Interface(bin=bin_dimension, foldername=objPath, visual=True, scale=[1, 1, 1])


for obj in os.listdir(objPath):
    obj = obj[0:-4]
    validT = []
    print(obj)
    if True:
        id = interface.addObject(obj,
                                 targetFLB = [0.4,0.4,0],
                                 rotation=[0,np.pi/2,0],
                                 linearDamping = 0.5,
                                 angularDamping = 0.5)

        _, vertices = p.getMeshData(id)
        vertices = np.array(vertices)

        aabbBefore = interface.get_wraped_AABB(id)
        _, orienBefore, positionBefore = interface.get_Wraped_Position_And_Orientation(id, getPosBase = True)

        succeeded, valid = interface.simulateToQuasistatic(linearTol=0.01, angularTol=0.01, maxBatch=10)
        aabbAfter = p.getAABB(id)
        _, orienAfter,  positionAfter = interface.get_Wraped_Position_And_Orientation(id,  getPosBase = True)

        interface.removeBody(id)



