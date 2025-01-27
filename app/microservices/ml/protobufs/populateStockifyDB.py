from datetime import datetime
import enum
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from createDB import Stocks, Company
import os
import numpy as np
import pandas as pd


#engine = create_engine('postgresql+psycopg2://postgres:stockify@localhost/stockify')
engine = create_engine('mysql+mysqlconnector://stockify_user:cn_project_stockify2122@localhost:3306/stockify')

Session = sessionmaker(bind=engine)
session = Session()
#directory = os.fsencode('./data')

#Convert txt into csv
def convert_txt_to_csv(file_path,new_file,delimiter=','):
    txt = pd.read_csv(file_path,delimiter=delimiter)
    txt.to_csv(new_file)



#convert_txt_to_csv('./data/company.txt','./data/company.csv',delimiter=';')
#convert_txt_to_csv('./data/stocks.txt','./data/stocks.csv')

#------------- CORRER CODIGO ABAIXO--------------------------------
def populate_table(csv_file,table):

    df = pd.read_csv(csv_file)
    df = df.dropna()
    #i=0
    
    for i, val in enumerate(df.values):
        if table == 'Company':
            rec = Company (
                company_code = val[2],
                security = val[3],
                sec = val[4],
                gics_sector = val[5],
                gics_sub_industry = val[6],
                heads_location = val[7],
                start_date = datetime.strptime(str(val[8]), "%d/%m/%Y").date(),
                cik = val[9],
                founded = val[10]
            )
        else:
            rec = Stocks (
                company_code = val[-1],
                date = datetime.strptime(val[1], "%Y-%m-%d").date(),
                max_price = val[3],
                min_price = val[4],
                volume = val[6],
                close = val[5],
                open = val[2]

            )
            
        session.add(rec)
        #i+=1
        #print(i)
    session.commit()

#populate_table('./data/company.csv','Company')
populate_table('./data/stocks.csv','Stocks')
#--------------------------------------------------------------

