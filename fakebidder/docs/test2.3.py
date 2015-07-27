import json
from bottle import route, run

config_file = open( 'config.json' )
config_data = json.load( config_file )
print config_data
pth_xml     = config_data["paths"]["xml"]


@route('/recipes/')
def recipes_list():
    return { "success" : False, "paths" : [], "error" : "list not implemented yet" }

@route('/recipes/<name>', method='GET')
def recipe_show( name="Mystery Recipe" ):
    return { "success" : False, "path" : pth_xml +name +".xml", "error" : "show not implemented yet" }

@route('/recipes/<name>', method='DELETE' )
def recipe_delete( name="Mystery Recipe" ):
    return { "success" : False, "error" : "delete not implemented yet" }

@route('/recipes/<name>', method='PUT')
def recipe_save( name="Mystery Recipe" ):
    return { "success" : False, "path" : pth_xml +name +" .xml", "error" : "save not implemented yet" }

run(host='localhost', port=8080, debug=True)


