#!/usr/bin/env python


# Import fakebidder module 
import fakebidder 
from fakebidder import *


##########
# Global variable 
#########

#global args 
global mylogger

#############
# End points 
############

@bottle.route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


@bottle.route('/requestdetails', method='POST')
def print_request_details():

    bidrequest = requestClass(bottle.request)

    bidresponse = responseClass(bottle.response) 

    bidresponse.createDetailsResponse(bidrequest)

    bidresponse.content_type = 'application/json'

    return json.dumps ( bidresponse.bidResponse ) 


@bottle.route('/fakebidder/', method='POST')
def return_bid() :

    bidrequest = requestClass(bottle.request)

    bidresponse = responseClass(bottle.response) 

    bidresponse.createBidResponse(bidrequest)

    mylogger.info(bidresponse.bidResponse) 
   
    bidresponse.content_type = 'application/json'
    return json.dumps ( bidresponse.bidResponse ) 


def main():
    
    setupObj = setupClass()

    global mylogger
    mylogger = mycustomelogger()

 
    PORT_NUMBER=setupObj.args.port  
    print " port id from the args object "   , setupObj.args  

    bottle.run(host='0.0.0.0', port=PORT_NUMBER)


if __name__ == "__main__":
         main()


  

