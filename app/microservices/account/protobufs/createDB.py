import enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy_utils import database_exists, create_database
# an Engine, which the Session will use for connection
# resources




engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@db:3306/stockify')
#engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@db:3307/stockify')

if not database_exists(engine.url):
    create_database(engine.url)


Base = declarative_base()

class VoteEnum(enum.Enum):
    Up = 1
    Down = 2

#Define Company Table
class Company(Base):
    __tablename__ = 'Company'
    company_code = Column(String,primary_key=True)
    security = Column(String)
    sec = Column(String)
    gics_sector = Column(String)
    gics_sub_industry = Column(String)
    heads_location = Column(String)
    start_date = Column(Date)
    cik = Column(String)
    founded = Column(String)

#Define User Table
class User(Base):
    __tablename__ = 'User'
    user_id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    email = Column(String,unique=True)
    birth_date = Column(Date)
    gender = Column(String)
    #child = relationship(UserVote, backref="User", passive_deletes=True)

#Define Stocks Table
class Stocks(Base):
    __tablename__ = 'Stocks'
    stock_id = Column(Integer,primary_key=True)
    company_code = Column(String,ForeignKey("Company.company_code"))
    date = Column(Date)
    max_price = Column(Float)
    min_price = Column(Float)
    volume = Column(Float)
    close = Column(Float)
    open = Column(Float)

#Define UserVote Table
class UserVote(Base):
    __tablename__ = 'UserVote'
    user_id = Column(Integer,ForeignKey("User.user_id",ondelete='CASCADE'),primary_key=True)
    company_code = Column(String,ForeignKey("Company.company_code",ondelete='CASCADE'),primary_key=True)
    vote_type = Column("value",Enum(VoteEnum))


#Create All tables
Base.metadata.create_all(engine)
#Drop tables
#Base.metadata.drop_all(engine)

# create session and add objects
#with Session(engine) as session:
 #   session.begin()
  #  try:
   #     
    #except:
     #   print('Unconnected')
