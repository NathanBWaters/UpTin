#randomBoxes.py

import maya.cmds as cmds
import random

random.seed( 1234 )

cubeList = cmds.ls('myCube*')

if len(cubeList) > 0:
    cmds.delete( cubeList )

result = cmds.polySphere( radius=1, name='myCube#')

print 'result: ' + str(result)

transformName = result[0]

instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#')

for i in range(0, 50):
    instanceResult = cmds.instance( transformName, name=transformName + '_instance#')
    print 'instanceResult' + str(instanceResult)
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    z = random.uniform(-10, 10)
    cmds.move(x,y,z,instanceResult)

    cmds.parent(instanceResult, instanceGroupName)

    xRot = random.uniform(0,360)
    yRot = random.uniform(0,360)
    zRot = random.uniform(0,360)

    cmds.rotate(xRot,yRot,zRot, instanceResult)

    scalingFactor = random.uniform(0.3, 1.5)

    cmds.scale(scalingFactor, scalingFactor,scalingFactor, instanceResult)


cmds.hide(transformName)
