#!/usr/bin/python
# Filename: fakebidder.py


###########################################################
### PACKAGES
############################################################

import json
import os
#import requests
#from bottle import route, run, request
import bottle
import random 
import sys
import logging
import memcache


os.putenv('PYTHONUNBUFFERED', 'enabled')
sys.stdout.flush()




#import bottle


#import json
#import os
#import requests
#from bottle import route, run, request
#import random 
#import sys
#import logging


## Global variable 
global memcache_host
memcache_host = "192.168.150.110"
global memcache_port
memcache_port = "11211"
 

##  Classes 

class memcacheConnection():
    def __init__(self):
        memcache_details = memcache_host  +":"+ memcache_port
        self.connection = memcache.Client([memcache_details], debug=0)
        print "initializing memcache" 
     
    def setValue(self,key,value):
        self.connection.set(key,value)
        print "setting memcache value - ", key ," : ", value
   
    def getValue(self,key):
        key = str(key) 
        value = self.connection.get(key)
        print "reading memcache value - ", key ," : ", value
        return value 


class requestClass():

    def __init__(self,bottleRequestObject):
        self.requestObject = bottleRequestObject
        self.requestDetails = {}
        self.requestDetails['headers'] = dict( bottle.request.headers ) 
        self.requestDetails['cookies'] = dict( bottle.request.cookies ) 
        self.requestDetails['data']    =  json.loads ( bottle.request.body.read() ) 


    def printRequest(self):
        print "inside requestClass.printRequest -----> ", self.requestObject.body.read()

    def getDetails(self):
        requestDetails = {}
        requestDetails['headers'] =  dict( bottle.request.headers ) 
        requestDetails['cookies'] =  dict( bottle.request.cookies ) 
        requestDetails['data']    =  json.loads ( bottle.request.body.read() ) 

        print type ( requestDetails )
        #print  dict ( requestDetails ,skipkeys = True ,ensure_ascii=False, sort_keys=True )

        #check if valid json
        #if ( is_valid_json(requestData)) :
        #    postdata = bottle.request.body.read()
        #else:
        #    return "ERROR: bad JSON"
        #pass
   
  
        return requestDetails

    def is_valid_json(jsonVariable):
        try:
            json_object = json.loads(jsonVariable) 
        except ValueError, e:
            return False
        return True 
    


class responseClass():

    def __init__(self,bottleResponseObject):
        self.responseObject = bottleResponseObject

    def printRequest(self):
        print "inside requestClass.printRequest -----> ", self.requestObject.body.read()

    def set_response(self,requestDetails):
        self.response = requestDetails

    def get_response(self):
        return self.response

    def get_bid_template(self):
        #  will eventually come from a yaml template file 
        self.bidResponseTemplate  = {
               "id": "auctionId",
               "seatbid": [ {
                     "seat":"testseat",
                     "bid": [ {
                             "id": "required id per 4.3.3",
                             "impid": "impid per 4.3.3",
                             "adomain": [ "gawker" ],
                             "price": "BID_PRICE",
                             "ext": { "creativeapi": 3 },
                             "adm": "<img src=\"http://www.foo.com/wp-content/themes/foo/images/ftr_icon.png?auction=${AUCTION_ID}&price=${AUCTION_PRICE:BF}\">",
                             "crid": "12345678"
                            } ]
                          } ]
             }
        return self.bidResponseTemplate


    def createDetailsResponse(self,bidrequest):

        # bid response template 
        self.bidResponse  = bidrequest.requestDetails


    def createBidResponse(self,bidrequest):

        # populate bid price 
        if ( 'userID' in bidrequest.requestDetails['data'] ) :
            # TODO : if network-userID key present in KV
            userID = bidrequest.requestDetails['data']['userID']
            userKV = memobj.getValue(userID)
            bid = userKV['returnBidAmount']

        elif ( bidrequest.requestDetails['cookies']['returnBidAmount'] ) : # if return bid price present in bid request cookie , use it
            bid = bidrequest.requestDetails['cookies']['returnBidAmount']

        else :  # return randon bid price
            bid = random.uniform(1, 10)


        #  populate bidResponseTemplate variable 
        self.get_bid_template()

        # bid response template 
        self.bidResponse  = self.bidResponseTemplate
    
        # get auction id from bid request and set it in response
        self.bidResponse['id'] = bidrequest.requestDetails['data']['auction_id']

        # set the bid in response 
        self.bidResponse['seatbid'][0]['bid'][0]['price'] = bid 


def mycustomelogger():

    #create logger with "spam_application"
    logger = logging.getLogger("spam_application")
    logger.setLevel(logging.DEBUG)
    
    #create file handler and set level to debug
    fh = logging.FileHandler("spam.log")
    fh.setLevel(logging.DEBUG)
    
    #create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -  %(message)s")
    #add formatter to fh
    fh.setFormatter(formatter)
    
    #add fh to logger
    logger.addHandler(fh)
    
    logging.basicConfig(  stream=sys.stdout, 
                      level=logging.INFO,
                      format= '[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} - %(message)s',
                      datefmt='%H:%M:%S')
    
    return logging 
    #return logger 
    

## Declaring global objects
global memobj 
memobj = memcacheConnection() 
 


def hello():
    print 'Hi, this is mymodule speaking.'

# End of mymodule.py

def is_valid_json(jsonVariable):
    try:
        json_object = json.loads(jsonVariable) 
    except ValueError, e:
        return False
    return True 

#%
#%def get_bid_template():
#%    #  will eventually come from a yaml template file 
#%    bidResponseTemplate  = {
#%           "id": "auctionId",
#%           "seatbid": [ {
#%                 "seat":"testseat",
#%                 "bid": [ {
#%                         "id": "required id per 4.3.3",
#%                         "impid": "impid per 4.3.3",
#%                         "adomain": [ "gawker" ],
#%                         "price": "BID_PRICE",
#%                         "ext": { "creativeapi": 3 },
#%                         "adm": "<img src=\"http://www.foo.com/wp-content/themes/foo/images/ftr_icon.png?auction=${AUCTION_ID}&price=${AUCTION_PRICE:BF}\">",
#%                         "crid": "12345678"
#%                        } ]
#%                      } ]
#%         }
#%    return bidResponseTemplate
#%
#%def populate_bid_template(requestData, responseJsonTemplate):
#%    global auction_id
#%    
#%    # convert json to a dictionary 
#%    ### requestDataDict = json.loads(requestData) 
#%    requestDataDict = requestData
#%
#%    # get auction id from bid request and set it in response
#%    auction_id =  requestDataDict['auction_id']  
#%    responseJsonTemplate['id'] = auction_id 
#%
#%    # popupate bid price 
#%    bid = 0 
#%    print bottle.request.get_cookie("returnBidAmount")
#%
#%
#%    if ( 'userID' in requestDataDict ) :  # if request contains userID 
#%        # TODO : if network-userID key present in KV
#%        userID = requestDataDict['userID']
#%        userKV = memobj.getValue(userID)
#%        bid = userKV['returnBidAmount']
#%  
#%    elif (  bottle.request.get_cookie("returnBidAmount") ) :  # if return bid price present in bid request cookie , use it
#%        bid = bottle.request.get_cookie("returnBidAmount")
#%
#%    else :  # return randon bid price  
#%        bid = random.uniform(1, 10)
#% 
#%    # set the bid in response 
#%    responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
#% 
#%    return responseJsonTemplate
#%
#%

def ifBuyerIdPresent ():
    pass 

