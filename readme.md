

# Resume Screener Backend

## Local Setup

- ### Clone the project

- ### Create virtual environment
  
  ```bash
    python3 -m venv resume-screener-backend-venv
  ```

- ### Active virtual environment

  ```bash
   ./resume-screener-backend-venv/bin/activate
  ```

- ### Install requirements
  Inside the project directory  ```resume-screener-backend```, run

  ```bash
    pip install -r requirements.txt
  ```

- ### Run application locally
  Inside the project directory  ```resume-screener-backend```, run

  ```bash
    sls wsgi serve
  ```

  This command would start the application lcoally and run on ```http://localhost:5000```

## Troubleshooting

- If there happens to be any error while trying to run the application locally using the sls command, Install the following serverless plugins:
  - #### serverless-python-requirements
  - #### serverless-wsgi
  - #### serverless-offline
  - #### serverless-dynamodb-local

- Minimun node version to run serverless is ```Node 14.x```