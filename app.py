from flask import Flask
import cron.process_resume as pr
import cron.process_context as pc

app = Flask(__name__)

@app.route("/process-resume", methods=['POST'])
def processResume(event, lambda_context):
    pr.run()
    return "Resume Processed"

@app.route("/process-context", methods=['POST'])
def processContext(event, lambda_context):
    pc.run()
    return "Context Processed"