# tinDep.py

import maya.cmds as cmds
import os
from os import listdir
from os.path import isfile, join
import subprocess
import requests
import json
from functools import partial

upTinPATH = os.environ['UPTIN_PATH']
serverURL = "http://tinupserver.nathanwaters.io:8080/"
scriptArray = []
connectionResponse = "Not tested"

def createUI(pWindowTitle, pApplyCallback, connectionResponse):
    windowID = 'myWindowID'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )

    cmds.rowColumnLayout(numberOfColumns=9, columnWidth=[(1,250), (1,50), (1,100), (1,50), (1,100), (1,50), (1,100) ], columnOffset=[(5, 'right',1) ] )

    cmds.text( label='Tool Name')
    cmds.text( label='Timestamp')
    cmds.text( label='Is Latest')
    cmds.separator(height=40, width=50, style='none')
    cmds.text( label='Positive Votes')
    cmds.separator(height=40, width=50, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')


    # used to submit an upvote
    def postUpvote(script_name, commit_id, args):
        print "Called upvote on " + script_name


    # used to submit a downvote
    def postDownvote(script_name, commit_id, args):
        print "Called downvote on " + script_name

    # user requests to update Maya script to newest code
    def updateCode(script_name, args):
        print "Called updateCode on " + script_name


    def separateScripts():
        # fill lack of update button
        cmds.separator(height=10, width=50, style='none')

        # dashes to separate
        cmds.text( label="---------------------")
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')
        cmds.separator(height=10, width=50, style='none')

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

        cmds.text( label=mayaScript['script_name'])
        cmds.text( label=mayaScript['local_commit_timestamp'])
        cmds.text( label=mayaScript['is_latest'])
        cmds.separator(height=10, width=50, style='none')
        cmds.text( label=mayaScript['local_upvote_percentage'])
        cmds.separator(height=10, width=50, style='none')

        cmds.button(label='Upvote', command=partial(postUpvote, mayaScript['script_name'], mayaScript['local_commit_id']))
        cmds.button(label='Downvote', command=partial(postDownvote, mayaScript['script_name'], mayaScript['local_commit_id']))
        if (mayaScript['is_latest'] == False):
            # provide upgrade button!
            cmds.button(label='Get Latest', command=partial(udpateCode, mayaScript['script_name']) )

            # input information about latest version of the script
            cmds.text( label="  -- latest")
            cmds.text( label=mayaScript['latest_commit_timestamp'])
            cmds.separator(height=10, width=50, style='none')
            cmds.separator(height=10, width=50, style='none')
            cmds.text( label=mayaScript['latest_upvote_percentage'])
            cmds.separator(height=10, width=50, style='none')

        else:
            separateScripts()

    cmds.separator(height=10, width=50, style='none')
    cmds.separator(height=10, width=50, style='none')
    separateScripts()

    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

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
def getScriptInfo(scriptName, commit_id):

    url = serverURL + "script/" + scriptName + "/" + commit_id
    print 'Checking backend with scriptName: ' + scriptName + "\n and url: " + url
    serverResponse = requests.get(url).text
    resultDict = json.loads(serverResponse)  # result is now a dict
    return resultDict



def loadScripts():
    global scriptArray
    for dirname in os.listdir(upTinPATH):
        # print path to all subdirectories first.
        print dirname
        print upTinPATH + "/" + dirname
        if (os.path.isdir(upTinPATH + "/" + dirname ) & os.path.isdir(upTinPATH + "/" + dirname + "/.git")):
            mayaToolRepo = upTinPATH + "/" + dirname
            # get commit id and timestamp
            try:
                osResp = subprocess.check_output("git rev-list --format=format:'%ci' --max-count=1 `git rev-parse HEAD`", cwd=mayaToolRepo, shell=True)
                local_timestamp = osResp.split("\n")[1]
                local_commit_id = subprocess.check_output("git log --format='%H' -n 1", cwd=mayaToolRepo, shell=True).strip()
                print local_commit_id
                print local_timestamp
                backendResp = getScriptInfo(dirname, local_commit_id )
                scriptArray.append(backendResp)
                print scriptArray[-1]
            except subprocess.CalledProcessError as e:
                print(e)

def testConnectionCallback():
    connectionResponse = requests.get(serverURL).text
    return connectionResponse


loadScripts();
createUI('UpTin', applyCallback, testConnectionCallback())
