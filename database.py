from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import urllib.parse

MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_HOST = settings.MYSQL_HOST
MYSQL_DB = settings.MYSQL_DB

# Build connection string
if MYSQL_PASSWORD:
    encoded_password = urllib.parse.quote_plus(MYSQL_PASSWORD)
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}/{MYSQL_DB}"
else:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}@{MYSQL_HOST}/{MYSQL_DB}"

# Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
