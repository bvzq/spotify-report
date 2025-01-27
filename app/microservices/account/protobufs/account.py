from concurrent import futures
import enum
#import psycopg2
from createDB import User, UserVote, Stocks,Company
#from createDB import User, UserVote, Stocks
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from passlib.apps import custom_app_context as pwd_context
# an Engine, which the Session will use for connection
# resources
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

#from . import account_pb2
import account_pb2
    
#from . import account_pb2_grpc
import account_pb2_grpc


engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@db:3306/stockify')
#engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@db:3307/stockify')
Session = sessionmaker(bind=engine)

#Account Service
class AccountService(account_pb2_grpc.AccountServicer):
    def readUser(self, request):
        session = Session()
        q = session.query(User).filter(request == User.username)
        #print([query.password for query in q])
        for query in q:
            user_id = query.user_id
            email = query.email
            username = query.username
            gender = query.gender
            birth_date = query.birth_date

        #verify = pwd_context.verify(password_req,password)
        #if verify:
            #print(verify)
            #Votes of the user
        q_vote = session.query(UserVote).join(Company).all()
        #print(q_vote)
        votes = []
        for row in q_vote:
            if user_id == row.user_id:
                #print(row.vote_type.value)
                vote =  account_pb2.Votes(ccode = row.company_code, vote_type = row.vote_type.value)
                votes.append(vote)
           
        #Information of user
        return account_pb2.respGetUser (
            username = username,
            email = email,
            birth_date = str(birth_date),
            gender = gender,
            vote_history = votes
        )

    def deleteUser(self, request):
        session = Session()
        session.query(User).filter(request == User.username).delete()
        session.commit()
        return account_pb2.responseUser(message='Successfully created')

    
    def createUser(self, request):
        #Hash password
        hash_pass = pwd_context.encrypt(request.get('password'))
        user = User(
            username=request.get('username'),
            email=request.get('email'),
            password=hash_pass,
            birth_date=request.get('birth_date'),
            gender=request.get('gender')
        )
        session = Session()
        session.add(user)
        session.commit()
        return account_pb2.responseUser(message='Successfully created')
        
    
    def updateUser(self, request):
        session = Session()
        req_username = request['username_default']
        query = session.query(User).filter(req_username == User.username)
        #.get('username')
        
        if req_username:
            username = str([q.username for q in query])
            if username != req_username:
                query.update({'username':req_username})
        
        if request['body_request'].get('birth_date'):
            query.update({'birth_date':request['body_request'].get('birth_date')})
        if request['body_request'].get('email'):
            query.update({'email':request['body_request'].get('email')})
        if request['body_request'].get('passowrd'):
            query.update({'email':request['body_request'].get('password')})
        
        session.commit()
        return account_pb2.responseUser(message='Successfully created')
    
    def createVote(self, request):
        session = Session()
        username= request.get('username')
        ccode = request.get('ccode')
        vote_type = request.get('vote_type')
        query = session.query(User).filter(username == User.username)
        for q in query:
            user_id = q.user_id 
        user_vote = UserVote( user_id = user_id, company_code =ccode, vote_type=vote_type)
        session.add(user_vote)
        session.commit()
        return account_pb2.responseUser(message='Successfully created')

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    account_pb2_grpc.add_AccountServicer_to_server(
        AccountService(), server
    )
    #server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:50051") #added
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()