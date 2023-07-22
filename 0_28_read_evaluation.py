import os
import torch
import trimesh
import pymeshlab
import numpy as np

source = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/abc_origin_for_draw'
data = '/home/hang/Documents/GitHub/IRBPP/logs/evaluation/IR_abc_good_500action_draw-2022.09.18-14-56-17/trajs.npy'

trajs = np.load(data, allow_pickle=True)

for traj in trajs:
    for item in traj:
        mesh = item[1]
        print(mesh)
        mesh = trimesh.load(os.path.join(source, mesh))
        # print(len(mesh.vertices))
        print(len(mesh.faces))