from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings 
# formet :- SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>&<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:new_password@localhost/fastapi2'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False, autoflush=False,bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# hostname = "localhost"
# database = "fastapi"
# userss  = "postgres"
# pass1 = "new_password"
# while True: 

#     try:
#         conn = psycopg2.connect(host=hostname, database = database, user = userss, password = pass1)
#         cursor = conn.cursor()
#         print("Detabase has been created....!")
#         break
#     except Exception as error:
#         print("Connecting to database was failed")
#         print("Error: ", error)
        

