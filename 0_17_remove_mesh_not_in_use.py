import os
import torch

# record = '../../data/final_data/IR_mix_mass/dicPathHalf.pt'
# record = torch.load(record)

record = os.listdir('/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/9_abc_good_mass_mesh_with_pose')

recordList = set()

for v in record:
    recordList.add(v[0:-6])
recordList = list(recordList)
print(recordList)
print(len(recordList))
# target = '../../picture/BlenderToolbox/meshes/packing/apc_origin'
# target = '../../picture/BlenderToolbox/meshes/packing/ycb_origin'
target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/10_abc_good_vhacd_with_pose'

for item in os.listdir(target):
    print(item)
    # if item[0:-6] not in recordList:
    if item[0:-6] not in record:
        path = os.path.join(target, item)
        print(path)
        os.remove(path)