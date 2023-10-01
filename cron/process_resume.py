import boto3 as b3
import utils.textract_utils as textUtils

BUCKET_NAME = 'resume-screener-resume-storage-dev'
BUCKET_RESUME_DIRECTORY = 'uploads/'

# def analyzeDocument(key):
    # textract = b3.client('textract')
    # extractResult = textract.analyze_document(
    #     Document= {
    #         'S3Object': {
    #             'Bucket': BUCKET_NAME,
    #             'Name': key,
    #         }
    #     },
    #      FeatureTypes=[
    #         'LAYOUT'
    #     ],
    # )
    # print(key)
    # print(extractResult)

'''
    readResumeFromS3
    Purpose - Reads the resume present in given BUCKET_NAME and inside BUCKET_RESUME_DIRECTORY
    Returns - List of all keys present in the given BUCKET_RESUME_DIRECTORY
'''
def readResumeFromS3():
    s3 = b3.client('s3')
    objectsList = s3.list_objects(Bucket=BUCKET_NAME, Marker=BUCKET_RESUME_DIRECTORY, Prefix=BUCKET_RESUME_DIRECTORY)
    objectNames = [item['Key'] for item in objectsList['Contents']]
    # obj = s3.get_object(Bucket=BUCKET_NAME, Keys=objectNames)
    return objectNames
'''
    run
'''
def run():
    listOfResume = readResumeFromS3()
    for key in listOfResume:
        # analyzeDocument(key)
        extractedText = textUtils.exteractTextFromDocument(key)
        print(extractedText)