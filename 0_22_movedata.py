import torch
from shutil import copyfile, copytree
import os

source = '../final_data/IR_concaveArea3_mass/dicPath.pt'

dictRecord = torch.load(source)

newDictObject = []

for v in dictRecord.values():
    if v[0] == 'o':
        newDictObject.append(v)

for name in newDictObject:
    n = name.split('/')[-1][0:-4]
    # print(n)
    # copyfile(os.path.join('../final_data/IR_mix_nomin/vhacd_with_pose', n+'.obj'),
    #          os.path.join('../final_data/IR_concaveArea3_nomin/vhacd_with_pose/objects', n+'.obj'))
    # copyfile(os.path.join('../final_data/IR_mix_nomin/pointCloud_with_pose', n+'.npz'),
    #          os.path.join('../final_data/IR_concaveArea3_nomin/pointCloud_with_pose/objects', n+'.npz'))

    # sourceShape = os.path.join('/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/9_apc_mass_mesh_with_pose', n+'.obj')
    # sourceShape = os.path.join('/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/9_ycb_mass_mesh_with_pose', n+'.obj')
    sourceShape = os.path.join('/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/9_rss_mass_mesh_with_pose', n+'.obj')
    if os.path.exists(sourceShape):
        print(sourceShape)
        copyfile(sourceShape,
             os.path.join('/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/IR_concaveArea3/objects', n+'.obj'))
