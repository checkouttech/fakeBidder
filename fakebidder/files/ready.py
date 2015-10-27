import yaml
import json

with open('response_templates.yaml', 'r') as f:
    responsedict = yaml.load(f)

print responsedict
print json.dumps(responsedict["responseTemplate"],indent=2)

        #testcase_data_json = json.dumps(testdict["default_template"]["data"],indent=2)    

template2match  = {
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



def findDiff(d1, d2, path=""):
    print "======= top level keys for d1 " , d1.keys()
    print "======= top level keys for d2 " , d2.keys()
    for k in d1.keys():
        print " top level checking for key ", k

        if not d2.has_key(k):
            print path, ":"
            print k + " as key not in d2", "\n"
        else:
            if type(d1[k]) is dict:
                if path == "":
                    path = k
                else:
                    path = path + "->" + k
                findDiff(d1[k],d2[k], path)
            else:
                if d1[k] != d2[k]:
                    print path, ":"
                    print " - ", k," : ", d1[k]
                    print " + ", k," : ", d2[k]



findDiff ( template2match, responsedict["responseTemplate"])

