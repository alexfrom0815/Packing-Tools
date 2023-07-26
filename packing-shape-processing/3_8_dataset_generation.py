import os
import torch
import numpy as np
import trimesh

bin_dimension = [0.32,0.32,0.3]
bin_scale = np.linalg.norm(bin_dimension)

subName = 'ycb'
baseDir = './final_data/{}/vhacd_with_pose'.format(subName)

id2shape = {}
counter = 0
for item in os.listdir(baseDir):
    print(item)
    mesh = trimesh.load_mesh(os.path.join(baseDir,item))
    id2shape[counter] = item
    counter += 1

if not os.path.exists('./dataset/{}/id2shape.pt'.format(subName)):
    torch.save(id2shape,'./dataset/{}/id2shape.pt'.format(subName))
else:
    id2shape = torch.load('./dataset/{}/id2shape.pt'.format(subName))

inverseDict = {}
for k in id2shape.keys():
    if id2shape[k][0:-6] not in inverseDict.keys():
        inverseDict[id2shape[k][0:-6]] = [k]
    else:
        inverseDict[id2shape[k][0:-6]].append(k)
print(inverseDict)
print(len(inverseDict.keys()))

allTrajs = []
for i in range(10000):
    print(i)
    traj = []
    for j in range(100):
        name = np.random.choice(list(inverseDict.keys()))
        traj.append(np.random.choice(inverseDict[name]))
    allTrajs.append(traj.copy())
torch.save(allTrajs, './dataset/{}/test_sequence.pt'.format(subName))