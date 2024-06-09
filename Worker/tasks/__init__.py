import pickle
import time
from db import Student
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
import os 
import json

### Connect to database
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(user=db_user, password=db_password, host=db_host, db=db_name))

# Retry connecting after 5 seconds if failed
Session = sessionmaker(bind=engine)
session = Session()

# Process login using data
def Process_Login(data):
    """ Authenticates user login """
    student_name = data['student_name']
    student_password = data['student_password']
    try:
        student = session.query(Student).filter(Student.student_name == student_name).first()
        if student:
            if check_password(student_password, student.student_password):
                # Password is correct, return user data
                return json.dumps({'result': 'true'})
            else:
                # Password is incorrect
                return json.dumps({'result': 'false'})
        else:
            # User not found
            return json.dumps({'result': 'false'})
    except Exception as e:       
        return "Error:" + str(e)

# Check decoded password
def check_password(password, hashed_password):
    """ Verifies password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Process create using data
def Process_Create(data):
    try:
        if data:
            # extract values from json
            student_name = data['student_name']
            student_type = data['student_type']
            student_version = data['student_version']
            student_owner = data['student_owner']
            student_password = data['student_password']
            hash_password = set_password(student_password)
            if student_name and student_type and student_version and student_owner and hash_password:
                student = Student(
                    student_name=student_name,
                    student_password=hash_password,
                    student_type=student_type,
                    student_version=student_version,
                    student_owner=student_owner              
                )
                session.add(student)
                session.commit()   
                return json.dumps({'result': data})
            else:
                return json.dumps({'result': 'false'})
    
    except Exception as e:
        print("Error:" + str(e))
        return False
    
# Set encoded password
def set_password(password):
    """ Generates hashed password """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')