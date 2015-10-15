import json
import os
#import requests
#from bottle import route, run, request
import bottle

@bottle.route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


@bottle.route('/fakebidder/', method='POST')
def recipe_save() :
    print "got something"
    postdata = bottle.request.body.read()
    return postdata

bottle.run(host='0.0.0.0', port=10009)

