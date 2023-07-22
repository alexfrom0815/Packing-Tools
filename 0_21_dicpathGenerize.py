import torch
import math
import numpy as np

# # source = '../final_data/IR_mix_mass/dicPathHalf.pt'
# # target = '../final_data/IR_mix_mass/dicPathGen.pt'
#
# source = '../final_data/tetris3D_tolerance_middle_mass/dicPath.pt'
# target = '../final_data/tetris3D_tolerance_middle_mass/dicPathGen.pt'
#
# dictRecord = torch.load(source)
# length = len(dictRecord)
# print(length)
# leftLength = math.ceil(length * 0.8)
# print(leftLength)
# newDict = {}
#
# for newIdx in range(leftLength):
#     originIndex = np.random.choice(list(dictRecord.keys()))
#     newDict[newIdx] = dictRecord[originIndex]
#     dictRecord.pop(originIndex)
# print(len(newDict))
# print(newDict)
#
# torch.save(newDict, target)

assert False

source = '../final_data/IR_concaveArea3_mass/dicPath.pt'
target = '../final_data/IR_concaveArea3_mass/dicPathGen.pt'

dictRecord = torch.load(source)

newDictObject = []
newDictBoard = []
newDictConcave = []

for v in dictRecord.values():
    if v[0] == 'c':
        newDictConcave.append(v)
    elif v[0] == 'b':
        newDictBoard.append(v)
    else:
        assert v[0] == 'o'
        newDictObject.append(v)

allDicts = [newDictObject, newDictBoard, newDictConcave]
newDict = []

for originDict in allDicts:
    length = len(originDict)
    leftLength = math.ceil(length * 0.8)

    for newIdx in range(leftLength):
        originIndex = np.random.choice(originDict)
        newDict.append(originIndex)
        originDict.remove(originIndex)

finalDict = {}
for idx in range(len(newDict)):
    finalDict[idx] = newDict[idx]
# print(finalDict)
torch.save(finalDict, target)