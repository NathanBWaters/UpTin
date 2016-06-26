from flask import Flask, Response
import flask
import psycopg2 as db
import os
import boto3
import json


# Let's use Amazon S3
s3 = boto3.resource('s3')

db_conn= None

def test():
    for bucket in s3.buckets.all():
        print(bucket.name)

# connection to PostgreSQL RDS database
def connect_db():
    print os.environ['TINUP_HOST']
    print os.environ['TINUP_USERNAME']
    print os.environ['TINUP_PASSWORD']
    host = os.environ['TINUP_HOST']
    username = os.environ['TINUP_USERNAME']
    password =  os.environ['TINUP_PASSWORD']
    global db_conn
    db_conn= db.connect("host='tinup-instance.c6bsisktzdvp.us-west-2.rds.amazonaws.com' dbname='postgres' user='TinUp_Username' password='TinUp_Password'")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from TinUp!"

def calculateVotePercentage(upvotes, downvotes):
    if (downvotes == 0): # we do not want to divide by 0
        return '100.00%'
    else: # should return a stringified float like 95.42%
        return str(upvotes / (upvotes + float(downvotes)) * 100)[0:5] + "%"



@app.route("/script/<script_name>/<commit_id>", methods=['GET'])
def getScript(script_name, commit_id):
    cursor = db_conn.cursor()

    print 'script_name is ' + script_name
    print 'commit_id is ' + commit_id

    # get information for local script and commit_id
    cursor.execute("SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON (ms.script_id = sv.script_id) WHERE (ms.script_name=%s) AND (sv.commit_id = %s);", [script_name, commit_id])
    localScript = cursor.fetchone()
    print ("localScript: " + str(localScript))
    localUpvotePercentage = calculateVotePercentage(localScript[9], localScript[10])

    # get information for latest version of script
    cursor.execute("SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON (ms.script_id = sv.script_id) WHERE (ms.script_name=%s) ORDER BY sv.script_version_id DESC LIMIT 1;", [script_name])
    latestScript = cursor.fetchone()
    print ("latestScript: " + str(latestScript))
    latestUpvotePercentage = calculateVotePercentage(latestScript[9], latestScript[10])

    data = json.dumps({
        'script_name': localScript[1],
        'point_of_contact': localScript[2],
        'github_url': localScript[3],
        'local_committer': localScript[6],
        'local_commit_id': localScript[7],
        'local_commit_timestamp': localScript[8],
        'local_upvote_percentage': localUpvotePercentage,
        'latest_committer': latestScript[6],
        'latest_commit_id': latestScript[7],
        'latest_commit_timestamp': latestScript[8],
        'latest_upvote_percentage': latestUpvotePercentage,
        'is_latest': localScript[7] == latestScript[7]
        }, sort_keys=True,
        indent=4, separators=(',', ': '))

    return Response(response=data,
    status=200, \
    mimetype="application/json")


if __name__ == "__main__":
    # test()
    connect_db()
    app.run()
