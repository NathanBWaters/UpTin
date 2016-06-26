from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "You are connected to the TinUp server!"

if __name__ == "__main__":
    app.run()
