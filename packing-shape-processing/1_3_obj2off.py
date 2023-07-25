import os
from shutil import copyfile
import trimesh
# 下一步, 整理文件

# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_apc_obj'
# target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_apc_off'

source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/0_ycb_obj'
target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_ycb_off'
for f in os.listdir(source):
    print(f)
    mesh = trimesh.load_mesh(os.path.join(source,f))
    off = f.replace('.obj', '.off')
    # trimesh.primitives.Box()
    try:
        mesh.export(os.path.join(target, off))
    except ValueError as e:
        pass