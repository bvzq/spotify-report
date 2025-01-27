#from threading import activeCount
#from . microservices.stocks.protobufs import stocks
#from . microservices.ml.protobufs import prediction
#from . microservices.account.protobufs import account
import stocks
#from microservices.ml.protobufs import prediction
#from microservices.account.protobufs import account
#import account
#import stocks
#import prediction
#from authlib.integrations.flask_client import OAuth
#from flask import Flask
from flask import make_response,jsonify,abort
#from functools import wraps
#import json
#from os import environ as env
#from werkzeug.exceptions import HTTPException

#from dotenv import load_dotenv, find_dotenv
#from flask import redirect
#from flask import session
#from flask import url_for
import json
from six.moves.urllib.request import urlopen
from functools import wraps
import http.client
#from flask import request, _request_ctx_stack
#from flask_cors import cross_origin
#from jose import jwt
#from six.moves.urllib.parse import urlencode
#from oauthlib.oauth2 import WebApplicationClient, AuthorizationCodeGrant





def read_one(ccode, date):
    my_dict={"ccode": ccode, "date": date}
    resp = stocks.stocksService().getStocksCompany(my_dict)
    

    return make_response(jsonify({"price":resp.price, "price_variation":resp.average_price, "ccode":resp.ccode, "price_Arr":{"historic_price":[resp.price_Arr[i].historic_price for i in range(len(resp.price_Arr))],
     "date":[resp.price_Arr[i].date for i in range(len(resp.price_Arr))]}}))

def read_date(date):
    resp = stocks.stocksService().getStocksDate(date)

    return make_response(jsonify({'ccode':[resp.stockDateArr[i].ccode for i in range(len(resp.stockDateArr))], 'current_price':[resp.stockDateArr[i].current_price for i in range(len(resp.stockDateArr))], 
    'min_price':[resp.stockDateArr[i].min_price for i in range(len(resp.stockDateArr))], 'max_price':[resp.stockDateArr[i].max_price for i in range(len(resp.stockDateArr))], 'date':[resp.stockDateArr[i].date for i in range(len(resp.stockDateArr))]}))



#read_one("AAA", "daily")