import os
import trimesh
import numpy as np
# ref_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_apc_off'
# correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_apc_good'
# target_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_apc_scale'

# ref_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_ycb_off'
# correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_ycb_good'
# target_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_ycb_scale'
#
# if not os.path.exists(target_path):
#     os.makedirs(target_path)
#
# for f in os.listdir(correct_path):
#     co_mesh = trimesh.load_mesh(os.path.join(correct_path, f))
#     ref_mesh = trimesh.load_mesh(os.path.join(ref_path, f))
#     co_mesh.apply_scale(ref_mesh.scale / co_mesh.scale)
#     co_mesh.export(os.path.join(target_path, f))

# # apply scale to rss data
# # ref_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_ycb_off'
# correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_rss_good'
# target_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_rss_scale'
#
# if not os.path.exists(target_path):
#     os.makedirs(target_path)
#
# for f in os.listdir(correct_path):
#     co_mesh = trimesh.load_mesh(os.path.join(correct_path, f))
#     co_mesh.apply_scale(1 / 1000)
#     co_mesh.export(os.path.join(target_path, f))

# apply scale to modelNet/shapeNet data
# correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_shapeNet_good'
# target_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_shapeNet_scale'

# correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_abc_good'
correct_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_abc_obj'
target_path  = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_abc_draw'

if not os.path.exists(target_path):
    os.makedirs(target_path)

bin_dimension = [0.32,0.32,0.3]
bin_scale = np.linalg.norm(bin_dimension)

for f in os.listdir(correct_path):
    co_mesh = trimesh.load_mesh(os.path.join(correct_path, f))
    co_mesh.apply_scale(0.49 * bin_scale / co_mesh.scale * 0.8)
    co_mesh.export(os.path.join(target_path, f))
    print(co_mesh.scale)
    # print(co_mesh.extents)
    # print(np.linalg.norm(co_mesh.extents))
    # print(np.linalg.norm(bin_dimension))
    # co_mesh.apply_scale(1 / 1000)
    # co_mesh.export(os.path.join(target_path, f))