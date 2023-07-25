import os
import trimesh

# Turn the mesh files into off format for the next step (reconstruction)
source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_ycb_obj'
target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_ycb_off'

if not os.path.exists(target):
    os.makedirs(target)

for item in os.listdir(source):
    itemPath = os.path.join(source, item)
    mesh = trimesh.load(itemPath)
    mesh.export(os.path.join(target, item.replace('.obj', '.off')))