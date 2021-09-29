import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database = os.environ.get('DATABASE_NAME', 'postgres')
user = os.environ.get('DATABASE_USER', 'postgres')
password = os.environ.get('DATABASE_PASSWORD', 'postgres')
host = os.environ.get('DATABASE_HOST', '127.0.0.1')
port = os.environ.get('DATABASE_PORT', '5432')

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
    user=user, password=password, host=host, port=port, database=database)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=100, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
