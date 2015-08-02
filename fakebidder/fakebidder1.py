import json
import os
#import requests
#from bottle import route, run, request
import bottle
import random 



##########
# Global variable 
#########

#global auction_id

########## 
# Functions , TODO :  Will be moved to a module 
##########


# TODO : return it as a dictionary and not a string 
def dump_headers():
    headersDict = {}
    headersDict = bottle.request.headers
    result = ["%s: %s" % (x, bottle.request.headers[x]) for x in bottle.request.headers.keys()]
    #print bottle.request.get_header('host')
    #print bottle.request.headers.keys()
    #print bottle.request.headers['host']
    return result 

# TODO : return it as a dictionary and not a string 
def dump_cookies():
    result = ["%s: %s" % (x, bottle.request.cookies[x]) for x in bottle.request.cookies.keys()]
    result.append('\n')
    #print bottle.request.cookies.keys()
    #print bottle.request.get_cookie("cookieName")
    return result


# TODO : return it as a dictionary and not a string 
def dump_data():
    result = bottle.request.body.read() 
    return result
 
def is_valid_json(jsonVariable):
    try:
        json_object = json.loads(jsonVariable) 
    except ValueError, e:
        return False
    return True 


def get_bid_template():
    # get random bid amount just in case not provided 
    # var bid = parseFloat(parseInt(Math.random()*10) + "." + parseInt(Math.random()*100000));

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


#############
# End points 
############

@bottle.route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


@bottle.route('/requestdetails', method='POST')
def print_request_details():
    requestDetails = {}
    requestDetails['headers'] = {}
    requestDetails['headers'] =  dump_headers()
    requestDetails['cookies'] =  dump_cookies()
    requestDetails['data']    =  dump_data()
    bottle.response.content_type = 'application/json'
    return requestDetails 
   

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
    
    print "DSP Response : id : ", auction_id ," : " , responseBid

    return responseBid








bottle.run(host='0.0.0.0', port=10001)

