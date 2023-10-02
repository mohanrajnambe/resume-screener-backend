import boto3 as b3

BUCKET_NAME = 'resume-screener-resume-storage-dev'
BUCKET_RESUME_DIRECTORY = 'uploads/'
BUCKET_TARGET_DIRECTORY = 'processed/'
RESUME_CONTEXT_TABLE = 'resume_context'
RESUME_SUMMARY_TABLE = 'resume_summary'

dynamoDb = b3.client('dynamodb')

def putResumeContext(objectKey, resumeContext):
    candidateId = (objectKey.split(BUCKET_RESUME_DIRECTORY)[1]).split('.pdf')[0]
    print(f'candidateId: {candidateId}')
    response = dynamoDb.put_item(
        TableName=RESUME_CONTEXT_TABLE,
        Item={
            'candidateId': {
                'S': candidateId
            },
            'context': {
                'S': resumeContext
            }
        }
    )
    return response

def getResumeContext(candidateKey):
    resumeContext = dynamoDb.get_item(
        TableName=RESUME_CONTEXT_TABLE,
        Key={
            'candidateId': {
                'S': str(candidateKey)
            }
        }
    )
    return resumeContext['Item'] if 'Item' in dict.keys(resumeContext) else None

def putResumeSummary(candidateId, jobId, resumeSummary):
    response = dynamoDb.put_item(
        TableName=RESUME_SUMMARY_TABLE,
        Item={
            'candidateId': {
                'S': candidateId
            },
            'jobId': {
                'S': jobId
            },
            'summary': {
                'S': resumeSummary
            }
        }
    )
    return response