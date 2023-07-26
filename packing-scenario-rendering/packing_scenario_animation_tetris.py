import sys
import os
import trimesh
import time
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

black = (0.38,0.38,0.38,1)
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
lightBlue = allColor[0]
# light warm color as background, deep cool color as target

def extendMat(mat3, translation = None):
    # print(mat3, translation)
    mat4 = np.eye(4)
    mat4[0:3,0:3] = mat3
    if translation is not None:
        mat4[0:3,3] = translation
    return mat4

def readMat(mat4):
    # print('readMat mat', mat4)
    translation = mat4[0:3, 3]
    mat3 = mat4[0:3,0:3]
    eulers = transforms3d.euler.mat2euler(mat3)
    # print('readMat pose', translation, eulers)
    return translation, eulers

def reLocate(mesh, location, rotation_euler):
    x = rotation_euler[0] * 1.0 / 180.0 * np.pi
    y = rotation_euler[1] * 1.0 / 180.0 * np.pi
    z = rotation_euler[2] * 1.0 / 180.0 * np.pi
    angle = (x,y,z)

    mesh.location = location
    mesh.rotation_euler = angle
    mesh.scale = scale
    bpy.context.view_layer.update()

    return mesh

def add_incontainer_object(meshPathList, poseList, color = None):
    meshes = []
    for partIdx, partPath in enumerate(meshPathList):
        # if 'robot' not  in partPath: continue
        # print(partIdx, partPath)

        poses = poseList[partIdx]
        orientation = poses[1]
        position = poses[0]
        print(position, orientation)

        meshincontainer = trimesh.load(partPath)
        drawMat = extendMat(transforms3d.euler.quat2mat([orientation[3], *orientation[0:3]])) #

        meshAfterRot = meshincontainer.copy()
        meshAfterRot.apply_transform(drawMat)

        tranlationMat = extendMat(eye, -meshAfterRot.bounds[0])
        drawMat = np.dot(tranlationMat, drawMat)

        tranlationMat = extendMat(eye, position)
        drawMat = np.dot(tranlationMat, drawMat)

        tranlationMat = extendMat(eye, [*(container.centroid[0:2] - bin_dimension[0:2] / 2), thick])
        drawMat = np.dot(tranlationMat, drawMat)

        subMat = drawMat
        newMat = np.dot(originMat,subMat)
        location, rotation = readMat(newMat)
        rotation = np.array(rotation) / np.pi * 180

        mesh = bt.readMesh(partPath, location, rotation, scale)
        meshes.append(mesh)

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
        colorIdx = (partIdx) % len(selectedColor)
        label = partPath.split('/')[-1]

        if color is not None:
            RGB = color
        else:
            RGB = selectedColor[colorIdx]
        RGBA = (RGB[0], RGB[1], RGB[2], 1)

        if label in [ 'camera.obj', 'camera2.obj', 'robot.obj']:
            alpha = 1
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            transmission = 0.0
            bt.setMat_transparent(mesh, meshColor, alpha, transmission)
        else:
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            # setMat_plastic(mesh, meshColor) # 这个是塑料材质的, 我想要单色
            AOStrength = 0.0
            bt.setMat_singleColor(mesh, meshColor, AOStrength)
    return meshes


timeStr = time.strftime('%Y.%m.%d-%H-%M-%S', time.localtime(time.time()))

scriptName = 'largeScene'
taskName = 'tetrisBuffer'
imageOutputPath = "./images/{}/{}/{}".format(scriptName, taskName, timeStr)
meshOutputPath = './tempdata/{}/{}'.format(scriptName, taskName)

if not os.path.exists(imageOutputPath):
  os.makedirs(imageOutputPath)
if not os.path.exists(meshOutputPath):
  os.makedirs(meshOutputPath)


baseScale = 1
baseposition = (0.2, -0.2, 0)
baserotation = (0, 0, 230)
baseposition = np.array(baseposition)
baserotation = np.array(baserotation)

meshList = os.listdir(meshOutputPath)

originMat = extendMat(transforms3d.euler.euler2mat(*(baserotation/180 * np.pi)), baseposition)
trajPosesSchedule = np.load('./dynamicsData/robotPosesTetris.npy', allow_pickle=True)
trajPoses = []
for traj in trajPosesSchedule:
    trajPoses += traj
trajPoses = np.array(trajPoses)

schedule = [240, 160, 250, 300, 30, 30, 70, 30, 30, 300, 80, 110, 120, 110]
FirstLength = schedule[0]
SecondLength = np.sum(schedule[0:5])
ThirdLength = np.sum(schedule[0:8])
ForthLength = np.sum(schedule[0:-2])
TotalLength = np.sum(schedule)




meshOnBeltBasicTrans = []
meshOnBeltBasicX = []

objectMeshDir = './meshes/packing/tetris3D_for_animation/'
shapeonbelt = [
    '1_2I_0.obj',
    '2_3L_1.obj',
    '1_1B_0.obj',
    '2_3T_1.obj',
    '2_2B_1.obj'
               ]

for i in range(len(shapeonbelt)):
    shapeonbelt[i] = os.path.join(objectMeshDir, shapeonbelt[i])

shapeonbelt.insert(0, os.path.join(meshOutputPath,
                                   'tetrisForAnimationHand.obj'))


allparts = './meshes/packing/largeScene/{}/sceneParts/'.format('IRBPP')
camera = trimesh.load(os.path.join(allparts, 'camera.obj'))
wareHouse = trimesh.load(os.path.join(allparts, 'warehouse.obj'))
beltBody =  trimesh.load(os.path.join(allparts, 'beltBody.obj'))
container =  trimesh.load(os.path.join(allparts, 'container.obj'))
bin_dimension = np.array([0.32,0.32,0.3])
minX = camera.centroid[0]
maxX = wareHouse.bounds[0][0]
objectInter = (maxX - minX) / 5
thick = 0.01

for idx, meshonbeltName in enumerate(shapeonbelt):
    meshonbelt = trimesh.load(meshonbeltName)
    transforms, _ = meshonbelt.compute_stable_poses()
    eye = np.eye(3)
    drawMat = transforms[0]

    meshAfterRot = meshonbelt.copy()
    meshAfterRot.apply_transform(drawMat)

    tranlationMat = extendMat(eye, [*(-meshAfterRot.centroid[0:2]), beltBody.bounds[1][2]-meshAfterRot.bounds[0][2]])
    drawMat = np.dot(tranlationMat, drawMat)

    tranlationMat = extendMat(eye, [0,beltBody.centroid[1], 0])
    drawMat = np.dot(tranlationMat, drawMat)

    meshOnBeltBasicTrans.append(drawMat)
    meshOnBeltBasicX.append(objectInter * (idx + 1) + minX)

objectMeshDir = './meshes/packing/tetris3D_for_animation'
incontainerPathList, initList, incontainerTrajList = np.load('./dynamicsData/incontainerDynamicsTetris.npy', allow_pickle=True)
for idx, name in enumerate(incontainerPathList):
    incontainerPathList[idx] = os.path.join(objectMeshDir, name)
incontainerPathList.append(os.path.join(meshOutputPath, 'robotParts', 'tetrisForAnimationT.obj'))
if True:
    robotPathList = []
    scenePathList = []
    bufferPathList = []
    folderName = 'robotParts'
    for linkIdx in range(7):
        partPath = 'link{}.obj'.format(linkIdx + 1)
        savepath = os.path.join(meshOutputPath, folderName, partPath)
        robotPathList.append(savepath)
    robotPathList.append(os.path.join(meshOutputPath, folderName, 'suction.obj'))
    robotPathList.append(os.path.join(meshOutputPath, folderName, 'tetrisForAnimationHand.obj'))
    robotPathList.append(os.path.join(meshOutputPath, folderName, 'tetrisForAnimationT.obj'))

    folderName = 'sceneParts'
    for partPath in os.listdir(os.path.join(meshOutputPath, folderName)):
        if partPath in ['stand.obj',  'stand2.obj', 'camera3.obj']: continue
        savepath = os.path.join(meshOutputPath, folderName, partPath)
        scenePathList.append(savepath)

    folderName = 'bufferParts'
    for idx in range(3):
            savepath = os.path.join(meshOutputPath, folderName, 'object{}.obj'.format(idx))
            bufferPathList.append(savepath)
    bufferPathList.append(os.path.join(meshOutputPath, folderName, 'plane.obj'))
    scenePathList += bufferPathList

    args = {
      # "image_resolution": [4096, 4096], # recommend >1080 for paper figures
      # "image_resolution": [512, 512], # recommend >1080 for paper figures
      # "image_resolution": [2800, 2800], # recommend >1080 for paper figures
      "image_resolution": [1400, 1400], # recommend >1080 for paper figures
      # "image_resolution": [280, 280], # recommend >1080 for paper figures
      "number_of_samples": 400, # recommend >200 for paper figures

      "mesh_scale": (baseScale,baseScale,baseScale), # UI: click mesh > Transform > Scale
      "shading": "smooth", # either "flat" or "smooth"
      "subdivision_iteration": 1, # integer
      "mesh_RGB": [144.0/255, 210.0/255, 236.0/255], # mesh RGB
      "light_angle": (6, -30, -155) # UI: click Sun > Transform > Rotation
    }

    ## initialize blender
    imgRes_x = args["image_resolution"][0]
    imgRes_y = args["image_resolution"][1]
    numSamples = args["number_of_samples"]
    exposure = 1.5
    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure, useBothCPUGPU=True, device='GPU')

    ## read mesh (choose either readPLY or readOBJ)

    # location = args["mesh_position"]
    # rotation = args["mesh_rotation"]

    scale = args["mesh_scale"]

    incontaierMeshes = []
    incontaierMeshes = add_incontainer_object(incontainerPathList[0:-1], initList)

    # # draw scene parts
    for partIdx, partPath in enumerate(scenePathList):
        if 'object.obj' in partPath: continue
        print(partIdx, partPath)
        mesh = bt.readMesh(partPath, baseposition, baserotation, scale)

        ## set shading (uncomment one of them)
        if args["shading"] == "smooth":
            bpy.ops.object.shade_smooth()
        elif args["shading"] == "flat":
            bpy.ops.object.shade_flat()
        else:
            raise ValueError("shading should be either flat or smooth in lazy pipeline")

        ## subdivision
        bt.subdivision(mesh, level=args["subdivision_iteration"])

        ## default render as plastic
        # colorIdx = np.random.randint(len(selectedColor))
        colorIdx = (partIdx + 1) % len(selectedColor)
        label = partPath.split('/')[-1]
        # if label in [ 'camera.obj', 'camera2.obj', 'camera3.obj']:
        if label in ['camera.obj', 'camera2.obj', 'camera5.obj']:
            RGB = black
        elif label in ['container.obj', 'stand5.obj', 'stand6.obj', 'stand7.obj']:
            # RGB = white
            RGB = darkWhite
        elif label in ['beltBody.obj', 'warehouse.obj', 'cylinderIn.obj']:
            RGB = allColor[38]
        elif label in ['beltTop.obj', 'cylinderOut.obj']:
            RGB = lightPink
        elif 'plane' in label:
            RGB = lightPink
        elif 'object0' in label:
            RGB = allColor[34]
        elif 'object1' in label:
            RGB = allColor[0]
        elif 'object2' in label:
            RGB = allColor[30]
        else:
            RGB = selectedColor[colorIdx]
        RGBA = (RGB[0], RGB[1], RGB[2], 1)
        # if label in [ 'camera.obj', 'camera2.obj', 'robot.obj']:
        if label in ['robot.obj']:
            alpha = 1
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            transmission = 0.0
            bt.setMat_transparent(mesh, meshColor, alpha, transmission)
        else:
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            # setMat_plastic(mesh, meshColor) # 这个是塑料材质的, 我想要单色
            AOStrength = 0.0
            bt.setMat_singleColor(mesh, meshColor, AOStrength)

    # init robot parts
    robotMeshes = []
    for partIdx, partPath in enumerate(robotPathList):
        # if 'robot' not  in partPath: continue
        if 'tetrisForAnimationT' not in partPath:
            robotPoses = trajPoses[0]
        else:
            robotPoses = trajPoses[ThirdLength]
            partIdx -= 1
        subMat = extendMat(transforms3d.euler.euler2mat(*robotPoses[partIdx][1],  'rxyz'), robotPoses[partIdx][0]) #
        # # newMat = np.dot(subMat,np.linalg.inv(mat))
        newMat = np.dot(originMat,subMat)
        # print('part pose', newMat)
        location, rotation = readMat(newMat)
        rotation = np.array(rotation) / np.pi * 180
        # print('read', location, rotation)

        mesh = bt.readMesh(partPath, location, rotation, scale)
        robotMeshes.append(mesh)

        ## set shading (uncomment one of them)
        if args["shading"] == "smooth":
          bpy.ops.object.shade_smooth()
        elif args["shading"] == "flat":
          bpy.ops.object.shade_flat()
        else:
          raise ValueError("shading should be either flat or smooth in lazy pipeline")

        ## subdivision
        bt.subdivision(mesh, level = args["subdivision_iteration"])

        colorIdx = (partIdx + 3) % len(selectedColor)
        label = partPath.split('/')[-1]
        if 'link' in label or 'suction' in label:
            RGB = blue
        elif 'tetrisForAnimationT' in partPath:
            RGB = red
        elif 'tetrisForAnimationHand' in partPath:
            RGB = allColor[38]
        else:
            RGB = selectedColor[colorIdx]

        RGBA = (RGB[0], RGB[1], RGB[2], 1)
        if label in [ 'camera.obj', 'camera2.obj', 'robot.obj']\
                or 'link' in label or 'suction' in label:
            alpha = 1
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            transmission = 0.0
            bt.setMat_transparent(mesh, meshColor, alpha, transmission)
        else:
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            AOStrength = 0.0
            bt.setMat_singleColor(mesh, meshColor, AOStrength)

    objectMeshes = []
    for partIdx, partPath in enumerate(shapeonbelt):
        if 'tetrisForAnimation' in partPath:
            objectMeshes.append(robotMeshes[-2])
            continue

        subMat = meshOnBeltBasicTrans[partIdx]
        newMat = np.dot(originMat, subMat)
        # print('part pose', newMat)
        location, rotation = readMat(newMat)
        rotation = np.array(rotation) / np.pi * 180
        # print('read', location, rotation)

        mesh = bt.readMesh(partPath, location, rotation, scale)
        objectMeshes.append(mesh)

        ## set shading (uncomment one of them)
        if args["shading"] == "smooth":
            bpy.ops.object.shade_smooth()
        elif args["shading"] == "flat":
            bpy.ops.object.shade_flat()
        else:
            raise ValueError("shading should be either flat or smooth in lazy pipeline")

        ## subdivision
        bt.subdivision(mesh, level=args["subdivision_iteration"])

        ## default render as plastic
        # colorIdx = np.random.randint(len(selectedColor))
        colorIdx = (partIdx + 2) % len(selectedColor)
        label = partPath.split('/')[-1]

        if 'link' in label or 'suction' in label:
            RGB = blue

        elif '1_2I_0' in partPath:
            RGB = allColor[30]
        elif '2_3L_1' in partPath:
            RGB = allColor[0]
        elif '1_1B_0' in partPath:
            RGB = allColor[34]
        elif '2_3T_1' in partPath:
            RGB = allColor[35]
        elif '2_2B_1' in partPath:
            RGB = allColor[38]
        else:
            RGB = selectedColor[colorIdx]
        RGBA = (RGB[0], RGB[1], RGB[2], 1)

        if label in ['camera.obj', 'camera2.obj', 'robot.obj']:
            alpha = 1
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            transmission = 0.0
            bt.setMat_transparent(mesh, meshColor, alpha, transmission)
        else:
            meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
            # setMat_plastic(mesh, meshColor) # 这个是塑料材质的, 我想要单色
            AOStrength = 0.0
            bt.setMat_singleColor(mesh, meshColor, AOStrength)

    ## set invisible plane (shadow catcher)
    bt.invisibleGround(shadowBrightness=0.9)

    ## set camera
    camLocation = (3, 0, 2)
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
    bt.setLight_ambient(color=(0.1,0.1,0.1,1))

    ## set gray shadow to completely white with a threshold (optional but recommended)
    bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

    ## save blender file so that you can adjust parameters in the UI
    bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

    # 1800
    # for poseIdx in range(TotalLength):
    startIdx = -1 + 400
    removeDone = False
    poseIdx = -1
    renderInter = 5
    # for poseIdx in range(TotalLength):
    while True:
        poseIdx += renderInter
        if poseIdx > TotalLength:
            break
        # if poseIdx < 800:
        #     continue
        output_path =  os.path.join(imageOutputPath,
                                    '{}.png'.format(str(poseIdx).rjust(7,'0')))

        robotPoses = trajPoses[poseIdx]

        # 物品放入容器并仿真, 删除旧物体
        if poseIdx >= ForthLength:
            icIdx = poseIdx-ForthLength
            if not removeDone:
                objectRemove = robotMeshes[-1]
                # robotMeshes[-1] = None
                objectMeshes[0] = None
                # bpy.data.objects.remove(objectRemove)
                # newHandledObject = add_incontainer_object([incontainerPathList[-1]], incontainerTrajList[icIdx], red)
                incontaierMeshes.append(objectRemove)
                removeDone = True
                alignTrans = np.array([0.000258, - 0.014599, - 0.000167]) # verpMesh.bounds[0] - simulateMesh.bounds[0]

            for partIdx, mesh in enumerate(incontaierMeshes):
                print('partIdx', partIdx)
                incontainerPoses = incontainerTrajList[icIdx][partIdx]
                orientation = incontainerPoses[1]
                position = incontainerPoses[0]
                print(position, orientation)

                meshincontainer = trimesh.load(incontainerPathList[partIdx])
                if partIdx != len(incontaierMeshes) - 1:
                    drawMat = extendMat(transforms3d.euler.quat2mat([orientation[3], *orientation[0:3]]))  #
                else:
                    # alignMat = extendMat(eye, - alignTrans)
                    alignMat = extendMat(eye)
                    drawMat = extendMat(transforms3d.euler.quat2mat([orientation[3], *orientation[0:3]]))  #
                    drawMat = np.dot(drawMat, alignMat)
                meshAfterRot = meshincontainer.copy()
                meshAfterRot.apply_transform(drawMat)

                tranlationMat = extendMat(eye, -meshAfterRot.bounds[0])
                drawMat = np.dot(tranlationMat, drawMat)

                tranlationMat = extendMat(eye, position)
                drawMat = np.dot(tranlationMat, drawMat)

                tranlationMat = extendMat(eye, [*(container.centroid[0:2] - bin_dimension[0:2] / 2), thick])
                drawMat = np.dot(tranlationMat, drawMat)

                subMat = drawMat
                newMat = np.dot(originMat, subMat)
                location, rotation = readMat(newMat)
                rotation = np.array(rotation) / np.pi * 180
                reLocate(mesh, location, rotation)

        # 机器人的移动路径
        for partIdx, mesh in enumerate(robotMeshes):
            if partIdx == len(robotMeshes) - 2: # H
                if poseIdx < FirstLength:
                    continue
                if poseIdx >= SecondLength:
                    continue

            if partIdx == len(robotMeshes) - 1: # T
                if poseIdx < ThirdLength or poseIdx >=ForthLength:
                    continue
                else:
                    partIdx -= 1
            subMat = extendMat(transforms3d.euler.euler2mat(*robotPoses[partIdx][1],  'rxyz'), robotPoses[partIdx][0]) #
            newMat = np.dot(originMat,subMat)
            location, rotation = readMat(newMat)
            rotation = np.array(rotation) / np.pi * 180
            reLocate(mesh, location, rotation)

        # Render the obejct transported by the conveyor belt.
        for partIdx, mesh in enumerate(objectMeshes):
            if poseIdx >= FirstLength and partIdx == 0:
                continue
            drawMat = meshOnBeltBasicTrans[partIdx]
            basicX = meshOnBeltBasicX[partIdx]

            tranlationMat = extendMat(eye, [basicX - objectInter / (TotalLength - 1) * poseIdx, 0, 0])
            drawMat = np.dot(tranlationMat, drawMat)

            newMat = np.dot(originMat,drawMat)
            location, rotation = readMat(newMat)
            rotation = np.array(rotation) / np.pi * 180

            reLocate(mesh, location, rotation)

        bpy.context.scene.render.threads_mode = "FIXED"
        bpy.context.scene.render.threads = 16

        # save rendering
        if poseIdx >=  startIdx and poseIdx % 10 == 4:
            bt.renderImage(output_path, cam)
        print('rotation_euler', camera.rotation_euler)

    sourcecamLocation = np.array((3, 0, 2))
    targetcamLocation = np.array((0.2, 0.25, 1.0))

    sourcelookAtLocation = np.array((0, 0, 0.5)) # 同样需要调整
    targetlookAtLocation = np.array((0.2, 0.25, 0.5)) # 同样需要调整

    sourceAngle = cam.rotation_euler[2]
    targetAngle = sourceAngle + (50-90) * 1.0 / 180.0 * np.pi

    inter = 120
    for i in range(inter):
        if i < 70:
            continue
        camLocation = (i+1) / inter * (targetcamLocation - sourcecamLocation) + sourcecamLocation
        lookAtLocation = (i+1) / inter * (targetlookAtLocation - sourcelookAtLocation) + sourcelookAtLocation


        focalLength = 45  # (UI: click camera > Object Data > Focal Length)

        cam = bt.movCamera(cam, camLocation, lookAtLocation, focalLength)
        cam.rotation_euler[2] = (i+1) / inter * (targetAngle - sourceAngle) + sourceAngle
        output_path = os.path.join(imageOutputPath, '{}.png'.format(str(poseIdx + renderInter * (i)).rjust(7, '0')))
        bt.renderImage(output_path, cam)

    # 调整Z轴角度就可以了
    bpy.ops.wm.read_factory_settings(use_empty=True)