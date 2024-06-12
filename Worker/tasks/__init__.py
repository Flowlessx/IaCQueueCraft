from sqlalchemy.exc import SQLAlchemyError
from db import Company, Account # Assuming 'Companies' is the model for the 'companies' table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager
import requests
import logging

### Connect to database
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
Gitlab_Token = os.environ['Gitlab_Token']

engine = create_engine(
    'postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(user=db_user, password=db_password, host=db_host, db=db_name),
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections every 30 minutes
    connect_args={'connect_timeout': 10}
)

Session = sessionmaker(bind=engine)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def register_company(data):
    with session_scope() as session:
        try:
            new_company = Company(name=data['name'])
            session.add(new_company)
            session.flush()  # Flush to get the id before committing

            # Define the URL for creating a new GitLab project
            url = "http://172.21.86.168/api/v4/projects"
            headers = {"Private-Token": Gitlab_Token}
            payload = {"name": data['name']}  # Use company name for the project

            # Send the POST request to create the project
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 201:  # 201 Created
                response_data = response.json()
                repo_id = response_data['id']  # Extract the repository ID from the response
                commit_message = "Initial commit for organization " + data['name']

                # Read the orgformation.yaml file content
                with open("tasks/orgformation/organization.yaml", "r") as orgformation_file:
                    orgformation_content = orgformation_file.read()

                file_path = "organization.yaml"

                commit_result = make_commit(repo_id, commit_message, file_path, orgformation_content)
                if commit_result["status"] == "success":
                    session.commit()
                    return "Company registered successfully"
                else:
                    logger.error(f"Commit failed: {commit_result['message']}")
                    return f"Company registered, but file commit failed: {commit_result['message']}"
            else:
                logger.error(f"Company registration failed: {response.content.decode()}")
                return f"Company registration failed: {response.content.decode()}"
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            return f"Database error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"

def create_account(data):
    with session_scope() as session:
        try:
            # Define the URL
            url = "http://172.21.86.168/api/v4/projects"
            # Define the headers
            headers = {"Private-Token": Gitlab_Token}
            # Define the payload
            payload = {
                "name": data['account_name']  # Replace "account_name" with the actual value from data
            }
            # Send the POST request
            response = requests.post(url, headers=headers, json=payload)

            # Check if the request was successful
            if response.status_code in {201}:  # 201 Created
                response_data = response.json()
                repo_id = response_data['id']  # Extract the repository ID from the response
                commit_message = "Initial commit " + data['account_name']
                # Read the Terraform file content
                with open("tasks/terraform/main.tf", "r") as terraform_file:
                    terraform_content = terraform_file.read()

                file_path = "main.tf"

                commit_result = make_commit(repo_id, commit_message, file_path, terraform_content)
                if commit_result["status"] == "success":
                    # Account model and a relationship with Companies
                    new_account = Account(name=data['account_name'], company_id=data['company_id'])
                    session.add(new_account)
                    session.flush()  # Flush to get the id before committing
                    session.commit()
                    return {"status": "success", "message": "Account created successfully"}, 201
                else:
                    logger.error(f"Commit failed: {commit_result['message']}")
                    return {"status": "error", "message": "Account failed to be committed"}, 500
            else:
                logger.error(f"Account creation failed: {response.content.decode()}")
                return {"status": "error", "message": f"Account creation failed: {response.content.decode()}"}, response.status_code
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            return {"status": "error", "message": f"Database error: {str(e)}"}, 500
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}, 500

def make_commit(repo_id, commit_message, file_path, file_content):
    try:
        url = f"http://172.21.86.168/api/v4/projects/{repo_id}/repository/commits"
        headers = {"Private-Token": Gitlab_Token}
        payload = {
            "branch": "main",
            "commit_message": commit_message,
            "actions": [
                {
                    "action": "create",
                    "file_path": file_path,
                    "content": file_content
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return {"status": "success"}
        else:
            return {"status": "error", "message": response.content.decode()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_companies():
    with session_scope() as session:
        companies = session.query(Company).all()
        return [{'id': company.id, 'name': company.name} for company in companies]
   
def get_accounts(data):
    with session_scope() as session:
        # Account model with a proper relationship with Companies
        accounts = session.query(Account).filter(Account.company_id == data['company_id']).all()
        return [{'id': account.id, 'name': account.name, 'company_id':account.company_id} for account in accounts]


