import json
import os
from bottle import route, run, request

config_file = open( 'config.json' )
config_data = json.load( config_file )
pth_xml     = config_data["paths"]["xml"]

@route('/recipes/<name>', method='PUT')
def recipe_save( name="" ):
    xml = request.forms.get( "xml" )
    if "" != name and "" != xml:
        with open( os.path.join( pth_xml, name + ".xml" ), "w" ) as f:
            f.write( xml )
        return { "success" : True, "path" : name }
    else:
        return { "success" : False, "error" : "save called without a filename or content" }

run(host='localhost', port=8080, debug=True)

