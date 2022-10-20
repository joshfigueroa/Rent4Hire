from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to a remote MySQL instance on Amazon RDS

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:Rent4Hire@aws-rent4hire-database.c543rvh0sa3x.us-east-1.rds.amazonaws.com:3306/rent4hire"
# SQLALCHEMY_DATABASE_URL = "aws-rent4hire-database.c543rvh0sa3x.us-east-1.rds.amazonaws.com"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
