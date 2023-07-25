import os
import trimesh

# Remove the meshes that are not watertight after reconstruction.
source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_ycb_good'

for f in os.listdir(source):
    print(f)
    mesh = trimesh.load_mesh(os.path.join(source,f))
    if not mesh.is_watertight:
        os.remove(os.path.join(source, f))

