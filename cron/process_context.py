import utils.dynamodb_utils as dynamoDbUtils
import utils.lambda_utils as lambdaUtils
import requests
import json

def getNoRelevencyScoreData():
    response = requests.get('https://qvizwfql6f.execute-api.us-east-1.amazonaws.com/dev/application-no-relevancy')
    return response

def getOpenApiResponse(resumeContext, jobTitle):
    body = {
        'data': resumeContext,
        'role': jobTitle
    }
    response = lambdaUtils.invokeLambda(body, 'skills-screening-lambda')
    return response.decode()
    
def run():
    candiatesList = (getNoRelevencyScoreData()).json()
    for candidate in candiatesList:
        context = dynamoDbUtils.getResumeContext(candidate['candidate_id'])
        if (context):
            resumeContext = list(dict.values(context['context']))[0]
            response = json.loads(getOpenApiResponse(resumeContext, candidate['job_title']))
            if (response['status'] == 200):
                responseJson = json.loads(response['response'])
                updateSummary = dynamoDbUtils.putResumeSummary(str(candidate['candidate_id']), str(candidate['job_id']), json.dumps(responseJson['resume']))
                if (updateSummary['ResponseMetadata']['HTTPStatusCode'] == 200):
                    requestBody = {
                        'jobid': str(candidate['job_id']),
                        'candidateid': str(candidate['candidate_id']),
                        'percentageslist': responseJson['relevancy']
                    }
                    updateRelevency = requests.post(
                        'https://qvizwfql6f.execute-api.us-east-1.amazonaws.com/dev/application-no-relevancy',
                        data=requestBody
                    )
    return None