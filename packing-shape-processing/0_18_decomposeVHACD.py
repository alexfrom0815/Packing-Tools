import os
import trimesh
import numpy as np
import torch

allColor = []
boxBrown = np.array([0.6, 0.3, 0.1])
allColor.append(boxBrown)
# ICLR COLOR
allColor.append(np.array([215, 155, 0]) * 1.0 / 255) # deep brown
allColor.append(np.array([251, 232, 222]) * 1.0 / 255) # light brown
allColor.append(np.array([108, 141, 190]) * 1.0 / 255) # deep blue
allColor.append(np.array([220, 239, 255]) * 1.0 / 255) # light blue
allColor.append(np.array([84,  130, 53]) * 1.0 / 255) # deep green
allColor.append(np.array([217, 241, 221]) * 1.0 / 255) # light green
allColor.append(np.array([205, 158, 166]) * 1.0 / 255) # dark red
allColor.append(np.array([146, 206, 80]) * 1.0 / 255) # figure3 green
allColor.append(np.array([159, 199, 192]) * 1.0 / 255) # figure3 dark green
allColor.append(np.array([155, 194, 230]) * 1.0 / 255) # figure3 bule
allColor.append(np.array([197, 181, 239]) * 1.0 / 255) # figure3 green
allColor.append(np.array([255, 202, 204]) * 1.0 / 255) # figure3 pink
allColor.append(np.array([255, 123, 127]) * 1.0 / 255) # figure3 red
allColor.append(np.array([244, 175, 132]) * 1.0 / 255) # figure3 oringe
allColor.append(np.array([245, 244, 194]) * 1.0 / 255) # figure3 ricewhite
allColor.append(np.array([255, 217, 102]) * 1.0 / 255) # figure3 yellow
# qijin color
allColor.append(np.array([241, 175, 176]) * 1.0 / 255) # robot pink
allColor.append(np.array([183, 234, 150]) * 1.0 / 255) # robot green
allColor.append(np.array([234, 209, 110]) * 1.0 / 255) # robot yellow
allColor.append(np.array([134, 204, 203]) * 1.0 / 255) # robot cyan
allColor.append(np.array([109, 135, 212]) * 1.0 / 255) # robot blue
allColor.append(np.array([151, 131, 205]) * 1.0 / 255) # robot purple
allColor.append(np.array([222, 79,  79]) * 1.0 / 255) # robot red
allColor.append(np.array([146, 168, 215]) * 1.0 / 255) # robot dark blue
allColor.append(np.array([223, 174, 255]) * 1.0 / 255) # paper purple
allColor.append(np.array([255, 220, 151]) * 1.0 / 255) # paper yellow
allColor.append(np.array([153, 204, 255]) * 1.0 / 255) # paper light blue
allColor.append(np.array([96,  108, 245]) * 1.0 / 255) # paper deep blue
allColor.append(np.array([220, 89,  80]) * 1.0 / 255) # paper red

record = []
record.append('../../data/final_data/IR_mix_mass/dicPathHalf.pt')
record.append('../../data/final_data/IR_concaveArea2_mass/dicPath.pt')

recordList = []
for r in record:
    r = torch.load(r)

    for v in r.values():
        recordList.append(v[0:-4])

allTypes = ['apc', 'ycb', 'rss', 'concaveArea']

for datatype in allTypes:
    rootPath = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'
    sourceF  = '11_{}_decomposed_mesh_parts'.format(datatype)
    vhacdF  = '10_{}_vhacd_with_pose'.format(datatype)

    sourceF = os.path.join(rootPath, sourceF)
    vhacdF = os.path.join(rootPath, vhacdF)

    for subDir in os.listdir(sourceF):
        print(subDir in record)
        subPath = os.path.join(sourceF, subDir)
        pathLength = len(os.listdir(subPath))

        if pathLength <= 10 and pathLength >= 4:
            meshParts = []
            for partIdx, part in enumerate(os.listdir(subPath)):
                partPath = os.path.join(subPath, part)
                mesh = trimesh.load(partPath)
                mesh.visual.face_colors = allColor[partIdx] * 255
                meshParts.append(mesh)
            # scene = trimesh.scene.Scene(meshParts)
            # scene.show()