import os
import trimesh
import numpy as np
import BlenderToolBox as bt
import bpy
import transforms3d
from allColor import allColor

selectedColor = [allColor[35], # yellow
                 allColor[0], # derekBlue
                 allColor[34], # green
                 allColor[38], # purple
                 allColor[29], # red
                 allColor[30], # brown
                 ]
black = (0.3,0.3,0.3,1)
gray = (0.65, 0.65, 0.65, 1) # not useful
white = allColor[6]
blue  = allColor[37]  # blue
brown = allColor[30]  # light brown
red = allColor[29] # red
darkWhite = allColor[31] # 31 this is the perfect white
lightYellow = allColor[42]
darkYellow = allColor[17]
orange = allColor[3]
deepOrange = allColor[14]
lightPink = allColor[28]
derekBlue = allColor[0]

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

scriptName = 'singleMesh'

meshInputPath = './meshes/packing/tetris3D'

taskName = meshInputPath.split('/')[-1]
imageOutputPath = "./images/{}/{}".format(scriptName, taskName)
meshOutputPath = './tempdata/{}/{}'.format(scriptName, taskName)

if not os.path.exists(imageOutputPath):
  os.makedirs(imageOutputPath)
if not os.path.exists(meshOutputPath):
  os.makedirs(meshOutputPath)

meshList = ['2_3T_0.obj']
baseScale = 1.25
globalScale = None

if 'tetris3D' in taskName:
    scaleList = []
    for meshFileName in meshList:
        mesh = trimesh.load(os.path.join(meshInputPath, meshFileName))
        scaleList.append(baseScale / np.max(mesh.extents))
        scaleList.append(baseScale / mesh.scale)
    globalScale = np.min(scaleList)

for meshFileName in meshList:
    meshName = meshFileName[0:-4]

    mesh = trimesh.load(os.path.join(meshInputPath, meshFileName))
    if globalScale is None:
        mesh.apply_scale(baseScale / np.max(mesh.extents))
    else:
        mesh.apply_scale(globalScale)

    angles = 720
    areaList = []
    angleList = []
    for angleIdx in range(angles):
        rotMesh = mesh.copy()
        Tz = extendMat(transforms3d.euler.euler2mat(0, 0, angleIdx * np.pi * 2 / angles, 'sxyz'))
        rotMesh.apply_transform(Tz)

        if rotMesh.extents[0] <= rotMesh.extents[1]:
            if rotMesh.center_mass[1] <= rotMesh.centroid[1]:
                areaList.append(rotMesh.extents[0] * rotMesh.extents[1])
                angleList.append(angleIdx)

    bestAngleIdx = int(np.argmin(areaList))
    Tz = extendMat(transforms3d.euler.euler2mat(0, 0, angleList[bestAngleIdx] * np.pi * 2 / angles, 'sxyz'))
    mesh.apply_transform(Tz)

    mesh.apply_translation([*-mesh.centroid[0:2], -mesh.bounds[0][2]])
    mesh.export(os.path.join(meshOutputPath, meshFileName))

    for rotIdx in range(2):
        args = {
          "output_path": os.path.join(imageOutputPath, meshName + '_{}.png'.format(rotIdx)),
          "image_resolution": [512, 512], # recommend >1080 for paper figures
          "number_of_samples": 200, # recommend >200 for paper figures
          "mesh_path": os.path.join(meshOutputPath, meshFileName), # either .ply or .obj
          "mesh_position": (0.5, 0, 0), # UI: click mesh > Transform > Location
          "mesh_rotation": (0, 0, 35 + 180 * rotIdx), # UI: click mesh > Transform > Rotation
          "mesh_scale": (1,1,1), # UI: click mesh > Transform > Scale
          "shading": "smooth", # either "flat" or "smooth"
          "subdivision_iteration": 0, # integer
          "mesh_RGB": [144.0/255, 210.0/255, 236.0/255], # mesh RGB
          "light_angle": (6, -30, -155) # UI: click Sun > Transform > Rotation
        }

        ## initialize blender
        imgRes_x = args["image_resolution"][0]
        imgRes_y = args["image_resolution"][1]
        numSamples = args["number_of_samples"]
        exposure = 1.5
        bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

        ## read mesh (choose either readPLY or readOBJ)
        meshPath = args["mesh_path"]
        location = args["mesh_position"]
        rotation = args["mesh_rotation"]
        scale = args["mesh_scale"]
        mesh = bt.readMesh(meshPath, location, rotation, scale)

        ## set shading (uncomment one of them)
        if args["shading"] == "smooth":
          bpy.ops.object.shade_smooth()
        elif args["shading"] == "flat":
          bpy.ops.object.shade_flat()
        else:
          raise ValueError("shading should be either flat or smooth in lazy pipeline")

        ## subdivision
        bt.subdivision(mesh, level = args["subdivision_iteration"])

        ## default render as plastic
        RGB = args["mesh_RGB"]
        RGBA = (RGB[0], RGB[1], RGB[2], 1)
        meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
        AOStrength = 0.0
        bt.setMat_singleColor(mesh, meshColor, AOStrength)

        ## set invisible plane (shadow catcher)
        bt.invisibleGround(shadowBrightness=0.9)

        ## set camera
        camLocation = (3, 0, 2)
        lookAtLocation = (0,0,0.5)
        focalLength = 45 # (UI: click camera > Object Data > Focal Length)
        cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

        ## Option1: Three Point Light System
        # bt.setLight_threePoints(radius=4, height=10, intensity=1700, softness=6, keyLoc='left')
        ## set light
        lightAngle = args["light_angle"]
        strength = 2
        shadowSoftness = 0.3
        sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

        ## set ambient light
        bt.setLight_ambient(color=(0.1,0.1,0.1,1))

        ## set gray shadow to completely white with a threshold (optional but recommended)
        bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

        ## save blender file so that you can adjust parameters in the UI
        bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

        ## save rendering
        bt.renderImage(args["output_path"], cam)

        bpy.ops.wm.read_factory_settings(use_empty=True)
