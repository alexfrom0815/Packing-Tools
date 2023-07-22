import os
import trimesh
import numpy as np

# apply scale to modelNet/shapeNet data
correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_concave_scale'
target_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_concaveArea_scale'

if not os.path.exists(target_path):
    os.makedirs(target_path)

bin_dimension = [0.32,0.32,0.3]
bin_scale = np.linalg.norm(bin_dimension)

for f in os.listdir(correct_path):
    co_mesh = trimesh.load_mesh(os.path.join(correct_path, f))
    scale = np.min(bin_dimension[0:2]) / np.max(co_mesh.extents[0:2]) * 0.5
    co_mesh.apply_scale(scale)
    co_mesh.apply_translation(-co_mesh.bounds[0])
    # co_mesh.export(os.path.join(target_path, f))
    print(scale)
    # print(co_mesh.scale)
    # print(co_mesh.extents)
    # print(np.linalg.norm(co_mesh.extents))
    # print(np.linalg.norm(bin_dimension))
