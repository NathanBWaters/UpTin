from flask import Flask, Response, request
import flask
import psycopg2 as db
import os
import json

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


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
@crossdomain(origin='*')
def hello():
    return "Hello World from TinUp!"

def calculateVotePercentage(upvotes, downvotes):
    if (downvotes == 0): # we do not want to divide by 0
        return '100.00%'
    else: # should return a stringified float like 95.42%
        return str(upvotes / (upvotes + float(downvotes)) * 100)[0:5] + "%"

# called only from Jenkins
# will add a script from new or append a new version
# you must pass a JSON with the script information
@app.route("/script", methods=['POST'])
@crossdomain(origin='*')
def postScript():
    cursor = db_conn.cursor()

    content = json.loads(request.data)
    print content

    script_name = content["script_name"]
    point_of_contact = content["point_of_contact"]
    github_url = content["github_url"]
    latest_committer = content["latest_committer"]
    latest_commit_timestamp = content["latest_commit_timestamp"]
    latest_commit_id = content["latest_commit_id"]


    # see if the script already exists
    cursor.execute("SELECT * from maya_scripts AS ms WHERE (ms.script_name=%s);", [script_name, ])

    script_id = None
    row = cursor.fetchone()

    if (row == None):  # it does not exist
        # create row in maya_scripts table and return newly created script_id
        try:
            cursor.execute("INSERT INTO maya_scripts (script_name, point_of_contact, \
            github_url) VALUES (%s, %s, %s) RETURNING script_id;", [script_name, point_of_contact, github_url]);
        except db.Error as e:
            db_conn.commit()
            data = json.dumps({
                'status': 'failure',
                'message': str(e)
                }, sort_keys=True,
                indent=4, separators=(',', ': '))
            return Response(response=data,
            status=500, \
            mimetype="application/json")

        script_id = cursor.fetchone()[0]



    else: # the script is already in the database.  Let's add a new version of an existing script
        print "new version of existing script"
        script_id = row[0]

    # add in version of script into script_versions table
    try:
        cursor.execute("INSERT INTO script_versions (script_id, committer, commit_id, \
            commit_timestamp, upvotes, downvotes) VALUES \
            (%s, %s, %s, %s, %s, %s);", [script_id, latest_committer, latest_commit_id,
            latest_commit_timestamp, 0, 0]);
    except db.Error as e:
        db_conn.commit()
        data = json.dumps({
            'status': 'failure',
            'message': str(e)
            }, sort_keys=True,
            indent=4, separators=(',', ': '))

        return Response(response=data,
        status=500, \
        mimetype="application/json")

    # close connection
    db_conn.commit()

    data = json.dumps({
        'status': 'success'
        }, sort_keys=True,
        indent=4, separators=(',', ': '))

    return Response(response=data,
    status=200, \
    mimetype="application/json")



@app.route("/script/<script_name>/<commit_id>", methods=['GET'])
@crossdomain(origin='*')
def getScript(script_name, commit_id):
    cursor = db_conn.cursor()

    print 'script_name is ' + script_name
    print 'commit_id is ' + commit_id

    # get information for local script and commit_id
    cursor.execute("SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON \
        (ms.script_id = sv.script_id) WHERE (ms.script_name=%s) AND (sv.commit_id = %s);", [script_name, commit_id])
    localScript = cursor.fetchone()
    print ("localScript: " + str(localScript))
    localUpvotePercentage = calculateVotePercentage(localScript[9], localScript[10])

    # get information for latest version of script
    cursor.execute("SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON \
        (ms.script_id = sv.script_id) WHERE (ms.script_name=%s) ORDER BY sv.script_version_id DESC LIMIT 1;", [script_name])
    latestScript = cursor.fetchone()
    print ("latestScript: " + str(latestScript))
    latestUpvotePercentage = calculateVotePercentage(latestScript[9], latestScript[10])

    data = json.dumps({
        'status': 'success',
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

    # stop blocking connection
    db_conn.commit()

    return Response(response=data,
    status=200, \
    mimetype="application/json")


if __name__ == "__main__":
    # test()
    connect_db()
    app.run('0.0.0.0', 8080)
