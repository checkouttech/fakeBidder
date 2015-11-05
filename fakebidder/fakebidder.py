#!/usr/bin/python
# Filename: fakebidder.py
import json
import os
#import requests
#from bottle import route, run, request
import bottle
import random 
import sys
import logging
import memcache


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

        #bottle.response.content_type = 'application/json'
        #return json.dumps ( requestDetails )
         #self.requestData = bottle.request.body.read()
        #self.requestData = bottleRequestObject.body.read()
    
        #check if valid json
        #if ( is_valid_json(requestData)) :
        #    postdata = bottle.request.body.read()
        #else:
        #    return "ERROR: bad JSON"
        #pass
   
        #headersDict = bottle.request.headers
        #headersDict = self.requestObject.headers
        #print bottle.request.get_header('host')
        #print bottle.request.headers.keys()
        #print bottle.request.headers['host']
  
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
    

    def createResponse(self,bidrequest):

        print "inside createResponse -----> ", bidrequest.requestDetails['data']

    #     responseBid = populate_bid_template(bidrequest.requestDetails['data'] , bidresponse.get_bid_template())

        #def populate_bid_template(requestData, responseJsonTemplate):
        
        # populate auction_id from request 
        # get auction id from bid request and set it in response

        print " auction id from requeset :::::::::::::::::> ",  bidrequest.requestDetails['data']['auction_id']

        # populate bid price 
        print " bid price from cookie :::::::::::::::::> ",  bidrequest.requestDetails['cookies']['returnBidAmount'] 
 
        # bid response template 
        print "bid response template:::::::::::::::::::> ",   self.bidResponseTemplate



        if ( 'userID' in bidrequest.requestDetails['data'] ) :
            # TODO : if network-userID key present in KV
            userID = bidrequest.requestDetails['data']['userID']
            userKV = memobj.getValue(userID)

            print "userID presenent -------> " , bidrequest.requestDetails['data']['userID'] 
            print " user ID value ", userKV
            bid = userKV['returnBidAmount']

        elif ( bidrequest.requestDetails['cookies']['returnBidAmount'] ) : # if return bid price present in bid request cookie , use it
            bid = bidrequest.requestDetails['cookies']['returnBidAmount']

        else :  # return randon bid price
            bid = random.uniform(1, 10)

        print "bid amount =------> " , bid

        self.bidResponse  = self.bidResponseTemplate
    


        self.bidResponse['seatbid'][0]['bid'][0]['price'] = bid 


        print "self.response -----> " , self.bidResponse

#%            # set the bid in response 
#%            responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
#      
#%            responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
#%            responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
 


 
#%          
#%            elif (  bottle.request.get_cookie("returnBidAmount") ) :  # if return bid price present in bid request cookie , use it
#%                bid = bottle.request.get_cookie("returnBidAmount")
#%        
#%            else :  # return randon bid price  
#%                bid = random.uniform(1, 10)
#%         
#%            # set the bid in response 
#%            responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
#%   



#%            # popupate bid price 
#%            bid = 0 
#%            print bottle.request.get_cookie("returnBidAmount")
        
 
#%        responseJsonTemplate['id'] = auction_id 
#% 
#%
#%        self.requestDetails['data']    =  json.loads ( bottle.request.body.read() ) 
#%
#%            global auction_id
#%            
#%            # convert json to a dictionary 
#%            ### requestDataDict = json.loads(requestData) 
#%            requestDataDict = requestData
#%        
#%       
#%        
#%        
#%            if ( 'userID' in requestDataDict ) :  # if request contains userID 
#%                # TODO : if network-userID key present in KV
#%                userID = requestDataDict['userID']
#%                userKV = memobj.getValue(userID)
#%                bid = userKV['returnBidAmount']
#%          
#%            elif (  bottle.request.get_cookie("returnBidAmount") ) :  # if return bid price present in bid request cookie , use it
#%                bid = bottle.request.get_cookie("returnBidAmount")
#%        
#%            else :  # return randon bid price  
#%                bid = random.uniform(1, 10)
#%         
#%            # set the bid in response 
#%            responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
#%         
#%            return responseJsonTemplate
#%        



    #bidresponse.createResponse(bidrequest)



#class myLogger():
#
#    def __init__(self,logging.getLoggerClass()):
#        self.logger = logging.getLogger('custom_logger')
#            
#    def setup_custom_logger(name):
#        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
#    
#        handler = logging.StreamHandler()
#        handler.setFormatter(formatter)
#    
#        logger = logging.getLogger(name)
#        logger.setLevel(logging.DEBUG)
#        logger.addHandler(handler)
#        return logger
#    
#
#    def setup_logger(logger_name, log_file, level=logging.INFO):
#        l = logging.getLogger(logger_name)
#        formatter = logging.Formatter('%(asctime)s : %(message)s')
#        fileHandler = logging.FileHandler(log_file, mode='w')
#        fileHandler.setFormatter(formatter)
#        streamHandler = logging.StreamHandler()
#        streamHandler.setFormatter(formatter)
#    
#        l.setLevel(level)
#        l.addHandler(fileHandler)
#        l.addHandler(streamHandler)   
#    

       #logging.basicConfig(  stream=sys.stdout, 
       #                       level=logging.INFO,
       #                       format= '[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} - %(message)s',
       #                       datefmt='%H:%M:%S')
       # logging.info('Watch out!')
        
    








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


#
#def dump_headers():
#    headersDict = {}
#    headersDict = bottle.request.headers
#    #print bottle.request.get_header('host')
#    #print bottle.request.headers.keys()
#    #print bottle.request.headers['host']
#    return dict ( headersDict ) 
#
#def dump_cookies():
#    cookiesDict = {}
#    cookiesDict = bottle.request.cookies
#    #print bottle.request.cookies.keys()
#    #print bottle.request.get_cookie("cookieName")
#    return dict ( cookiesDict)
#
#def dump_data():
#    dataDict = {}
#    dataDict =  json.loads ( bottle.request.body.read() ) 
#    return dataDict 
#
def get_bid_template():
    #  will eventually come from a yaml template file 
    bidResponseTemplate  = {
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
    return bidResponseTemplate

def populate_bid_template(requestData, responseJsonTemplate):
    global auction_id
    
    # convert json to a dictionary 
    ### requestDataDict = json.loads(requestData) 
    requestDataDict = requestData

    # get auction id from bid request and set it in response
    auction_id =  requestDataDict['auction_id']  
    responseJsonTemplate['id'] = auction_id 

    # popupate bid price 
    bid = 0 
    print bottle.request.get_cookie("returnBidAmount")


    if ( 'userID' in requestDataDict ) :  # if request contains userID 
        # TODO : if network-userID key present in KV
        userID = requestDataDict['userID']
        userKV = memobj.getValue(userID)
        bid = userKV['returnBidAmount']
  
    elif (  bottle.request.get_cookie("returnBidAmount") ) :  # if return bid price present in bid request cookie , use it
        bid = bottle.request.get_cookie("returnBidAmount")

    else :  # return randon bid price  
        bid = random.uniform(1, 10)
 
    # set the bid in response 
    responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
 
    return responseJsonTemplate



def ifBuyerIdPresent ():
    pass 
     
#     responseBid = populate_bid_template(requestData,responseJson)

    # convert json to dictionary 
    # responseJsonTemplateDict = json.loads(responseJsonTemplate) 

    #print "is NOT instance of dict ",    isinstance(responseJsonTemplate, dict) 
    #print "is instance of dict ",    isinstance(responseJsonTemplate, dict) 



