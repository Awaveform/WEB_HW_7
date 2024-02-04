from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Database connection information
db_user = 'postgres'
db_password = 'qwe'
db_host = 'localhost'  # if running locally
db_port = '5432'
db_name = 'postgres'

# Create the database engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@127.0.0.1:{db_port}/{db_name}')

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Rest of your model definitions...
