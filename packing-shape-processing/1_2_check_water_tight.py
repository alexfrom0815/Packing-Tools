import os
import trimesh

# Check if all the meshes are watertight.

source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_ycb_off'
for f in os.listdir(source):
    print(f)
    mesh = trimesh.load_mesh(os.path.join(source,f))
    print(mesh.is_watertight)

