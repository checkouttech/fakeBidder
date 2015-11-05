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

#############
# End points 
############

@bottle.route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


@bottle.route('/requestdetails', method='POST')
def print_request_details():

    bidrequest = requestClass(bottle.request)
    requestDetails =  bidrequest.getDetails()

    bidresponse = responseClass(bottle.response) 
    bidresponse.set_response(requestDetails) 

    bidresponse.content_type = 'application/json'
    return json.dumps ( bidresponse.get_response() )



@bottle.route('/fakebidder/', method='POST')
def return_bid() :

    bidrequest = requestClass(bottle.request)

    bidresponse = responseClass(bottle.response) 

    bidresponse.get_bid_template()    # TODO : move into bid template 
    bidresponse.createResponse(bidrequest)
    
    return json.dumps ( bidresponse.bidResponse ) 


#%
#%    print2log = "DSP Response : id : ", fakebidder.auction_id ," : " , responseBid
#%
#%    logging.info(print2log)
#%    sys.stdout.flush()
#%    print "DSP Response : id : ", fakebidder.auction_id ," : " , responseBid
#%
#%    #logger = loggingClass()
#%
#%    bidresponse.set_response(responseBid) 
#%
#%    bidresponse.content_type = 'application/json'
#%    return json.dumps ( bidresponse.get_response() )

    #requestDetails =  bidrequest.getDetails()
    #requestData = json.dumps ( requestDetails['data'] ) 

    #bidresponse.set_response(requestDetails) 

    #print " print the object ------> " , bidrequest.printRequest()

    #print "getDetails function ---->   " , bidrequest.getDetails()
    #print "requestDetails variable ----> " , bidrequest.requestDetails 

    #requestData = bottle.request.body.read()

    #print "requestData direct " , requestData

    #check if valid json 
    #if ( is_valid_json(requestData)) :
    #    postdata = bottle.request.body.read()
    #else:
    #    return "ERROR: bad JSON"
     
    #if ( bidrequest.is_valid_data(requestDetails['data'])):
    #    print  "valid json " 
    #else :
    #     return "ERROR: bad JSON"

    #responseBidTemplate = get_bid_template()

    #responseBidTemplate = bidresponse.get_bid_template()

    #responseBid = populate_bid_template(requestData,responseBidTemplate) 
    #responseBid = populate_bid_template(requestDetails['data'] , bidresponse.get_bid_template()) 
    #return responseBid


   
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

    #print  dict ( requestDetails ,skipkeys = True ,ensure_ascii=False, sort_keys=True )
