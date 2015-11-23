#!/usr/bin/env python

import bottle

@bottle.route('/') 
def index():
    return '<b>Hello world!</b>' 

@bottle.route('/requestdetails', method='POST')
def print_request_details():

     print "headers ----> ", dict( bottle.request.headers )
     print "cookies ----> ", dict( bottle.request.cookies )
     print "body -------> ", bottle.request.body.read()

    #quiet=True to suppress info message on every request 
bottle.run(host='0.0.0.0', port=23456)

  

