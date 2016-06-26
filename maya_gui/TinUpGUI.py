# tinDep.py

import maya.cmds as cmds
import os
from os import listdir
from os.path import isfile, join
import subprocess
import requests
import json

tinupPATH = os.environ['TINUP_PATH']
serverURL = "http://localhost:5000/"
scriptArray = []
connectionResponse = "Not tested"

def createUI(pWindowTitle, pApplyCallback, connectionResponse):
    windowID = 'myWindowID'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )

    cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[(1,150), (1,50), (1,100), (1,50), (1,100), (1,50), (1,100) ], columnOffset=[(5, 'right',1) ] )

    cmds.text( label='Tool Name')
    cmds.separator(height=40, width=50, style='none')
    cmds.text( label='Is Latest')
    cmds.separator(height=40, width=50, style='none')
    cmds.text( label='Positive Votes')
    cmds.separator(height=40, width=50, style='none')
    cmds.separator(h=10, style='none')

    # determine if your local commit is the latest
    def isLatestCallback(mayaScript):
        print 'local_commit_id: ' + mayaScript['local_commit_id']
        print 'latest_commit_id: ' + mayaScript['latest_commit_id']
        if (mayaScript['local_commit_id'] == mayaScript['latest_commit_id']):
            return "Yes"
        else:
            return "No"

    # create rows for each script in TINUP_PATH
    for mayaScript in scriptArray:
        cmds.text( label=mayaScript['name'])
        cmds.separator(height=10, width=50, style='none')
        cmds.text( label=isLatestCallback(mayaScript))
        cmds.separator(height=10, width=50, style='none')
        cmds.text( label=mayaScript['upvotePercentage'])
        cmds.separator(height=10, width=50, style='none')
        cmds.button(label='Upgrade', command=pApplyCallback )




    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.button(label='Apply', command=pApplyCallback )

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI( windowID )

    cmds.button (label='Cancel', command=cancelCallback)

    # see if you can connect to the server
    if (connectionResponse == "Hello World from TinUp!"):
        cmds.text(label="Status: Connected!")
    else:
        cmds.text(label="Status: Failure connecting...")



    cmds.showWindow()

def applyCallback(*pArgs) :
    print 'Apply button pressed.'

# used to compare the script you have
# against the one in the database
def compareScript(scriptName):
    print 'Checking backend with scriptName: ' + scriptName
    serverResponse = requests.get(serverURL + "script/" + scriptName).text
    resultDict = json.loads(serverResponse)  # result is now a dict
    # print serverResponse
    # print "----"
    # print resultJSON
    return resultDict


def loadScripts():
    global scriptArray
    for dirname in os.listdir(tinupPATH):
        # print path to all subdirectories first.
        print dirname
        print tinupPATH + "/" + dirname
        if (os.path.isdir(tinupPATH + "/" + dirname ) & os.path.isdir(tinupPATH + "/" + dirname + "/.git")):
            mayaToolRepo = tinupPATH + "/" + dirname
            command = "git status /Users/NathanBWaters/Library/Preferences/Autodesk/maya/2015-x64/scripts/TinUp/randomBoxes"
            # get commit id and timestamp
            try:
                osResp = subprocess.check_output("git rev-list --format=format:'%ci' --max-count=1 `git rev-parse HEAD`", cwd="/Users/NathanBWaters/Library/Preferences/Autodesk/maya/2015-x64/scripts/TinUp/randomBoxes", shell=True)
                osResp = osResp.split("\n")
                backendResp = compareScript(dirname)
                scriptArray.append( {'name' : dirname, 'local_commit_id': osResp[0], 'local_timestamp': osResp[1],
                    'latest_timestamp': backendResp['commit_timestamp'],
                    'committer': backendResp['committer'],
                    'point_of_contact' : backendResp['point_of_contact'],
                    'upvotePercentage' : backendResp['upvotePercentage'],
                    'latest_commit_id' : backendResp['commit_id'],
                    } )
                print scriptArray[-1]
            except subprocess.CalledProcessError as e:
                print(e)

def testConnectionCallback():
    connectionResponse = requests.get(serverURL).text
    return connectionResponse

loadScripts();
createUI('UpTin', applyCallback, testConnectionCallback())
