import json
import os
#import requests
#from bottle import route, run, request
import bottle
import random 
import sys
#import logging
import fakebidder 
from fakebidder import *


##########
# Global variable 
#########

#global auction_id

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

    mylogger = mycustomelogger()
    mylogger.info(bidresponse.bidResponse) 
   
    return json.dumps ( bidresponse.bidResponse ) 




def main():
    cmdargs = sys.argv
    PORT_NUMBER = cmdargs[1] 
    print "\\\\\\\\\\\\\\==================================="
    print PORT_NUMBER 

    bottle.run(host='0.0.0.0', port=PORT_NUMBER)
    # my code here

if __name__ == "__main__":
    main()


  

