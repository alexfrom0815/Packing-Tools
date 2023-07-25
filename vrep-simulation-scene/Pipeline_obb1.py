import os
import numpy as np
from simulation import vrep
import time
import bincutting_obb1 as boxes
import threading
from matplotlib import colors


class Robot(object):
    def __init__(self, connectIp, connectPort, objectMeshDir = '', objectNumber = 0, workspaceLimits = [[]],**kwargs):

        ### Connect
        self.ip   = connectIp
        self.port = connectPort

        ### Object
        ### Define colors for object meshes (Tableau palette)
        self.colorSpace = np.asarray([[78.0, 121.0, 167.0], # blue
                                       [89.0, 161.0, 79.0], # green
                                       [156, 117, 95], # brown
                                       [242, 142, 43], # orange
                                       [237.0, 201.0, 72.0], # yellow
                                       [186, 176, 172], # gray
                                       [255.0, 87.0, 51.0], # red
                                       [176, 122, 161], # purple
                                       [118, 183, 178], # cyan
                                       [255, 157, 167], # pink
                                       [0, 0, 0], # black
                                       [0, 0, 255], # pure blue
                                       [0, 255, 0], # pure green
                                       [255, 0, 0], # pure red
                                       [0, 255, 255], # pure cyan
                                       [255, 255, 0], # pure yellow
                                       [255, 0, 255], # magenta
                                       [255, 255, 255], # white
                                      ])/255.0

        ### Read files in object mesh directory
        self.objectMeshDir = objectMeshDir
        self.objectNumber = objectNumber
        try:
            self.meshList = os.listdir(self.objectMeshDir)
            ### Randomly choose objects to add to scene
            self.objectMeshIndex = np.random.randint(0, len(self.meshList), size=self.objectNumber)
            self.objectMeshColor = self.colorSpace[np.asarray(range(self.objectNumber)) % len(self.colorSpace), :]
        except:
            self.meshList = None
            if objectNumber == 0:
                self.cerr("Failed to read mesh, detected objectNumber = 0, no need to read mesh, you can ignore this warning", 1)
            else:
                self.cerr("Failed to read mesh, please check the objectMeshDir", 0)

        ### Workspace limits
        self.workspaceLimits = workspaceLimits

        self.targetName = kwargs['targetName']
        self.openParentObjectName = kwargs['openParentObjectName']
        self.closeParentObjectName = kwargs['closeParentObjectName']
        self.suckerName = kwargs['suckerName']

    def cerr(self, context, type):
        if type == 0:
            print("\033[1;31mError\033[0m: %s"%context)
        elif type == 1:
            print("\033[1;33mWarning\033[0m: %s"%context)

    # connect
    def connect(self):

        vrep.simxFinish(-1)  # close all opened connections
        self.clientID = vrep.simxStart(self.ip, self.port, True, True, 3000, 5)
        ### Connect to V-REP
        if self.clientID == -1:
            import sys
            sys.exit('\nV-REP remote API server connection failed (' + self.ip + ':' +
                     str(self.port) + '). Is V-REP running?')
        else:
            print('V-REP remote API server connection success')
        return

    def disconnect(self):

        ### Make sure that the last command sent has arrived
        vrep.simxGetPingTime(self.clientID)
        ### Now close the connection to V-REP:
        vrep.simxFinish(self.clientID)
        return

    def listDistance(self, src, tar):
        return np.sqrt((src[0]-tar[0])**2 + (src[1]-tar[1])**2 + (src[2]-tar[2])**2)

    def start(self):

        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)
        print('''==========================================\n========== simulation start ==============\n==========================================\n''')

    def stop(self):

        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)
        print('''==========================================\n========== simulation stop ===============\n==========================================\n''')

    def restart(self):

        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)
        print('''==========================================\n========== simulation stop ===============\n==========================================\n''')
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)
        print('''==========================================\n========== simulation start ==============\n==========================================\n''')


    def createPureShape(self, toolShape, targetPosition, mass = 0.01):

        # the name of the scene object where the script is attached to, or an empty string if the script has no associated scene object
        scriptDescription = 'remoteApiCommandServer'
        # the name of the Lua function to call in the specified script

        retResp, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(self.clientID, scriptDescription, vrep.sim_scripttype_childscript,
                            'CreatePureShape',
                            [],
                            [toolShape[0], toolShape[1], toolShape[2], targetPosition[0], targetPosition[1], targetPosition[2], mass],
                            [],
                            bytearray(),
                            vrep.simx_opmode_blocking)
        return retInts[0]

    def setColor(self,objHandle,color):
        scriptDescription = 'remoteApiCommandServer'
        retResp, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(self.clientID, scriptDescription, vrep.sim_scripttype_childscript,
                            'SetColor',
                            [objHandle],
                            color,
                            [],
                            bytearray(),
                            vrep.simx_opmode_blocking)


    def untilReach(self,tar, targetHandle):
        pass
        time.sleep(0.08)
        # simRet, targetPosition = vrep.simxGetObjectPosition(self.clientID, targetHandle, -1, vrep.simx_opmode_blocking)
        # print('targetPosition:', targetPosition)
        # while True:
        #     simRet, currPosition = vrep.simxGetObjectPosition(self.clientID, targetHandle, -1,
        #                                                         vrep.simx_opmode_blocking)
        #     simRet, targetPosition = vrep.simxGetObjectPosition(self.clientID, targetHandle, -1, vrep.simx_opmode_blocking)
        #     print('targetPosition:', targetPosition)
        #     if self.listDistance(currPosition, tar) < 1e-3:
        #         break

    ### move and gripper
    def move(self, targetName, toolPosition, toolOrientation, moveSpeed=50, turnSpeed=50,sleepTime = 0.04):
        while True:
            simRet, targetPosition = vrep.simxGetObjectPosition(self.clientID, self.targetHandle,-1,vrep.simx_opmode_blocking)
            # print([simRet, targetPosition])
            if simRet == 0:
                break

        simRet, targetOrientation = vrep.simxGetObjectOrientation(self.clientID, self.targetHandle,-1,vrep.simx_opmode_blocking)
        originPosition = targetPosition

        if toolPosition != None:
            moveDirection = np.asarray([toolPosition[0] - originPosition[0], toolPosition[1] - originPosition[1], toolPosition[2] - originPosition[2]])
            moveMagnitude = np.linalg.norm(moveDirection)
            moveStep = 1 / moveSpeed * moveDirection / moveMagnitude
            moveStepNumber = int(np.floor(moveMagnitude * moveSpeed))

            for stepIter in range(moveStepNumber):
                tempTarget = [originPosition[0] + moveStep[0] * (stepIter + 1),
                              originPosition[1] + moveStep[1] * (stepIter + 1),
                              originPosition[2] + moveStep[2] * (stepIter + 1)]

                vrep.simxSetObjectPosition(self.clientID, self.targetHandle, -1, tempTarget, vrep.simx_opmode_blocking)
                self.untilReach(tempTarget, self.targetHandle)

            vrep.simxSetObjectPosition(self.clientID, self.targetHandle, -1, (toolPosition[0], toolPosition[1], toolPosition[2]), vrep.simx_opmode_blocking)

        if toolOrientation != None:
            turnDirection = np.asarray([toolOrientation[0] - targetOrientation[0], toolOrientation[1] - targetOrientation[1], toolOrientation[2] - targetOrientation[2]])
            turnMagnitude = np.linalg.norm(turnDirection)
            turnStep = 1 / turnSpeed * turnDirection / turnMagnitude
            turnStepNumber = int(np.floor(turnMagnitude * turnSpeed))

            for stepIter in range(turnStepNumber):
                ### turn
                vrep.simxSetObjectOrientation(self.clientID, self.targetHandle, -1, (targetOrientation[0] + turnStep[0], targetOrientation[1] + turnStep[1], targetOrientation[2] + turnStep[2]), vrep.simx_opmode_blocking)
                simRet, targetOrientation = vrep.simxGetObjectOrientation(self.clientID, self.targetHandle, -1, vrep.simx_opmode_blocking)
            vrep.simxSetObjectOrientation(self.clientID, self.targetHandle, -1, (toolOrientation[0], toolOrientation[1], toolOrientation[2]), vrep.simx_opmode_blocking)

    def openSucker(self, objectName, parentObjectName):
        simRet, objectHandle = vrep.simxGetObjectHandle(self.clientID, objectName, vrep.simx_opmode_blocking)
        simRet, parentObject = vrep.simxGetObjectHandle(self.clientID, parentObjectName, vrep.simx_opmode_blocking)
        for _ in range(10):
            flag = vrep.simxSetObjectParent(self.clientID, objectHandle, parentObject, True, vrep.simx_opmode_blocking)
            if flag == 0:
                break
        time.sleep(0.01)

    def closeSucker(self, objectName, parentObjectName):
        simRet, objectHandle = vrep.simxGetObjectHandle(self.clientID, objectName, vrep.simx_opmode_blocking)
        simRet, parentObject = vrep.simxGetObjectHandle(self.clientID, parentObjectName, vrep.simx_opmode_blocking)
        for _ in range(10):
            flag = vrep.simxSetObjectParent(self.clientID, objectHandle, parentObject, False, vrep.simx_opmode_blocking)
            if flag == 0:
                break
        time.sleep(0.01)

    def robotInit(self):
        simRet, self.targetHandle = vrep.simxGetObjectHandle(self.clientID, self.targetName, vrep.simx_opmode_blocking)
        simRet, tipHandle = vrep.simxGetObjectHandle(self.clientID, tipName, vrep.simx_opmode_blocking)
        simRet, tipPosition = vrep.simxGetObjectPosition(self.clientID, tipHandle, -1, vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(self.clientID, self.targetHandle, -1, tipPosition, vrep.simx_opmode_blocking)

        self.forwarder = vrep.simxGetObjectHandle(self.clientID, 'customizableConveyor_forwarder', vrep.simx_opmode_blocking)[1]
        simRet, currentSensor = vrep.simxGetObjectHandle(self.clientID, 'Current', vrep.simx_opmode_blocking)
        simRet, previewSensor = vrep.simxGetObjectHandle(self.clientID, 'Preview', vrep.simx_opmode_blocking)
        simRet, self.currentSensorPosition = vrep.simxGetObjectPosition(self.clientID, currentSensor, -1, vrep.simx_opmode_blocking)
        simRet, self.previewSensorPosition = vrep.simxGetObjectPosition(self.clientID, previewSensor, -1, vrep.simx_opmode_blocking)

    def dropIt(self,currPosition, targetPosition, box, boxHandle, maxHeight):
        self.move(self.targetName, [currPosition[0], currPosition[1], 0.35], None)

        print('question:',[currPosition[0], currPosition[1], 0.01 + box[2] - 0.09])
        self.move(self.targetName, [currPosition[0], currPosition[1], 0.01 + box[2] - 0.09],None)
        # self.move(self.targetName, [currPosition[0], currPosition[1], maxHeight + 0.1],None)
        self.move(self.targetName, [-0.375, -0.575, maxHeight + 0.1],None)


        self.move(self.targetName, [targetPosition[0], targetPosition[1], maxHeight + 0.1], None)
        self.move(self.targetName, [targetPosition[0], targetPosition[1], targetPosition[2] + box[2] * 0.5 - 0.09 + 0.01], None)

        if targetPosition[2] + box[2] * 0.5 > maxHeight:
            maxHeight = targetPosition[2] + box[2] * 0.5

        self.closeSucker(self.suckerName, self.closeParentObjectName)
        self.setColor(boxHandle, color=colors.hex2color(colors.cnames['lightskyblue']))
        self.move(self.targetName, [targetPosition[0], targetPosition[1], maxHeight + 0.1], None)
        self.openSucker(self.suckerName, self.openParentObjectName)
        # self.setColor(boxHandle,)
        simRet, currPosition = vrep.simxGetObjectPosition(self.clientID, boxHandle, -1, vrep.simx_opmode_blocking)
        # print('currPosition2: ', currPosition, 'lossX: %.3f' % (targetPosition[0] - currPosition[0]),
        #       'lossY: %.3f' % (targetPosition[1] - currPosition[1]))
        return maxHeight

    def clearBox(self, handleList):
        for boxHandle in handleList:
            vrep.simxRemoveObject(self.clientID, boxHandle, vrep.simx_opmode_blocking)

    def resetGame(self, handleList):
        self.clearBox(handleList)
        handleList = []
        self.boxLocation = []
        self.boxShape = []



### connect demo
connectIp = '127.0.0.1'
connectPort = 19997

objectMeshDir = 'objects/blocks'
objectNumber = 10

targetName = 'Target'
tipName = 'Tip'
openCloseJointName = 'RG2_openCloseJoint'
speed = 0.02

objectName = 'suctionPadLoopClosureDummy1'
closeParentObjectName = 'suctionPadLink'
openParentObjectName = 'suctionPad'

# add cuboid
boxes = boxes.newBoxs
boxesNum = 0
for box in boxes:
    if box[3] != -1:
        boxesNum+=1
loss = 0.0

# Cols: min max, Rows: x y z (define workspace limits in robot coordinate)
workspaceLimits = np.asarray([[-0.724, -0.276], [-0.224, 0.224], [-0.0001, 0.4]])

robot = Robot(connectIp, connectPort, objectMeshDir, objectNumber, workspaceLimits,suckerName = objectName,
              openParentObjectName = openParentObjectName, closeParentObjectName = closeParentObjectName, targetName = targetName)

robot.connect()
robot.robotInit()

### start stop restart demo
robot.start()
simRet, tipHandle = vrep.simxGetObjectHandle(robot.clientID, tipName, vrep.simx_opmode_blocking)
simRet, tipPosition = vrep.simxGetObjectPosition(robot.clientID, tipHandle, -1, vrep.simx_opmode_blocking)
tipPosition[0] = tipPosition[0] + 0.2
vrep.simxSetObjectPosition(robot.clientID, robot.targetHandle, -1, tipPosition, vrep.simx_opmode_blocking)


nameList = [] # global
targetposition_list = [] # global
handleList = []
initX = 2.8
toPack = 0

# 着色可以在这里写
def addBox():
    toProduce = 0
    boxHandle  = None
    lastPosition = [0, 0, 0]  # global

    toColorList = []
    global targetposition_list
    global nameList
    global handleList

    toColorHandle = None

    while True:
        time.sleep(0.13)

        if boxHandle is not None:
            simRet, lastPosition = vrep.simxGetObjectPosition(robot.clientID, boxHandle, -1, vrep.simx_opmode_blocking)

        if (toProduce == 0 or (abs(lastPosition[0] - initX) > 0.3 and abs(lastPosition[0] - initX) <1)) and toProduce < len(boxes):
            if lastPosition[0] == 0 and toProduce!=0:
                continue

            shape = [boxes[toProduce][0], boxes[toProduce][1], boxes[toProduce][2]]
            targetPosition = [boxes[toProduce][3] + boxes[toProduce][0] * 0.5, boxes[toProduce][4] + boxes[toProduce][1] * 0.5, boxes[toProduce][5] + boxes[toProduce][2] * 0.5]
            targetposition_list.append(targetPosition)

            initPosition = [initX, -0.85, 0.01 + boxes[toProduce][2] / 2]
            scaling = 0.93
            boxHandle = robot.createPureShape([shape[0] * scaling, shape[1] * scaling, shape[2]], initPosition)
            boxName = 'Cuboid' if toProduce == 0 else 'Cuboid{}'.format(toProduce - 1)
            nameList.append(boxName)
            handleList.append(boxHandle)
            toColorList.append(boxHandle)
            # robot.setColor(boxHandle, color=colors.hex2color(colors.cnames['pink']))
            toProduce += 1

        print('toProduce:', toProduce)
        if toProduce >= len(boxes):
            break

t = threading.Thread(target=addBox)
t.start()

beltStop = False
time.sleep(0.5)

maxHeight = 0
lastPostion = None
while True:
    time.sleep(0.1)
    singnal = False
    if len(handleList) == 0:
        continue
    else:
        curr = handleList[toPack]

    simRet, currPosition = vrep.simxGetObjectPosition(robot.clientID, curr, -1, vrep.simx_opmode_blocking)
    if abs(currPosition[0] - robot.currentSensorPosition[0]) > 0.2:
        continue

    if lastPostion is not None:
        if abs(currPosition[0] - lastPostion[0]) <= 1e-3 and np.sum(currPosition)!=0:
            singnal = True

    lastPostion = currPosition


    if singnal:
        targetPosition = targetposition_list[toPack]
        curr = handleList[toPack]
        for _ in range(10):
            simRet, currPosition = vrep.simxGetObjectPosition(robot.clientID, curr, -1, vrep.simx_opmode_blocking)
            print([toPack,simRet,currPosition])
            if abs(currPosition[0] - robot.currentSensorPosition[0]) <= 0.2:
                break

        maxHeight = robot.dropIt(currPosition, targetPosition, boxes[toPack], curr, maxHeight)

        print(maxHeight)

        toPack += 1
        lastPostion = None

    if toPack >= boxesNum:
        break

