import os

import torch

dicPath = '/home/hang/Documents/GitHub/IRBPP/data/final_data/IR_mix/dicPathHalf.pt'
# dataPath = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/IR_mix_no_vhacd'
dataPath = '/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox/meshes/packing/ycb_no_vhacd'

dicPath = torch.load(dicPath)
validItems = list(dicPath.values())

for path in os.listdir(dataPath):
    if path not in validItems:
        itemPath = os.path.join(dataPath, path)
        os.remove(itemPath)