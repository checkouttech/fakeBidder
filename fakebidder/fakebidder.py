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


def hello():
    print 'Hi, this is mymodule speaking.'

# End of mymodule.py

def is_valid_json(jsonVariable):
    try:
        json_object = json.loads(jsonVariable) 
    except ValueError, e:
        return False
    return True 



def dump_headers():
    headersDict = {}
    headersDict = bottle.request.headers
    #print bottle.request.get_header('host')
    #print bottle.request.headers.keys()
    #print bottle.request.headers['host']
    return dict ( headersDict ) 

def dump_cookies():
    cookiesDict = {}
    cookiesDict = bottle.request.cookies
    #print bottle.request.cookies.keys()
    #print bottle.request.get_cookie("cookieName")
    return dict ( cookiesDict)

def dump_data():
    dataDict = {}
    dataDict =  json.loads ( bottle.request.body.read() ) 
    return dataDict 

def get_bid_template():
    # get random bid amount just in case not provided 
#
#    bid = 0 
#    print bottle.request.get_cookie("returnBidAmount")
#
#    #print bottle.request.get_cookie("cookieName")
#
#    if (  bottle.request.get_cookie("returnBidAmount") ) :
#        bid = bottle.request.get_cookie("returnBidAmount")
#        print bid 
#    else :  
#        bid = random.uniform(1, 10)
#
    # if request contains userID
       # if network-userID key present in KV
       # get IT 

        #if ( mc.get(networkID"."userID) )   
        #mc.set(str(networkID)+""+str(userID),"this is value")
        #print mc.get(str(networkID)+""+str(userID))

    #  will eventually come from a yaml template file 

    responseJson = {
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
    return responseJson

#     responseBid = populate_bid_template(requestData,responseBidTemplate)
def populate_bid_template(requestData, responseJsonTemplate):
    global auction_id
    
    # convert json to a dictionary 
    requestDataDict = json.loads(requestData) 

    # convert json to dictionary 
    # responseJsonTemplateDict = json.loads(responseJsonTemplate) 

    print "is NOT instance of dict ",    isinstance(responseJsonTemplate, dict) 
    print "is instance of dict ",    isinstance(responseJsonTemplate, dict) 



    # populate aucation ID from request 
    auction_id =  requestDataDict['auction_id']  
    responseJsonTemplate['id'] = auction_id 

    # popupate bid price 
    bid = 0 
    print bottle.request.get_cookie("returnBidAmount")

    if ( 'userID' in requestDataDict )  :  # if request contains userID 
       # return bid price present in KV store , use it 
       ## print "this is the userID --------> ", userID
       # if request contains userID
         # if network-userID key present in KV
         # get IT 
      
       memcache_server = "192.168.150.110" 
       memcache_port = "11211"

       mc = memcache.Client(['192.168.150.110:11211'], debug=0)
       print "key from mc " , mc.get ("network_1.buyerkey_1001") 

       userKV = mc.get ("network_1.buyerkey_1001")
       bid = userKV['returnBidAmount']

  
       # if ( mc.get(networkID.userID) ): 
            #mc.set(str(networkID).str(userID),"this is value")
        #    print mc.get(str(networkID).str(userID))
         #   print "this is the userID --------> ", requestDataDict['userID']



    elif (  bottle.request.get_cookie("returnBidAmount") ) :  # if return bid price present in bid request cookie , use it
        bid = bottle.request.get_cookie("returnBidAmount")
        print bid 
    else :  # return randon bid price  
        bid = random.uniform(1, 10)

    responseJsonTemplate['seatbid'][0]['bid'][0]['price'] = bid 
 
    return responseJsonTemplate


def ifBuyerIdPresent ():
    pass 
    # if buyer user id present 
     
#     responseBid = populate_bid_template(requestData,responseJson)

    # check if key present 
    #if mc.get("
    # if present then get value and return 
    # else return false 

    # get
    # set
    # 
    # delete
   # stats 




