from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']

engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(user=db_user, password=db_password, host=db_host, db=db_name, connect_args={'connect_timeout': 5}))

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=False, nullable=False) 
    accounts = relationship("Account", back_populates="company")

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=False, nullable=False)
    platform = Column(String(200), unique=False, nullable=True)
    account_type = Column(String(200), unique=False, nullable=True)
    # Add foreign key relationship to companies table
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    # Define relationship with Company model
    company = relationship("Company", back_populates="accounts")

Base.metadata.create_all(engine)
engine.dispose()
