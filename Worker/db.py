from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']

engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(user=db_user, password=db_password, host=db_host, db=db_name))

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(200), unique=False, nullable=True)
    student_type = Column(String(200), unique=False, nullable=True)
    student_version = Column(String(200), unique=False, nullable=True)
    student_owner = Column(String(200), unique=False, nullable=True)
    student_password = Column(String(200), unique=False, nullable=True)

Base.metadata.create_all(engine)


