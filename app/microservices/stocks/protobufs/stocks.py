from concurrent import futures
import enum
from logging import raiseExceptions
#import psycopg2
#from app.database.createDB import User, UserVote, Stocks,Company
#from database.createDB import User, UserVote, Stocks,Company
from createDB import User, UserVote, Stocks
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import func
#from passlib.apps import custom_app_context as pwd_context
# an Engine, which the Session will use for connection
# resources
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from datetime import datetime, timedelta

#from . import stocks_pb2
import stocks_pb2
    
#from . import stocks_pb2_grpc
import stocks_pb2_grpc
from sqlalchemy import desc, asc

#engine = create_engine('postgresql+psycopg2://postgres:stockify@db/stockify')
engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@localhost:3306/stockify')
#engine = create_engine('postgresql+psycopg2://postgres:stockify@db:5432/stockify')
Session = sessionmaker(bind=engine)

#today_date = "2021/04/22"
today_date = '2021-02-01'
today_date = datetime.strptime(today_date, "%Y-%m-%d")

class stocksService(stocks_pb2_grpc.StocksServicer):
    def getStocksCompany(self, request):
        # Filtering database by company code and date
        if request.get('date') == 'daily':
            days=1
        elif request.get('date') == 'weekly':
            days = 7
        elif request.get('date') == 'monthly':
            days = 30
        else:
            days = 365
            
        
        start_date = today_date - timedelta(days=days) 
        
        today_date_str = today_date.strftime("%Y-%m-%d")
        start_date_str = start_date.strftime("%Y-%m-%d")   
        
        session = Session()
        #print(session)
        q = session.query(Stocks).filter((request.get('ccode') == Stocks.company_code)).filter(Stocks.date.between(start_date_str, today_date_str))
        print("Query: ",len(q.all()))

        q1 = session.query(Stocks).filter((request.get('ccode') == Stocks.company_code)).filter(Stocks.date.between(start_date_str, today_date_str)).order_by(desc(Stocks.date)).limit(1)
        
        #q2 = session.query(Stocks).all()
        #for query in q2:
            #print(query.max_price)
        for query in q1:
            price=query.close
            max_price=query.max_price
            min_price=query.min_price
       
        price_hist = []
        for query in q:
            my_dict = {"date":str(query.date), "historic_price":query.close}
            price_hist.append(my_dict)    
       
        try:
            price_today = session.query(Stocks).filter((request.get('ccode') == Stocks.company_code)).filter(Stocks.date.between(today_date_str, today_date_str))#.order_by(desc(Stocks.date)).limit(1)
            for i  in price_today:
                price = i.close
                print("price today {}".format(price))
        except:
            return stocks_pb2.responseStock(price=price, max_price=max_price, min_price=min_price, ccode=request.get('ccode'), average_price=0, price_Arr=price_hist)

        
        try:
            price_previous = session.query(Stocks).filter((request.get('ccode') == Stocks.company_code)).filter(Stocks.date.between(start_date_str, start_date_str))#.order_by(asc(Stocks.date)).limit(1)
            for j in price_previous:
                previous_price = j.close
            print("price previous {}".format(previous_price))
        except:
            return stocks_pb2.responseStock(price=price, max_price=max_price, min_price=min_price, ccode=request.get('ccode'), average_price=0, price_Arr=price_hist)

        
        
            
        

        price_variation = ((price-previous_price)/previous_price)*100
        
        return stocks_pb2.responseStock(price=price, max_price=max_price, min_price=min_price, ccode=request.get('ccode'), average_price=price_variation, price_Arr=price_hist)

    
    def getStocksDate(self, request):
        if request == 'daily':
            days=1
        elif request == 'weekly':
            days = 7
        elif request == 'monthly':
            days = 30
        else:
            days = 365
        
    
        start_date = today_date - timedelta(days=days) 
        session = Session()
        
        q = session.query(Stocks).filter(start_date<=today_date)
        date_s=[]
        for query in q:
            my_dict = {"ccode":query.company_code, "date":str(query.date), "current_price":query.close, "max_price":query.max_price, "min_price":query.min_price}
            date_s.append(my_dict)

        return stocks_pb2.responseDate(stockDateArr=date_s)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    stocks_pb2_grpc.add_StocksServicer_to_server(
        stocksService(), server
    )
    #server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:5003") #added
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()





