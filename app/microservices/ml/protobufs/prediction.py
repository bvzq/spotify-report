from concurrent import futures
import enum
#import psycopg2
#from app.database.createDB import User, UserVote, Stocks,Company
#from database.createDB import User, UserVote, Stocks,Company
from createDB import User, UserVote, Stocks
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from statsmodels.tsa.arima.model import ARIMA
# an Engine, which the Session will use for connection
# resources
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
import pandas as pd

#!pip install cython
#!pip install pystan
#!pip install prophet
from prophet import Prophet

#from . import prediction_pb2
import prediction_pb2
    
#from . import prediction_pb2_grpc
import prediction_pb2_grpc


#engine = create_engine('postgresql+psycopg2://postgres:stockify@db/stockify')
engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@localhost:3306/stockify')
#engine = create_engine('postgresql+psycopg2://postgres:stockify@db:5432/stockify')
Session = sessionmaker(bind=engine)

#Account Service
class Stats_service(prediction_pb2_grpc.Stats_serviceServicer):
    def getPrediction(self, request):
        arr = []
        predictions = []
        session = Session()
        q = session.query(Stocks).filter(request.get('ccode') == Stocks.company_code)
        for query in q:
             arr.append({'date': query.date, 'close': query.close})
        df = pd.DataFrame(arr)
        
        #df = df.reset_index()
        df.columns = ['ds', 'y']
        df['ds']= pd.to_datetime(df['ds'])
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods = 3)
        pred = m.predict(future)
        
        for i in range(0,3):
            
            #Predict for three days
            yhat = list(pred['yhat'][-3:])[i]
            predictions.append(yhat)
        
        print("pred", predictions)

        return prediction_pb2.response_pred(company_stats = [{
            'message':'successfully predicted',
            'name':request.get('ccode'),
            'prediction_one_day':predictions[0],
            'prediction_two_day':predictions[1],
            'prediction_three_day':predictions[2]
            }]) 





def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    prediction_pb2_grpc.add_Stats_serviceServicer_to_server(
        Stats_service(), server
    )
    #server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:5002") #added
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()