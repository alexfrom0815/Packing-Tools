
import os
import trimesh

# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_apc_good'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_abc_good'
source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/1_abc_downsample/2500'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_ycb_good'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_rss_good'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_modelNet_good'
for f in os.listdir(source):
    print(f)
    mesh = trimesh.load_mesh(os.path.join(source,f))
    if not mesh.is_watertight:
        os.remove(os.path.join(source, f))

