import os
import trimesh
import numpy as np

bin_dimension = [0.32,0.32,0.3]
bin_scale = np.linalg.norm(bin_dimension)
all_scale = []
half_scale = []
source = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_mix/vhacd_with_pose'
# source = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_apc_data/vhacd_with_pose'
source = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_apc_ycb/vhacd_with_pose'

for f in os.listdir(source):
    # print(f)
    mesh = trimesh.load_mesh(os.path.join(source,f))
    # print(mesh.scale / bin_scale)
    all_scale.append(mesh.scale / bin_scale)
    if mesh.scale / bin_scale < 0.5:
        half_scale.append(mesh.scale / bin_scale)
print(np.mean(all_scale))
print(np.percentile(all_scale, 90))
print(len(half_scale))
for i in range(10):
    print(np.percentile(all_scale, (i + 1) * 10))
