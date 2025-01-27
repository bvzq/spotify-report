from threading import activeCount
#from . microservices.stocks.protobufs import stocks
#from . microservices.ml.protobufs import prediction
#from . microservices.account.protobufs import account

import prediction
#import account
#import stocks
#import prediction
#from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask import make_response,jsonify,abort
from functools import wraps
import json

#from dotenv import load_dotenv, find_dotenv

from flask import url_for
import json
from six.moves.urllib.request import urlopen

#import http.client
from flask import request, _request_ctx_stack
#from flask_cors import cross_origin
#from jose import jwt
#from six.moves.urllib.parse import urlencode
#from oauthlib.oauth2 import WebApplicationClient, AuthorizationCodeGrant


APP = Flask(__name__)


AUTH0_DOMAIN = 'dev-ic19sbcj.us.auth0.com'
API_AUDIENCE = "https://stockify_api"
ALGORITHMS = ["RS256"]
jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
jwks = json.loads(jsonurl.read())

APP = Flask(__name__)



def get_prediction(ccode):
    req = {'ccode':ccode}
    resp = prediction.Stats_service().getPrediction(req)
    return make_response(jsonify({
        'message': resp.company_stats[0].message,
        'name': resp.company_stats[0].name,
        'prediction_one_day':resp.company_stats[0].prediction_one_day,
        'prediction_two_day':resp.company_stats[0].prediction_two_day,
        'prediction_three_day':resp.company_stats[0].prediction_three_day
    }))


