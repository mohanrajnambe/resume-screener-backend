from flask import Flask
app = Flask(__name__)

@app.route("/")
def main(event, context):
    return "Home is under construction!"

@app.route("/test")
def test(event, context):
    return "Test Api is working good!"
