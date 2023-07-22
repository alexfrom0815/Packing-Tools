import torch
import trimesh
import os
import numpy as np
import transforms3d



def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

interVal = 20
root = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing'

# datatype = 'apc' # apc ycb rss
datatype = 'ycb' # apc ycb rss


# base_path = '2_{}_filt_8'.format(datatype)
base_path = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_{}_off'.format(datatype)
expName = '3_{}_origin_stable_poses'.format(datatype)
# originshape不是water tight的, 无法检查contain
target_path = os.path.join(root, expName)

logDir = os.path.join(root, 'debug', expName)

if not os.path.exists(target_path): os.makedirs(target_path)
if not os.path.exists(logDir) : os.makedirs(logDir)
dirs = os.listdir(base_path)

bin_dimension = [0.8, 0.8, 0.30]

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

    # Secondly, Check if this shape is repeat in the list
    validTransforms = [transforms[i] for  i in range(min(3, len(transforms)))]
    torch.save(validTransforms, logDir + '/{}.pt'.format(name))
    torch.save(validTransforms, target_path + '/{}.pt'.format(name))
