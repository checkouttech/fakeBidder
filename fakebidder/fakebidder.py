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

    bid = 0 
    print bottle.request.get_cookie("returnBidAmount")

    #print bottle.request.get_cookie("cookieName")
    if (  bottle.request.get_cookie("returnBidAmount") ) :
        bid = bottle.request.get_cookie("returnBidAmount")
        print bid 
    else :
        bid = random.uniform(1, 10)

    responseJson = {
           "id": "auctionId",
           "seatbid": [ {
                 "seat":"testseat",
                 "bid": [ {
                         "id": "required id per 4.3.3",
                         "impid": "impid per 4.3.3",
                         "adomain": [ "gawker" ],
                         "price": bid,
                         "ext": { "creativeapi": 3 },
                         "adm": "<img src=\"http://www.foo.com/wp-content/themes/foo/images/ftr_icon.png?auction=${AUCTION_ID}&price=${AUCTION_PRICE:BF}\">",
                         "crid": "12345678"
                        } ]
                      } ]
         }
    return responseJson


def populate_bid_template(requestData, responseJson):
    global auction_id
    requestDataJson = json.loads(requestData) 
    auction_id =  requestDataJson['auction_id']  
    responseJson['id'] = auction_id    
    return responseJson


