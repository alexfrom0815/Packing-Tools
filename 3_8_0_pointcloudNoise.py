import time

import numpy as np
import os
import trimesh
import torch




# root = '../final_data/tetris3D_tolerance_middle_mass/'
# root = '../final_data/IR_mix_mass/'
root = '../final_data/IR_concaveArea3_mass/'


# root = '../final_data/IR_concaveArea3_nomin/'
# root = '../final_data/IR_mix_nomin/'

# sourceF  = root + 'vhacd_with_pose/board'
# sourceF  = root + 'vhacd_with_pose/concave'
sourceF  = root + 'vhacd_with_pose/objects'
# sourceF = '../final_data/IR_mix_nomin/vhacd_with_pose'

# rootPath = '../nomin'

# sourceF = os.path.join(rootPath, sourceF)
# sourceF = os.path.join(sourceF)
# sourceF = os.path.join(root, 'vhacd_with_pose')
points_sigma = 0.1
pointcloud_size = 100000

# targetF  = root + 'pointCloud_with_pose_{}'.format(int(points_sigma * 100))
# targetF  = root + 'pointCloud_with_pose_{}/board'.format(int(points_sigma * 100))
# targetF  = root + 'pointCloud_with_pose_{}/concave'.format(int(points_sigma * 100))
targetF  = root + 'pointCloud_with_pose_{}/objects'.format(int(points_sigma * 100))

# targetF  = root + 'pointCloud_with_pose/board'
# targetF  = root + 'pointCloud_with_pose/concave'
# targetF  = root + 'pointCloud_with_pose/objects'

# targetF = os.path.join(targetF)

# targetF = '../final_data/IR_mix_nomin/pointCloud_with_pose'


if not os.path.exists(os.path.join(targetF)):
    os.makedirs(targetF)


for f in os.listdir(sourceF):

    name_in = os.path.join(sourceF, f)
    mesh = trimesh.load(name_in)  #
    # mesh.apply_translation(-mesh.center_mass)
    mesh.apply_translation(-mesh.bounds[0])
    s = time.time()
    points, face_idx = mesh.sample(pointcloud_size, return_index=True)

    points += points_sigma * mesh.scale * np.random.randn(pointcloud_size, 3)

    e = time.time()
    print(e-s)
    filename = os.path.join(targetF, f[0:-4])
    np.savez(filename, points=points)
    print(filename)
# parser.add_argument('--points_sigma', type=float, default=0.01,
#                     help='Standard deviation of gaussian noise added to points'
#                          'samples on the surfaces.')
