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
import argparse 
import ConfigParser
import socket
import time
import statsd    
 


global mylogger

os.putenv('PYTHONUNBUFFERED', 'enabled')
sys.stdout.flush()

##  Classes 

class memcacheConnection():
    def __init__(self,memcache_host,memcache_port):

        print "initializing memcache" 
        print "memcache_host-->" , memcache_host ,  "  memcache_port " , memcache_port
        memcache_details = memcache_host  +":"+ memcache_port
        self.connection = memcache.Client([memcache_details], debug=0)
     
    def setValue(self,key,value):
        self.connection.set(key,value)
        print "setting memcache value - ", key ," : ", value
   
    def getValue(self,key):
        key = str(key) 
        value = self.connection.get(key)
        print "reading memcache value - ", key ," : ", value
        return value 


class setupClass():

    #args = ""

    def __init__(self):
        self.args = self.parse_arguments()
    
        # declaring global object for memcache # TODO do same for logger
        global memobj 
        memobj = memcacheConnection(self.args.memcache_host, self.args.memcache_port) 

        #global mylogger
        #mylogger = mycustomelogger()


    def parse_arguments(self):
        
        #global args 
        conf_parser = argparse.ArgumentParser(
            # Turn off help, so we print all options in response to -h
                add_help=False
                )
        conf_parser.add_argument("-c", "--conf_file", help="Specify config file", metavar="FILE")
     
        args, remaining_argv = conf_parser.parse_known_args()
        
        print "remaining_argv ...", remaining_argv
        
        defaults = {}
    
        if args.conf_file:
            config = ConfigParser.SafeConfigParser()
            config.read([args.conf_file])
            defaults = dict(config.items("Defaults"))
           
        # Don't surpress add_help here so it will handle -h
        parser = argparse.ArgumentParser(
            # Inherit options from config_parser
            parents=[conf_parser],
            # print script description with -h/--help
            description=__doc__,
            # Don't mess with format of description
            formatter_class=argparse.RawDescriptionHelpFormatter,
            ) 
            
        parser.set_defaults(**defaults)
        parser.add_argument('-p','--port',action="store",  help='Port for fake bidder', required=True, type=int )
        parser.add_argument('-dl','--debug_log_filename',action="store",  help='Debug log filename')
        parser.add_argument('-rl','--records_log_filename',action="store",  help='Records log filename')
        #parser.add_argument('-p','--port',action="store",  help='Port for fake bidder', type=int )
        args = parser.parse_args(remaining_argv)
        print args
        return args
    





 
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


class graphiteClass(object):

    def __init__(self,setupObj):
        statsd_host = setupObj.args.statsd_host
        statsd_port = setupObj.args.statsd_port 

        # memobj = memcacheConnection(self.args.memcache_host, self.args.memcache_port) 
        print "initializing statsd connection" 
        print "statsd_host-->" , statsd_host ,  "  statsd_port " , statsd_port
        self.connection = None
        try:
            self.connection = statsd.StatsClient(
               host = statsd_host, 
               port = statsd_port)
    
        except:
            print "Couldn't connect to %(server)s on port %(port)d" % {'server':statsd_host, 'port':statsd_host}
 



class loggerClass(object):

    def __init__(self,setupObj):
        debug_log_filename = setupObj.args.debug_log_filename
        debug_log_level    = setupObj.args.debug_log_level
        debug_log_format   = setupObj.args.debug_log_format


        self.debugLogger = logging.getLogger("debug_log")
        self.debugLogger.setLevel(logging.DEBUG)
 
        # create console handler and set level to info
        handler = logging.FileHandler(debug_log_filename)
        handler.setLevel(logging.getLevelName(debug_log_level))
        formatter = logging.Formatter(debug_log_format)
        handler.setFormatter(formatter)
        self.debugLogger.addHandler(handler)


        records_log_filename =  setupObj.args.records_log_filename
        records_log_level    = setupObj.args.records_log_level
        records_log_format   = setupObj.args.records_log_format

        self.recordsLogger = logging.getLogger("records_log")
        self.recordsLogger.setLevel(logging.DEBUG)
        # create console handler and set level to info
        handler = logging.FileHandler(records_log_filename)
        handler.setLevel(logging.getLevelName(records_log_level))
        formatter = logging.Formatter(records_log_format)
        handler.setFormatter(formatter)
        self.recordsLogger.addHandler(handler)

    def log_records(self,bidresponse):
        # log info 
        network_id = "fb1"
        metric_name =   'fakebidder.'+  network_id + '.sum_bids_received'  

        id = bidresponse.bidResponse['id']
        bidAmount = bidresponse.bidResponse['seatbid'][0]['bid'][0]['price']
       
        #global mylogger
        self.recordsLogger.info(id +","+ str(bidAmount)) 



###
###def mycustomelogger():
###
###    #create logger with "spam_application"
###    logger = logging.getLogger("main")
###    logger.setLevel(logging.DEBUG)
###    
###    #create file handler and set level to debug
###    fh = logging.FileHandler("spam.log")
###    fh.setLevel(logging.DEBUG)
###    
###    #create formatter
###    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -  %(message)s")
###    #add formatter to fh
###    fh.setFormatter(formatter)
###    
###    #add fh to logger
###    logger.addHandler(fh)
###    
###    logging.basicConfig(  stream=sys.stdout, 
###                      level=logging.INFO,
###                      format= '[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} - %(message)s',
###                      datefmt='%H:%M:%S')
###    
###    return logging 
###    #return logger 
###    







###
###def graphitelogger(setupObj):
###    #feedGraphite
###
###    ### graphite thingy 
###    STATSD_SERVER = '192.168.150.104'
###    STATSD_PORT = 8125
###    
###    network_id = "fb1"
###    metric_name =   'fakebidder.'+  network_id + '.sum_bids_received'  
###    c = None  
###
###    try:
###        c = statsd.StatsClient(
###           host = STATSD_SERVER, 
###           port = STATSD_PORT)
###
###        #c.incr(metric_name, count=500)
###    except:
###        print "Couldn't connect to %(server)s on port %(port)d" % {'server':STATSD_SERVER, 'port':STATSD_PORT}
###        #sys.exit(1)
###    finally:
###        pass     
###      
###    print  metric_name
###    return c 
###


## Declaring global objects


def hello():
    print 'Hi, this is mymodule speaking.'


def is_valid_json(jsonVariable):
    try:
        json_object = json.loads(jsonVariable) 
    except ValueError, e:
        return False
    return True 

# End of mymodule.py

def ifBuyerIdPresent ():
    pass 

