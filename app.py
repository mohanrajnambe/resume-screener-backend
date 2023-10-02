import json
import logging
from nis import cat
from re import L
from flask import Flask, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import Application, Job, Candidate, db
import os
import re
import boto3

app = Flask(__name__)
CORS(app)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

db.init_app(app)
migrate = Migrate(app, db)
table_name = 'resume_summary'
@app.route("/")
def main(event, context):
    return "Home is under construction!"

@app.route("/test")
def test(event, context):
    return "Api test is successs"

def candidate_to_dict(candidate):
    return {
        'id': candidate.id,
        'lastName': candidate.lastName,
        'firstName': candidate.firstName,
        'address': candidate.address,
        'email': candidate.email,
        'number': candidate.number
    }

def job_to_dict(job):
    return {
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'openingCount': job.openingCount,
    }

@app.route('/candidate-list')
def getCandidateList(event, context):
    try:
        query = Candidate.query.all()
        candidates_list = [candidate_to_dict(candidate) for candidate in query]
        return {
            'statusCode': 200,
            'body': json.dumps(candidates_list)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@app.route('/job-opening-list')
def getJobOpeningList(event, context):
    try:
        # print(f'args: {request.args}')
        print(f'event: {event}')
        applicationcount = 'false'
        # print("Received Lambda event: %s", json.dumps(event))
        # applicationcount = request.args.get('applicationcount')
        if event['applicationcount']:
            applicationcount =event['applicationcount']
        applicationCount = applicationcount.lower() == 'true'
        print(f'applicationCount: {applicationCount}')
        job_list = []

        if applicationCount:
            query = db.session.query(Job, db.func.count(Application.id).label('applicationCount')).outerjoin(Application).group_by(Job.id).having(db.func.count(Application.id) > 0).all()

            for job, application_count in query:
                job_dict = job_to_dict(job)
                job_dict['applicationCount'] = application_count
                job_list.append(job_dict)
        else:
            jobs = Job.query.all()

            for job in jobs:
                job_dict = job_to_dict(job)
                job_list.append(job_dict)
        response = {
            'statusCode': 200,
            'body': json.dumps(job_list)
        }
        return response
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@app.route('/post-job', methods=['POST'])
def postJob(event, context):
    try:
        logging.info("Received Lambda event: %s", json.dumps(event))
        event_body = json.loads(event['body'])
        data = event_body
        new_job = Job(
            title=data['title'],
            description=data['description'],
            openingCount=data['openingCount']
        )
        db.session.add(new_job)
        db.session.commit()

        return {
            'statusCode': 201,
            'body': json.dumps(job_to_dict(new_job))
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@app.route('/applied-jobs', methods=['GET'])
def getAppliedJobs(event, context):
    try:
        candidate_id = 0
        if event.get("queryStringParameters") and event["queryStringParameters"].get("candidateid"):
                candidate_id = event["queryStringParameters"]['candidateid']
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Candidate not found'})
            }

        applied_jobs = Application.query.filter_by(candidateId=candidate_id).all()

        job_list = []
        for applied_job in applied_jobs:
            job = applied_job.job
            job_dict = {
                'job_id': job.id,
                'job_title': job.title,
                'job_description': job.description,
                'application_status': applied_job.status
            }
            job_list.append(job_dict)

        response =  {
            'statusCode': 201,
            'body': json.dumps(job_list)
        }
        return response
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


@app.route('/non-applied-jobs', methods=['GET'])
def getNonAppliedJobs(event, context):
    try:
        candidate_id = 0
        if event.get("queryStringParameters") and event["queryStringParameters"].get("candidateid"):
                candidate_id = event["queryStringParameters"]['candidateid']
        candidate = Candidate.query.get(candidate_id)


        if not candidate:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Candidate not found'})
            }

        all_jobs = Job.query.all()
        applied_jobs = Application.query.filter_by(candidateId=candidate_id).all()
        applied_job_ids = set(applied_job.jobId for applied_job in applied_jobs)
        non_applied_jobs = [job for job in all_jobs if job.id not in applied_job_ids]
        job_list = []
        for job in non_applied_jobs:
            job_dict = {
                'job_id': job.id,
                'job_title': job.title,
                'job_description': job.description
            }
            job_list.append(job_dict)

        return {
            'statusCode': 201,
            'body': json.dumps(job_list)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@app.route('/apply-job', methods=['POST'])
def applyJob(event, context):
    try:
        logging.info("Received Lambda event: %s", json.dumps(event))
        event_body = json.loads(event['body'])
        job_id = event_body['jobid']
        candidate_id = event_body['candidateid']
        if job_id is None or candidate_id is None:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'jobid and candidateid are required'})
            }

        job = Job.query.get(job_id)
        candidate = Candidate.query.get(candidate_id)

        if not job or not candidate:
             return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Job or candidate not found'})
            }

        new_application = Application(jobId=job_id, candidateId=candidate_id, status='New')

        db.session.add(new_application)
        db.session.commit()

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Application submitted successfully'})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@app.route('/application-no-relevancy', methods=['GET'])
def getApplicationsWithNoRelevancy(event, context):
    try:
        applications = Application.query.filter_by(relevancyScore=-1).all()

        application_list = []
        for application in applications:
            job = Job.query.get(application.jobId)
            if job:
                application_dict = {
                    'job_id': application.jobId,
                    'job_title': job.title,
                    'candidate_id': application.candidateId,
                }
                application_list.append(application_dict)

        return {
            'statusCode': 200,
            'body': json.dumps(application_list)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@app.route('/post-average-relevancy', methods=['POST'])
def postAverageRelevancy(event, context):
    try:
        logging.info("Received Lambda event: %s", json.dumps(event))
        event_body = json.loads(event['body'])
        job_id = event_body['jobid']
        candidate_id = event_body['candidateid']
        percentages_list = event_body['percentageslist']

        numeric_values = [int(match.group()) for value in percentages_list for match in re.finditer(r'\d+', value)]

        if numeric_values:
            average = sum(numeric_values) / len(numeric_values)
            application = Application.query.filter_by(jobId=job_id, candidateId=candidate_id).first()
            if application:
                application.relevancyScore = average
                db.session.commit()
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Relevancy score updated successfully'})
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Application not found'})
                }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No valid numeric values found in the percentages_list'})
            }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


@app.route('/get-job-id', methods=['GET'])
def getJobById(event, context):
    try:
        print(event)
        # Retrieve the job by its ID
        job_id = 0
        if event.get("queryStringParameters") and event["queryStringParameters"].get("jobid"):
                job_id = event["queryStringParameters"]['jobid']
        job = Job.query.get(job_id)

        if not job:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Job not found'})
            }

        applications = Application.query.filter_by(jobId=job_id).all()
        applications_list = []

        for application in applications:
            candidate = Candidate.query.get(application.candidateId)
            if candidate:
                application_dict = {
                    'application_id': application.id,
                    'candidate_id': candidate.id,
                    'candidate_firstName': candidate.firstName,
                    'candidate_lastName': candidate.lastName,
                    'candidate_email': candidate.email,
                    'application_status': application.status,
                    'relevancy_score': application.relevancyScore
                }
                applications_list.append(application_dict)
                print(candidate.id)
                try:
                    # Use the get_item method to retrieve an item based on the candidate_id
                    response = dynamodb.get_item(
                        TableName='resume_summary',
                        Key={
                            'candidateId': {'S': str(candidate.id)},
                            'jobId': {'S': str(job_id)}
                        }
                    )

                    # Check if the item was found
                    print("Received Lambda event: %s", json.dumps(response))
                    if 'Item' in response:
                        item = response['Item']
                        # application_dict['summary'] = json.loads(item['summary']['S'])
                        summary = json.loads(item['summary']['S'])
                        # print(f"summary retrieved: {json.loads(item['summary']['S']['JSON'])}")

                        json_string = summary.replace('\n', '').replace('    ', '')
                        data = json.loads(json_string)
                        print
                        application_dict['summary'] = data

                    else:
                        print(f"No item found for candidate_id: {candidate.id} {job_id}")
                except Exception as e:
                    print(e)

        job_data = {
            'job_id': job.id,
            'job_title': job.title,
            'job_description': job.description,
            'job_openingCount': job.openingCount,
            'applications': applications_list
        }

        return {
            'statusCode': 200,
            'body': json.dumps(job_data)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
@app.route('/get-upload-resume-singed-url', methods=['GET'])
def getUploadResumePresignedUrl(event, context):
    s3 = boto3.client('s3')
    try:
        signedUrl = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': 'resume-screener-resume-storage-dev',
                'Key': 'upload/'
            },
            ExpiresIn=300
        )
        print(signedUrl)
        response = {
            'status': 200,
            'response': {
                'singedUrl': signedUrl,
                'expiration': 300
            }
        }
    except Exception as e:
        response = {
            'status': 500,
            'error': "Unable to generate presigned url"
        }
    return response
        
        
if __name__ == '__main__':
    app.run(debug=True)
