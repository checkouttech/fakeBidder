#!/usr/bin/env python


# Import fakebidder module 
import fakebidder 
from fakebidder import *
 
import statsd

##########
# Global variable 
#########

#global args 
global mylogger
global l 
global mydebuglogger

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

    print mylogger.debugLogger.getEffectiveLevel() 
    mylogger.debugLogger.debug(bidresponse.bidResponse) 

    bidresponse.content_type = 'application/json'

    return json.dumps ( bidresponse.bidResponse ) 


@bottle.route('/fakebidder/', method='POST')
def return_bid() :

    bidrequest = requestClass(bottle.request)

    bidresponse = responseClass(bottle.response) 

    bidresponse.createBidResponse(bidrequest)

    # log records info 
    mylogger.log_records(bidresponse)

    #feedGraphite
    network_id = "fb1"
    metric_name =   'fakebidder.'+  network_id + '.sum_bids_received'  
    print bidresponse.bidResponse['seatbid'][0]['bid'][0]['price']
    bidAmount = bidresponse.bidResponse['seatbid'][0]['bid'][0]['price']

    feedGraphite.connection.incr(metric_name, count=bidAmount)    

  

    bidresponse.content_type = 'application/json'
    return json.dumps ( bidresponse.bidResponse ) 


def main():
    
    setupObj = setupClass()

    global mylogger
    mylogger = loggerClass(setupObj) 
    #mydebuglogger = loggerClass(setupObj) 

    #mylogger.logger.info ("this is logger speaking ") 


    global feedGraphite
    feedGraphite =  graphiteClass(setupObj)

    PORT_NUMBER=setupObj.args.port  
    print " port id from the args object "   , setupObj.args  

    #quiet=True to suppress info message on every request 
    bottle.run(host='0.0.0.0', port=PORT_NUMBER, quiet=True)


if __name__ == "__main__":
         main()


  

