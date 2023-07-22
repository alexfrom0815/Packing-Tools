import numpy as np
import trimesh
import os
import transforms3d
import numpy as np

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

root = '/home/hang/Documents/GitHub/IRBPP/data/datas/'

source = 'tetris3D_tolerance_middle'
target = 'tetris3D_tolerance_middle_nomin'

if not os.path.exists(os.path.join(root,target)):
    os.makedirs(os.path.join(root, target))

for f in os.listdir(os.path.join(root, source)):
    meshPath = os.path.join(root, source, f)
    mesh = trimesh.load(meshPath)
    rot = np.random.randint(360)
    mat = transforms3d.euler.euler2mat(0,0, rot / 360 * 2 * np.pi)
    mat = extendMat(mat)
    mesh.apply_transform(mat)
    mesh.apply_translation(-mesh.center_mass)
    mesh.export(os.path.join(root, target, f))
