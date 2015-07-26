import json
import os
from bottle import route, run, static_file

config_file = open( 'config.json' )
config_data = json.load( config_file )
pth_xml     = config_data["paths"]["xml"]

@route('/recipes/<name>', method='GET')
def recipe_show( name="" ):
    if "" != name:
        return static_file( name, pth_xml  )
    else:
        return { "success" : False, "error" : "show called without a filename" }


run(host='localhost', port=8080, debug=True)
