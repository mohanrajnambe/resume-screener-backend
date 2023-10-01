from flask import Flask, request
import json
import cron.process_resume as pr

app = Flask(__name__)

@app.route("/")
def main():
    # Getting request body
    # body = request.get_data()
    return "Home is under construction!"

@app.route("/test")
def test():
    return "Test Api is working good!"


@app.route("/process-resume", methods=['POST'])
def processResume():
    pr.run()
    return "Resume Processed"