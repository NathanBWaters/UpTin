# tinDep.py

import maya.cmds as cmds
import os
from os import listdir
from os.path import isfile, join
import subprocess

tinupPATH = os.environ['TINUP_PATH']
serverURL = "http://localhost:5000"
scriptArray = []

def createUI(pWindowTitle, pApplyCallback):
    windowID = 'myWindowID'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )

    cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1,150), (1,100), (1,100), (1,100), (1,100) ], columnOffset=[(1, 'left',1), (5, 'right',1) ] )

    cmds.text( label='Tool Name')
    cmds.text( label='Description')
    cmds.text( label='Is Latest')
    cmds.text( label='Positive Votes')
    cmds.separator(h=10, style='none')

    # create rows for each script in TINUP_PATH
    for mayaScript in scriptArray:
        cmds.text( label=mayaScript['name'])
        cmds.text( label='temp')
        cmds.text( label='yes')
        cmds.text( label='90%')
        cmds.button(label='Upgrade', command=pApplyCallback )




    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.button(label='Apply', command=pApplyCallback )

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI( windowID )

    cmds.button (label='Cancel', command=cancelCallback)

    cmds.showWindow()

def applyCallback(*pArgs) :
    print 'Apply button pressed.'

def loadScripts():
    global scriptArray
    for dirname in os.listdir(tinupPATH):
        # print path to all subdirectories first.
        print dirname
        print tinupPATH + "/" + dirname
        if (os.path.isdir(tinupPATH + "/" + dirname ) & os.path.isdir(tinupPATH + "/" + dirname + "/.git")):
            print "It's a github directory!"
            mayaToolRepo = tinupPATH + "/" + dirname
            command = "git status /Users/NathanBWaters/Library/Preferences/Autodesk/maya/2015-x64/scripts/TinUp/randomBoxes"
            # get commit id and timestamp
            try:
                osResp = subprocess.check_output("git rev-list --format=format:'%ci' --max-count=1 `git rev-parse HEAD`", cwd="/Users/NathanBWaters/Library/Preferences/Autodesk/maya/2015-x64/scripts/TinUp/randomBoxes", shell=True)
                osResp = osResp.split("\n")
                scriptArray.append( {'name' : dirname, 'commit_id': osResp[0], 'timestamp': osResp[1]} )
                print scriptArray[-1]
            except subprocess.CalledProcessError as e:
                print(e)


loadScripts();
createUI('UpTin', applyCallback)
