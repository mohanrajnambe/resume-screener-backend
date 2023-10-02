import utils.textract_utils as textUtils
import utils.s3_utils as s3Utils
import utils.dynamodb_utils as dynamoDbUtils

BUCKET_NAME = 'resume-screener-resume-storage-dev'
BUCKET_RESUME_DIRECTORY = 'uploads/'
BUCKET_TARGET_DIRECTORY = 'processed/'
RESUME_CONTEXT_TABLE = 'resume_context'
    
'''
    run
'''
def run():
    listOfResume = s3Utils.readResumeFromS3()
    for key in listOfResume:
        extractedText = textUtils.exteractTextFromDocument(key)
        # print(extractedText)
        response = dynamoDbUtils.putResumeContext(key, extractedText)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            s3Utils.moveAndDeleteObject(key)