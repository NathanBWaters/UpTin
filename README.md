# UpTin
Continuous Deployment for Maya plugins.  



## Setting up UpTin

### Set up RDS PostgreSQL Database
* The database allows us to store pertinent information about our commits that Git doesn't store by itself - such as the likes and dislikes of the different versions by your Artists as well as comments.
* The python server will be communicating with the database and requires a connection with it in order to start. 
* Make sure your database is open on 5432 to your local computer as well as the instance the UpTin server will be hosted on.  Do this through your RDS security group settings.  
* Write down your Master Instance Identifier, Username, and Password, becuase you'll be setting your environment variables with them soon.

### Start server
* git clone https://github.com/NathanBWaters/UpTin
* cd UpTin
* export UPTIN_ID="<Your Master Instance Identifier>"
* export UPTIN_HOST="<RDS Endpoint without port>"
* export UPTIN_USERNAME="<Your Master Username>"
* export UPTIN_PASSWORD="<Your Master Password>"
* `sh server/setup.sh`
* `python server/UpTinServer.py` 

### Set up Jenkins 
* `docker run --rm -p 2222:2222 -p 8080:8080 -p 8081:8081 -p 9418:9418 -ti jenkinsci/workflow-demo`
* Sample code of what Jenkins should do
* 	~~~~
#!/bin/sh
echo "Started.  Now print the GIT_COMMIT" 
git clone https://github.com/NathanBWaters/randomBoxes
cd randomBoxes
curl -H "Content-Type: application/json" -X POST -d '{"github_url":"'"$GIT_URL"'", "latest_commit_id":"'"$GIT_COMMIT"'", "latest_commit_timestamp": "'"$(git log -1 --format=%cd --date=local)"'","latest_committer": "'"$GIT_COMMITTER_EMAIL"'","point_of_contact": "'"$GIT_AUTHOR_EMAIL"'","script_name":"randomBoxes"}' http://tinupserver.nathanwaters.io:8080/script
~~~~

### Set up GUI
* Put your custom plugins inside a folder located in your `/scripts` folder. For example, I put my scripts inside `/scripts/UpTin`.
* Set an UPTIN_PATH environment variable in your Maya.env file to point to your newly created folder.  The Maya.env file is how you can set environment variables for you MEL and Python scripts inside Maya. 
* Your Maya.env file is in:
  *  Mac: /Users/<user>/Library/Preferences/Autodesk/maya/<maya-version>
  *  Windows: <drive>:\Documents and Settings\<user>\My Documents\maya\<maya-version>
* Open Maya.  Open the script editor menu.
* Load the `maya_gui/UpTinGui.py` file from this repo into Maya. 
* Update the following line: `serverURL = "http://uptin-server.nathanwaters.io:8080/"` to point to your server.  
* Once you run the script, it will go through all of the git repositories inside your UPTIN_PATH folder and display them.  
* You now have the option to upvote, downvote, and update your scripts! 
* 



