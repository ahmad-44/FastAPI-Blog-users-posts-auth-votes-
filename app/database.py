from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Establish a connection with db. This engine also manages pool of db connections
engine = create_engine(f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}", echo=False)

# It creates a session factory bound to the engine. 
# That factory will generate new Session objects when called.
#now, autoflush (making pending ORM changes to DB) will be called only when we call commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# This function is a FastAPI dependency that provides a database session to path operations then guarantees the session is closed after the request is done.
def get_db():
    db = SessionLocal() # Create a new session
    try:
        yield db # Yield the session to be used in the request
    finally:
        db.close() # Ensure the session is closed after the request

# Define the Base class for declarative models 
Base = declarative_base()

"""
#it was used for testing the connection in main.py with rather manual approach which used psycopg and not the orm approach
# import psycopg
# from psycopg.rows import dict_row
# import time
# while True:
#     try:
#         conn = psycopg.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="asdasd",
#             row_factory=dict_row
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed ************")
#         print("Error:", error)
#         time.sleep(2)
"""