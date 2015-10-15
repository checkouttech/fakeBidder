import json
import os
#import requests
#from bottle import route, run, request
import bottle
import random 
import sys
import logging
import fakebidder 
from fakebidder import *


##########
# Global variable 
#########

global auction_id

########## 
# Functions , TODO :  Will be moved to a module 
##########

#############
# End points 
############

@bottle.route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


@bottle.route('/requestdetails', method='POST')
def print_request_details():
    requestDetails = {}
    requestDetails['headers'] =  dump_headers()
    requestDetails['cookies'] =  dump_cookies()
    requestDetails['data']    =  dump_data()

    print type ( requestDetails )
    print  dict ( requestDetails ,skipkeys = True ,ensure_ascii=False, sort_keys=True )

    bottle.response.content_type = 'application/json'
    return json.dumps ( requestDetails )




@bottle.route('/fakebidder/', method='POST')
def return_bid() :
    requestData = bottle.request.body.read()

    #check if valid json 
    if ( is_valid_json(requestData)) :
        postdata = bottle.request.body.read()
    else:
        return "ERROR: bad JSON"
     
    responseJson = get_bid_template()
    responseBid = populate_bid_template(requestData,responseJson) 
    
    print2log = "DSP Response : id : ", fakebidder.auction_id ," : " , responseBid


    logging.info(print2log)
    sys.stdout.flush()
    print "DSP Response : id : ", fakebidder.auction_id ," : " , responseBid

    return responseBid

logging.basicConfig(  stream=sys.stdout, 
                      level=logging.INFO,
                      format= '[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} - %(message)s',
                      datefmt='%H:%M:%S')
logging.info('Watch out!')
#logging.basicConfig(format=FORMAT,level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
# format='%(asctime)s %(levelname)s %(message)s',
cmdargs = sys.argv

PORT_NUMBER = cmdargs[1] 
print "\\\\\\\\\\\\\\==================================="
print PORT_NUMBER 
print fakebidder.hello()

bottle.run(host='0.0.0.0', port=PORT_NUMBER)
#bottle.run(host='0.0.0.0', port=10001)

