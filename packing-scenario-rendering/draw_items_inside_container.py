import os
import sys
if os.path.exists('/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox'):
    sys.path.append('/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox') # change this to your path to “path/to/BlenderToolbox/
elif os.path.exists('/home/dell/zhaohang/IRBPP/picture/BlenderToolbox'):
    sys.path.append('/home/dell/zhaohang/IRBPP/picture/BlenderToolbox')
else:
    assert os.path.exists('/home/zhaohang/zhaohang/IRBPP/picture/BlenderToolbox')
    sys.path.append('/home/zhaohang/zhaohang/IRBPP/picture/BlenderToolbox') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import numpy as np
import os
import transforms3d
import trimesh
from allColor import allColor
import bpy

selectedColor = [allColor[35],
                 allColor[28],
                 allColor[34],
                 allColor[38],
                 allColor[29],
                 allColor[30],
                 allColor[31],
                 allColor[37]
                 ]

def extendMat(mat3, translation = None):
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

# ~/zhaohang/tools/blender-3.1.2-linux-x64/blender --background --python draw_single_mesh.py
# ~/tools/blender-3.1.2-linux-x64/blender --background --python

scriptName = 'episodeFigureDown'

# taskName = 'IR_mix_no_vhacd'
# taskName = 'tetris3D_tolerance_middle_tri_to_quad'
taskName = 'IR_concaveArea3'

if taskName == 'IR_mix_no_vhacd':
    folderList = [
        'IR_mix_mass_pcd_half-2022.09.02-18-15-06',
        'IR_mix_mass_pcd_half_hier_10_for_draw_10_10-2022.09.02-20-42-17',
        'IR_mix_mass_pcd_half_hier_10_for_draw_10_5-2022.09.02-20-42-33',
        'IR_mix_mass_pcd_half_hier_10_for_draw_10_3-2022.09.02-20-42-51',
                ]
elif taskName == 'tetris3D_tolerance_middle_tri_to_quad':
    folderList = [
        'new_tetris3D_mass_middle_30_for_draw-2022.09.02-18-49-37',
        'new_tetris3D_mass_middle_30_hier_10_for_draw_10_10-2022.09.02-18-53-09',
        'new_tetris3D_mass_middle_30_hier_10_for_draw_10_5-2022.09.02-18-53-19',
        'new_tetris3D_mass_middle_30_hier_10_for_draw_10_3-2022.09.02-18-53-27',
                ]
elif taskName == 'IR_concaveArea3':
    folderList = [
        'IR_concaveArea3_mass_category-2022.09.02-19-12-53',
        'IR_concaveArea3_mass_hier_10_continue_for_draw_10_10-2022.09.02-19-16-12',
        'IR_concaveArea3_mass_hier_10_continue_for_draw_10_5-2022.09.02-19-16-25',
        'IR_concaveArea3_mass_hier_10_continue_for_draw_10_3-2022.09.02-19-16-49',
    ]

bin_dimension = np.array([0.32,0.32,0.3])

selected = []
if taskName == 'IR_mix_no_vhacd':
    selected = [193, 361, 375, 385, 841, 875, 877, 920, 951, 970, 979, 1104, 1197, 1205, 1228, 1260, 1327, 1357, 1448, 1519, 1608, 1626, 1707, 1856]

elif taskName == 'tetris3D_tolerance_middle_tri_to_quad':
    selected = [336, 361, 381, 511, 782, 948, 1144, 1246, 1256, 1369, 1428, 1521, 1767, 1904, 1987]

elif taskName == 'IR_concaveArea3':
    selected =  [28, 118, 146, 377, 413, 661, 720, 814, 893, 988, 1005, 1053, 1057, 1088, 1225, 1309, 1387, 1403, 1485, 1513, 1533, 1666, 1811]


for trajIdx in selected:
    for folder in folderList:


        dataPath = './tempdata/evaluation/{}/trajs.npy'.format(folder)
        meshInputPath = './meshes/packing/{}'.format(taskName)
        imageOutputPath = "./images/{}/{}/{}".format(scriptName, taskName, folder)
        meshOutputPath = './tempdata/{}/{}/{}'.format(scriptName, taskName, folder)

        outputPath = os.path.join(imageOutputPath, 'traj_{}.png'.format(trajIdx))
        if os.path.exists(outputPath): continue
        if not os.path.exists(imageOutputPath): os.makedirs(imageOutputPath)
        if not os.path.exists(meshOutputPath): os.makedirs(meshOutputPath)

        containerPath = './meshes/packing/containerInUse/box_{}_{}_{}'.format(*bin_dimension)
        assert os.path.exists(containerPath), 'run generateContainer.py first'

        baseScale = 1.25
        base_position = np.array((0.0, -0.9, 0.0))
        base_rotation = np.array([0,   0,    45])
        baseScale = np.array((1,1,1)) * baseScale / np.max(bin_dimension)

        trajs = np.load(dataPath, allow_pickle=True)

        tempPath = os.path.join(meshOutputPath, str(trajIdx))
        if not os.path.exists(tempPath):
            os.makedirs(tempPath)
        traj = trajs[trajIdx]

        meshPathList = []
        for i in range(5):
            meshPathList.append(os.path.join(containerPath, 'Box{}.obj'.format(i)))
        containerLength = len(meshPathList)
        thick = trimesh.load(meshPathList[0]).extents[2]

        for itemIdx in range(len(traj)-1): # The last item is not valid.
            item = traj[itemIdx]
            name = item[1]
            positionT, orientationT = item[2:]
            positionT = np.array(positionT)  # xyzw
            meshFile = os.path.join(meshInputPath, name)
            mesh = trimesh.load_mesh(meshFile)
            mesh.apply_transform(extendMat(transforms3d.quaternions.quat2mat([orientationT[3], *orientationT[0:3]])))
            mesh.apply_translation(-mesh.bounds[0])
            mesh.apply_translation(positionT)
            mesh.apply_translation([-bin_dimension[0]/2, -bin_dimension[1]/2, thick])

            tempFile = os.path.join(tempPath, '{}.obj'.format(itemIdx))
            mesh.export(tempFile)
            meshPathList.append(tempFile)

        args = {
            # "output_path": imageOutputPath,
            "output_path": os.path.join(imageOutputPath, 'traj_{}.png'.format(trajIdx)),
            "image_resolution": [1080, 1080],  # recommend >1080 for paper figures
            "number_of_samples": 200,  # recommend >200 for paper figures
            "mesh_path": meshPathList,  # either .ply or .obj
            "mesh_position": (0, 0, 0),  # UI: click mesh > Transform > Location
            "mesh_rotation": (0, 0, 0),  # UI: click mesh > Transform > Rotation
            "mesh_scale": baseScale.tolist(),  # UI: click mesh > Transform > Scale
            "shading": "smooth",  # either "flat" or "smooth"
            "subdivision_iteration": 1,  # integer
            "mesh_RGB": [144.0 / 255, 210.0 / 255, 236.0 / 255],  # mesh RGB
            # "light_angle": (6, -30, -155)  # UI: click Sun > Transform > Rotation
            "light_angle": (0, 0, 0)  # UI: click Sun > Transform > Rotation
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

        for partIdx, partPath in enumerate(meshPath):
            print(partPath)
            is_container = False
            if partIdx < containerLength:
                is_container = True

            mesh = bt.readMesh(partPath, location, rotation, scale)

            ## set shading (uncomment one of them)
            if args["shading"] == "smooth":
                bpy.ops.object.shade_smooth()
            elif args["shading"] == "flat":
                bpy.ops.object.shade_flat()
            else:
                raise ValueError("shading should be either flat or smooth in lazy pipeline")

            ## subdivision
            # if partIdx > containerLength:
            bt.subdivision(mesh, level=args["subdivision_iteration"])

            ## default render as plastic
            if is_container:
                RGB = allColor[6]
                # RGB = np.array([170, 145,  100]) * 1.0 / 255
            else:
                RGB = selectedColor[partIdx % len(selectedColor)]

            RGBA = (RGB[0], RGB[1], RGB[2], 1)
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            # setMat_plastic(mesh, meshColor) # 这个是塑料材质的, 我想要单色
            AOStrength = 0.0
            bt.setMat_singleColor(mesh, meshColor, AOStrength)

        ## set invisible plane (shadow catcher)
        bt.invisibleGround(shadowBrightness=0.9)
        # bt.invisibleGround(shadowBrightness=1)

        ## set camera
        camLocation = (0, 0, 3)
        lookAtLocation = (0, 0, 0.5)
        focalLength = 45  # (UI: click camera > Object Data > Focal Length)
        cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

        ## Option1: Three Point Light System
        # bt.setLight_threePoints(radius=4, height=10, intensity=1700, softness=6, keyLoc='left')
        ## set light
        lightAngle = args["light_angle"]
        strength = 2
        shadowSoftness = 0.3
        sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

        ## set ambient light
        bt.setLight_ambient(color=(0.1, 0.1, 0.1, 1))

        ## set gray shadow to completely white with a threshold (optional but recommended)
        bt.shadowThreshold(alphaThreshold=0.05, interpolationMode='CARDINAL')
        # bt.shadowThreshold(alphaThreshold=1, interpolationMode='CARDINAL')

        ## save blender file so that you can adjust parameters in the UI
        bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

        ## save rendering
        bt.renderImage(args["output_path"], cam)

        bpy.ops.wm.read_factory_settings(use_empty=True)

