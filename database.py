from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


DATABASE_URL = URL.create(

    drivername='mysql+pymysql',

    username='avnadmin',
    password='AVNS_MRI-BUADEZtRkvue4qD',
    host='students-novostack-c49d.d.aivencloud.com',
    port=11640,
    database='loan_app'
)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()