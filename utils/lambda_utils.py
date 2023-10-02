import boto3
import json

aws_region = 'us-east-1'
lambda_function_name = 'skills-screening-lambda'

lambda_client = boto3.client('lambda', region_name=aws_region)

def invokeLambda(inputData, lambdaName):
    response = lambda_client.invoke(
        FunctionName=lambdaName,
        InvocationType='RequestResponse',
        Payload=json.dumps(inputData)
    )
    return response['Payload'].read()