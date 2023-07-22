import os
from shutil import copyfile

source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_shapeNet_scale'
target = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_shapeNet_manual'

bown = 0
mug = 0
for item in os.listdir(source):
    itemOld = item
    # if 'shapeNet_bowl' in item:
    #     itemNew = item.replace('shapeNet_bowl', 'shapeNet_bowl_{}_'.format(bown))
    #     bown += 1
    if 'shapeNet_mug' in item:
        itemNew = item.replace('shapeNet_mug', 'shapeNet_mug_{}_'.format(mug))
        mug += 1
        copyfile(os.path.join(source, itemOld),  os.path.join(target, itemNew))
