from flask import Flask
import psycopg2 as db
import os

# connection to PostgreSQL RDS database


conn = None

def connect_db():
    print os.environ['TINUP_HOST']
    print os.environ['TINUP_USERNAME']
    print os.environ['TINUP_PASSWORD']
    host = os.environ['TINUP_HOST']
    username = os.environ['TINUP_USERNAME']
    password =  os.environ['TINUP_PASSWORD']
    global conn
    conn = db.connect("host='tinup-instance.c6bsisktzdvp.us-west-2.rds.amazonaws.com' dbname='postgres' user='TinUp_Username' password='TinUp_Password'")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from TinUp!"

if __name__ == "__main__":
    connect_db()
    app.run()
