import trimesh
import os
import shutil
import random

folderList = ['abc_0001_obj_v00']
counter = 0
for folder in folderList:
    root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/ABC/download/obj/'
    basePath = os.path.join(root,folder)
    targetPath = os.path.join(root, folder + 'Clean')

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    for dir in os.listdir(basePath):
        dirPath = os.path.join(basePath, dir)
        dirList = os.listdir(dirPath)

        if len(dirList) > 0:
            counter += 1
            # meshPath = os.path.join(dirPath, dirList[0])
            # shutil.copy(meshPath, os.path.join(targetPath, dirList[0]))

            # mesh = trimesh.load(meshPath)
            # # print(mesh.scale)
            # print(mesh.is_watertight)
            # # print(len(mesh.vertices))
            # # trimesh.primitives.Box().is_watertight
print(counter)

