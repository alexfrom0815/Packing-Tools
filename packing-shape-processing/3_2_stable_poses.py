import torch
import trimesh
import os
import numpy as np
import transforms3d
import pybullet as p
import pyquaternion
import sys
sys.path.append('../../')
from environment.physics0.Interface import Interface

# Generate the stable poses for the objects.

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

interVal = 20
root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

datatype = 'ycb' # apc ycb rss
base_path = '0_{}_scale'.format(datatype)
expName = '3_{}_stable_poses'.format(datatype)

base_path = os.path.join(root, base_path)
vhacd_path = os.path.join(root, '5_{}_vhacd'.format(datatype))
target_path = os.path.join(root, expName)

logDir = os.path.join(root, 'debug', expName)

if not os.path.exists(target_path): os.makedirs(target_path)
if not os.path.exists(logDir) : os.makedirs(logDir)
dirs = os.listdir(base_path)

bin_dimension = [0.8, 0.8, 0.30]
objPath = os.path.join(root, vhacd_path)
interface = Interface(bin=bin_dimension, foldername=objPath,
                      visual=False, scale=[1, 1, 1])

for PlyPath in dirs:
    name = PlyPath[0:-4]
    print(name)
    record = os.path.join(target_path, name  + '.pt')
    if os.path.exists(record):
        continue
    objPath = os.path.join(base_path,PlyPath)

    mesh = trimesh.load(objPath)
    extentX, extentY = mesh.extents[0:2] * 2

    transforms, probs = mesh.compute_stable_poses()  # Computes stable orientations of a mesh and their quasi-static probabilities.
    transforms = transforms[0:10]
    probs = probs[0:10]

    mesh.apply_translation(-mesh.bounds[0])
    meshList = []
    meshExtents = []

    # Firstly, Check whether this shape is stable is simulator


    validT = []
    for T in transforms:
        quat = transforms3d.quaternions.mat2quat(T[0:3, 0:3])
        quat = [quat[1], quat[2], quat[3], quat[0]]  # Saved in xyzw

        id = interface.addObject(name,
                                 targetFLB=[0.4, 0.4, 0],
                                 rotation=quat,
                                 linearDamping=0.5,
                                 angularDamping=0.5)

        _, vertices = p.getMeshData(id)
        vertices = np.array(vertices)

        aabbBefore = interface.get_wraped_AABB(id)
        _, orienBefore, positionBefore = interface.get_Wraped_Position_And_Orientation(id, getPosBase=True)

        succeeded, valid = interface.simulateToQuasistatic(linearTol=0.01, angularTol=0.01, maxBatch=10)
        aabbAfter = p.getAABB(id)
        _, orienAfter, positionAfter = interface.get_Wraped_Position_And_Orientation(id, getPosBase=True)

        interface.removeBody(id)

        q1 = pyquaternion.Quaternion([orienBefore[3], *orienBefore[0:3]])  # wxyz
        q2 = pyquaternion.Quaternion([orienAfter[3], *orienAfter[0:3]])
        r_diff = pyquaternion.Quaternion.absolute_distance(q1, q2)

        t_diff = np.linalg.norm(np.array(positionBefore) - np.array(positionAfter))

        if r_diff > 0.1 or t_diff > 0.05:
            continue
        validT.append(T)

    transforms = validT
    # Secondly, Check if this shape is repeat in the list
    for i in range(len(transforms)):
        T = transforms[i]

        mesh2tran = mesh.copy()
        mesh2tran.apply_transform(T)
        mesh2tran.apply_translation(-mesh2tran.bounds[0])

        # place the shape with given prefer
        angles = 360
        areaList = []
        rotMeshList = []
        for angleIdx in range(angles):
            rotMesh =  mesh2tran.copy()
            Tz = extendMat(transforms3d.euler.euler2mat(0, 0, angleIdx * np.pi * 2 / angles, 'sxyz'))
            rotMesh.apply_transform(Tz)

            if rotMesh.extents[0] <= rotMesh.extents[1]: # x 方向要少
                if rotMesh.center_mass[1] <= rotMesh.centroid[1]:
                    areaList.append(rotMesh.extents[0] * rotMesh.extents[1])
                    rotMeshList.append(rotMesh.copy())

        bestAngle = int(np.argmin(areaList))
        mesh2tran = rotMeshList[bestAngle]
        mesh2tran.apply_translation(-mesh2tran.bounds[0])
        meshList.append(mesh2tran)
        meshExtents.append(mesh2tran.extents)

    if len(meshList) != 0:
        threshhold = 0.2 # 感覺應該自適應地挑選一個分位, 不過這個地方意義不大, 先暫時放棄
        lenPos = len(meshList)
        invalidList = []
        validList = []
        meshExtents = np.max(np.array(meshExtents),axis=0)

        xRange = np.linspace(0, meshExtents[0], interVal)
        yRange = np.linspace(0, meshExtents[1], interVal)
        zRange = np.linspace(0, meshExtents[2], interVal)

        x = xRange.repeat(interVal * interVal, axis=0).reshape(-1, 1)
        y = yRange.repeat(interVal, axis=0).reshape((1, -1)).repeat(interVal, axis=0).reshape(-1, 1)
        z = zRange.reshape((1, -1)).repeat(interVal * interVal, axis=0).reshape(-1, 1)
        points = np.concatenate([x, y, z], axis=1)

        checkLabels = [m.contains(points) for m in meshList]

        for i in range(lenPos):
            if i in invalidList: continue
            for j in range(i + 1, lenPos):
                if j in invalidList: continue
                verticesI = checkLabels[i]
                verticesJ = checkLabels[j]

                xorDistance = np.sum(np.logical_xor(verticesI, verticesJ))
                percentage = xorDistance / np.sum(verticesI)

                percentage /= 2
                print('dist {} and {}: {}'.format(i, j, percentage))
                if  percentage < threshhold: # 距离越小越相似, 应该删去
                    invalidList.append(j)
            validList.append(i)

        validTransforms = [transforms[i] for  i in validList]
        f = open(logDir + '/{}.txt'.format(name), 'w')
        for s in validTransforms:
            f.writelines(str(s.tolist()) + '\n')
        f.close()
        torch.save(validTransforms, logDir + '/{}.pt'.format(name))

        torch.save(validTransforms, target_path + '/{}.pt'.format(name))

