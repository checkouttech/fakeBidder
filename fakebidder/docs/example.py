 
    ##print bottle.request.json
    ##return bottle.request.json

    #data = json.load(requests.body)
    #print "data", data
    #response = data['site']
#  curl -i -X GET  -d '{"username": "fooba", "password": "1234"}' http://localhost:8080/recipes/a
    #print  response






#  curl -i -X GET  -d '{"username": "fooba", "password": "1234"}' http://localhost:8080/recipes/a
#
#@route('/fakebidder/', method='GET')
#def recipe_save() :
#    print "got something"
#    data = json.load(request.body)
#    print "data", data
#    response = data['site'] 
#    print  response 	
#    return response
#
#
#        return { "success" : False, "error" : "save called without a filename or content" }
#
#
##
#
#    if "" != name and "" != xml:
#        with open( os.path.join( pth_xml, name + ".xml" ), "w" ) as f:
#            f.write( xml )
#        return { "success" : True, "path" : name }
#    else:
#

#@route('/fakebidder/', method='GET')
#def recipe_save() :
#    print "got something"
#    data = json.load(request.body)
#    print "data", data
#    response = data['site'] 
#    print  response 	
#    return response


#
#@route('/hello')
#def hello():
#    return "Hello World!"
#
#


#
#@route('/recipes/')
#def recipes_list():
#    return "LIST"
#
#@route('/recipes/<name>', method='GET')
#def recipe_show( name="Mystery Recipe" ):
#    return "SHOW RECIPE " + name
#
#@route('/recipes/<name>', method='DELETE' )
#def recipe_delete( name="Mystery Recipe" ):
#    return "DELETE RECIPE " + name
#
#@route('/recipes/<name>', method='PUT')
#def recipe_save( name="Mystery Recipe" ):
#    return "SAVE RECIPE " + name
#
#
#
#import json
#import os
#from bottle import route, run, request
#
##config_file = open( 'config.json' )
##config_data = json.load( config_file )
##pth_xml     = config_data["paths"]["xml"]
#
##  curl -i -X GET  -d '{"username": "fooba", "password": "1234"}' http://localhost:8080/recipes/a
#
#@route('/recipes/<name>', method='GET')
#def recipe_save( name="" ):
#    data = json.load(request.body)
#    print "data", data
#    #xml = request.forms.get( "xml" )
#    #accept=request.headers.get("Accept")
#    #data = request.body.read()
#    #print bottle.request.body.read() 
#    #data = request.GET.read('key')
#    #print request.GET.get()
#    #print accept
#    #print data
#
#    response = data['site'] 
#    print  response 	
#
#
#    return data
#

##
##
##    if "" != name and "" != xml:
##        with open( os.path.join( pth_xml, name + ".xml" ), "w" ) as f:
##            f.write( xml )
##        return { "success" : True, "path" : name }
##    else:
##        return { "success" : False, "error" : "save called without a filename or content" }
##
