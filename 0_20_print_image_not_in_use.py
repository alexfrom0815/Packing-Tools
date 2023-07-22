import os
import torch
from shutil import copyfile, copytree

record = []
record.append('../../data/final_data/IR_mix_mass/dicPathHalf.pt')
record.append('../../data/final_data/IR_concaveArea2_mass/dicPath.pt')

recordList = []
for r in record:
    r = torch.load(r)

    for v in r.values():
        if '/' in v:
            v = v.split('/')[-1]
        recordList.append(v[0:-4])
print(recordList)
allTypes = ['apc_mass', 'ycb_no_vhacd',  'concaveArea']
for datatype in allTypes:
    rootPath = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/images/singleMesh_inUse'
    sourceF  = '{}'.format(datatype)

    sourceF = os.path.join(rootPath, sourceF)

    for subFile in os.listdir(sourceF):
        if subFile[0:-6] not in recordList:
            os.remove(os.path.join(sourceF, subFile))
            print(subFile)

