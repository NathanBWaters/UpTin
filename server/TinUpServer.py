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


@app.route("/script/<script_name>", methods=['GET'])
def getScript(script_name):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON (ms.script_id = sv.script_id) WHERE ms.script_name = %s;", [script_name])

    response = cursor.fetchone()


    if (response[10] == 0): # we do not want to divide by 0
        upvotePercentage = '100.00%'
    else: # should return a stringified float like 95.42%
        upvotePercentage = str(response[9] / (response[9] + float(response[10])) * 100)[0:5] + "%"

    print upvotePercentage

    data = json.dumps({'script_name': response[1], 'point_of_contact': response[2],
        'github_url': response[3], 'committer': response[6], 'commit_id': response[7],
        'commit_timestamp': response[8], 'upvotePercentage': upvotePercentage}, sort_keys=True,
        indent=4, separators=(',', ': '))

    response = Response(response=data,
    status=200, \
    mimetype="application/json")

    return response

if __name__ == "__main__":
    # test()
    connect_db()
    app.run()
