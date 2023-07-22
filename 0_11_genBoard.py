import os.path

import numpy as np
import trimesh

bin_dimension = np.array([0.32,0.32,0.3])
target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_board_random_scale'
if not os.path.exists(target):
    os.makedirs(target)

tolerance = 0.001 # 感觉这个tolerance反而会引起问题，不应该是每个voxel都被缩小，而是应该整体减小一点， 这个很重要！

flat_low_bound = 0.12
flat_up_bound = 0.16
hight_low_bound = 0.02
hight_up_bound  = 0.04
for i in range(20):
    x = np.random.random() * (flat_up_bound - flat_low_bound) + flat_low_bound
    y = np.random.random() * (flat_up_bound - flat_low_bound) + flat_low_bound
    z = np.random.random() * (hight_up_bound - hight_low_bound) + hight_low_bound
    board = trimesh.primitives.Box(extents=[x, y, z])
    board.apply_translation(-board.center_mass)
    board.export(os.path.join(target, 'board_{}.obj'.format(i)))