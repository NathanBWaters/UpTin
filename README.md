# UpTin
Continuous Deployment for Maya plugins.  

![UpTin Menu](https://raw.githubusercontent.com/NathanBWaters/UpTin/master/documentation/uptin-menu.png "UpTin Menu")


### See it in Action!
[https://vimeo.com/172483275](https://vimeo.com/172483275)

## Setting up UpTin

### Set up RDS PostgreSQL Database
* The database allows us to store pertinent information about our commits that Git doesn't store by itself - such as the likes and dislikes of the different versions by your Artists as well as comments.
* The python server will be communicating with the database and requires a connection with it in order to start. 
* Make sure your database is open on 5432 to your local computer as well as the instance the UpTin server will be hosted on.  Do this through your RDS security group settings.  
![SecGroup](https://raw.githubusercontent.com/NathanBWaters/UpTin/master/documentation/security-group2.png "SecGroup")
* Write down your Master Instance Identifier, Username, and Password, becuase you'll be setting your environment variables with them soon.
![RDS Form](https://raw.githubusercontent.com/NathanBWaters/UpTin/master/documentation/rds-form.png "RDS Form")
* Connect to the database using pgAdmin3 and open schema.sql in this repository.  Run the schema to begin populating your RDS PostgreSQL instance.
![Schema](https://raw.githubusercontent.com/NathanBWaters/UpTin/master/documentation/uptin-schema.png "Schema")

### Start server
* The server is what your Maya plugin communicates with.  It has two main endpoints
 * `POST` `/script`  You must post a JSON with the following information 
~~~~
{
    "github_url": "a2342444aa",
    "latest_commit_id": "4bc92a8437445442c4b55a774b96df5973e9a7",
    "latest_commit_timestamp": "2016-09-26 12:07:28",
    "latest_committer": "fakeemail @ yahoo.com",
    "point_of_contact": "fakeemail @ yahoo.com",
    "script_name": "randomSpheres5"
}
~~~~

 * `GET` `/script/{script_name}/{commit_id}`
  * This will return all of the necessary information about your script, including whether or not it's the latest version of the script.
~~~~
   {
    "github_url": "https://github.com/NathanBWaters/randomSpheres",
    "is_latest": false,
    "latest_commit_id": "02f3c9750b492c0cbab6d732efff4cdbbbf0ba77",
    "latest_commit_timestamp": "Mon Jun 27 03:24:04 2016",
    "latest_committer": "",
    "latest_upvote_percentage": "100.00%",
    "local_commit_id": "d7fb6bde8fe16a54ec86030a6701661dc0b8c819",
    "local_commit_timestamp": "2016-06-26 15:01:28",
    "local_committer": "fakeemail @ yahoo.com",
    "local_upvote_percentage": "34.21%",
    "point_of_contact": "fakeemail @ yahoo.com",
    "script_name": "randomSpheres",
    "status": "success"
  }
~~~~

* git clone https://github.com/NathanBWaters/UpTin
* cd UpTin
* export UPTIN_ID="Your Master Instance Identifier"
* export UPTIN_HOST="RDS Endpoint without port"
* export UPTIN_USERNAME="Your Master Username"
* export UPTIN_PASSWORD="Your Master Password"
* `sh server/setup.sh`
* `python server/UpTinServer.py` 

### Set up Jenkins 

![Jenkins Trigger](https://raw.githubusercontent.com/NathanBWaters/UpTin/master/documentation/jenkins-trigger.png "Jenkins Trigger")

* `docker run --rm -p 2222:2222 -p 8080:8080 -p 8081:8081 -p 9418:9418 -ti jenkinsci/workflow-demo`
* ![alt text][documentation/jenkins-trigger.png]
* Sample code of what Jenkins should do
~~~~
#!/bin/sh
git clone https://github.com/NathanBWaters/randomBoxes
cd randomBoxes
#####################
## This is where you run your tests
#####################

# If it passed your tests, push the git commit information to your server
# This curl request is hitting the `POST` `/script` endpoint of your server
# You will have to update multiple variables in this command, but the GIT environment variables should be present thanks to Jenkins Git Plugin.  
curl -H "Content-Type: application/json" -X POST -d '{"github_url":"'"$GIT_URL"'", "latest_commit_id":"'"$GIT_COMMIT"'", "latest_commit_timestamp": "'"$(git log -1 --format=%cd --date=local)"'","latest_committer": "'"$GIT_COMMITTER_EMAIL"'","point_of_contact": "'"$GIT_AUTHOR_EMAIL"'","script_name":"randomBoxes"}' http://tinupserver.nathanwaters.io:8080/script
~~~~

### Set up GUI
* Put your custom plugins inside a folder located in your `/scripts` folder. For example, I put my scripts inside `/scripts/UpTin`.
* Set an UPTIN_PATH environment variable in your Maya.env file to point to your newly created folder.  The Maya.env file is how you can set environment variables for you MEL and Python scripts inside Maya. 
* Your Maya.env file is in:
  *  Mac: /Users/{user}/Library/Preferences/Autodesk/maya/{maya-version}
  *  Windows: {drive}:\Documents and Settings\{user}\My Documents\maya\{maya-version}
* Open Maya.  Open the script editor menu.
* Load the `maya_gui/UpTinGui.py` file from this repo into Maya. 
* Update the following line: `serverURL = "http://uptin-server.nathanwaters.io:8080/"` to point to your server.  
* Once you run the script, it will go through all of the git repositories inside your UPTIN_PATH folder and display them.  
* You now have the option to upvote, downvote, and update your scripts! 


