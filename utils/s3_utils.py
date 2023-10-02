import boto3 as b3

BUCKET_NAME = 'resume-screener-resume-storage-dev'
BUCKET_RESUME_DIRECTORY = 'uploads/'
BUCKET_TARGET_DIRECTORY = 'processed/'
RESUME_CONTEXT_TABLE = 'resume_context'

s3 = b3.client('s3')

'''
    readResumeFromS3
    Purpose - Reads the resume present in given BUCKET_NAME and inside BUCKET_RESUME_DIRECTORY
    Returns - List of all keys present in the given BUCKET_RESUME_DIRECTORY
'''
def readResumeFromS3():
    
    objectsList = s3.list_objects(Bucket=BUCKET_NAME, Marker=BUCKET_RESUME_DIRECTORY, Prefix=BUCKET_RESUME_DIRECTORY)
    objectNames = []
    if ('Contents' in dict.keys(objectsList)):
        objectNames = [item['Key'] for item in objectsList['Contents']]
    return objectNames

'''
    moveAndDeleteObject
    Purpose - Move the object from one bucket directory to another bucket directory
'''
def moveAndDeleteObject(objectKey):
    # print(objectKey)
    targetKey = BUCKET_TARGET_DIRECTORY + objectKey.split(BUCKET_RESUME_DIRECTORY)[1]
    response = s3.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={
            'Bucket': BUCKET_NAME,
            'Key': objectKey
        },
        Key=targetKey
    )
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        deleteResponse = s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=objectKey
        )