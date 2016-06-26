# tinDep.py

import maya.cmds as cmds
import requests as req


connectionResponse = "Not tested"
url = "http://localhost:5000"
def createUI(pWindowTitle, pApplyCallback, testConnectionCallback):
    windowID = 'myWindowID'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )

    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,150), (2,150), (3,150) ], columnOffset=[(1, 'right',3) ] )

    cmds.text( label='Time Range: ')

    startTimeField = cmds.intField(value=cmds.playbackOptions(q=True, minTime=True))
    endTimeField = cmds.intField(value=cmds.playbackOptions(q=True, maxTime=True))

    cmds.text(label='Attribute')

    targetAttributeField = cmds.textField(text='rotateY')

    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')

    cmds.button(label='Apply', command=pApplyCallback )

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI( windowID )

    cmds.button (label='Cancel', command=cancelCallback)

    cmds.separator(h=30, style='none')
    cmds.separator(h=30, style='none')

    cmds.separator(h=30, style='none')
    cmds.separator(h=30, style='none')

    cmds.button (label='Test Connection', command=testConnectionCallback)
    print "connection response is " + connectionResponse
    targetAttributeField = cmds.textField(text=connectionResponse )

    cmds.showWindow()

def applyCallback(*pArgs) :
    print req.get("https://zm6dh2txl0.execute-api.us-west-2.amazonaws.com/prod/ping").text

def testConnectionCallback(*pArgs):
    global connectionResponse
    connectionResponse = req.get(url + "/").text
    print connectionResponse
    createUI('UpTin', applyCallback, testConnectionCallback)


createUI('UpTin', applyCallback, testConnectionCallback)
