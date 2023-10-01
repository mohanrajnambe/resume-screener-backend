import boto3 as b3
import time

BUCKET_NAME = 'resume-screener-resume-storage-dev'
Client = b3.client('textract')

def invokeTextDetectJob(documentName):
    response = None
    response = Client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': BUCKET_NAME,
                'Name': documentName
            }
        })
    return response["JobId"]

def checkJobComplete(jobId):
    response = Client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job id: {}\nJob status: {}".format(jobId, status))
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = Client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job id: {}\nJob status: {}".format(jobId, status))
    return status

def getJobResults(jobId):
    pages = []
    response = Client.get_document_text_detection(JobId=jobId)
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']
        while(nextToken):
            response = Client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
            pages.append(response)
            print("Resultset page recieved: {}".format(len(pages)))
            nextToken = None
            if('NextToken' in response):
                nextToken = response['NextToken']
    return pages

def exteractTextFromDocument(documentName):
    jobId = invokeTextDetectJob(documentName)
    if (checkJobComplete(jobId)):
        result = getJobResults(jobId)
        extractedText = ''
        for resultPage in result:
            for item in resultPage["Blocks"]:
                if item["BlockType"] == "LINE":
                    extractedText += '\033[94m' + item["Text"] + '\033[0m'