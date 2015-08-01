import json
import os
#import requests
#from bottle import route, run, request
import bottle
import random 

@bottle.route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


def is_valid_json(jsonVariable):
    try:
        json_object = json.loads(jsonVariable) 
    except ValueError, e:
        return False
    return True 


def get_bid_template():

    # get random bid amount just in case not provided 
    # var bid = parseFloat(parseInt(Math.random()*10) + "." + parseInt(Math.random()*100000));

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

    # print requestData.keys()  
    requestDataJson = json.loads(requestData) 
    auction_id =  requestDataJson['auction_id']  
    print auction_id 
    #return auction_id 
    #responseDataJson = json.loads(responseJson) 
    #print responseDataJson['id']
    print responseJson
    responseJson['id'] = auction_id    
    print requestData 
    print responseJson
    return responseJson





@bottle.route('/fakebidder/', method='POST')
def recipe_save() :
    print "got something"
  

    requestData = bottle.request.body.read()

    #check if valid json 
    if ( is_valid_json(requestData)) :
        postdata = bottle.request.body.read()
    else:
        return "ERROR: bad JSON"
     
    responseJson = get_bid_template()

    responseBid = populate_bid_template(requestData,responseJson) 


    return responseBid
    #return postdata








bottle.run(host='0.0.0.0', port=10001)




# todo 
# insert everything in try / catch 
# check for json 
# 

