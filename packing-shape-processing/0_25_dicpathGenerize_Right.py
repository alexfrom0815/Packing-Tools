import os.path

import torch
import math
import numpy as np

source = '../final_data/IR_mix_mass/dicPathHalf.pt'
target = '../final_data/IR_mix_mass/'

# source = '../final_data/tetris3D_tolerance_middle_mass/dicPath.pt'
# target = '../final_data/tetris3D_tolerance_middle_mass/'

left = 1

dictRecord = torch.load(source)

inverseDict = {}
for k in dictRecord.keys():
    if dictRecord[k][0:-6] not in inverseDict.keys():
        inverseDict[dictRecord[k][0:-6]] = [k]
    else:
        inverseDict[dictRecord[k][0:-6]].append(k)

length = len(inverseDict)
leftLength = math.ceil(length * left)
print(leftLength)

# newDict = {}
# keyCounter = 0
# valuecounter = 0
# for k in inverseDict.keys():
#     keyCounter += 1
#     if keyCounter < leftLength:
#         value = inverseDict[k]
#         for idx in value:
#             newDict[valuecounter] = dictRecord[idx]
#             valuecounter += 1
# print(newDict)
# print(len(newDict))
# torch.save(newDict, os.path.join(target, 'dicPathPart_{}.pt'.format(left)))
#
# # assert False
# source = '../final_data/IR_concaveArea3_mass/dicPath.pt'
# target = '../final_data/IR_concaveArea3_mass/dicPathGen.pt'
#
# dictRecord = torch.load(source)
#
# newDictObject = []
# newDictBoard = []
# newDictConcave = []
#
# for v in dictRecord.values():
#     if v[0] == 'c':
#         newDictConcave.append(v)
#     elif v[0] == 'b':
#         newDictBoard.append(v)
#     else:
#         assert v[0] == 'o'
#         newDictObject.append(v)
#
# allDicts = [newDictObject, newDictBoard, newDictConcave]
# newDict = []
#
# for originDict in allDicts:
#     length = len(originDict)
#     leftLength = math.ceil(length * 0.8)
#
#     for newIdx in range(leftLength):
#         originIndex = np.random.choice(originDict)
#         newDict.append(originIndex)
#         originDict.remove(originIndex)
#
# finalDict = {}
# for idx in range(len(newDict)):
#     finalDict[idx] = newDict[idx]
# # print(finalDict)
# torch.save(finalDict, target)