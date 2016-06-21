import json
import os
import random
import urllib2

KEY = os.environ['DATAPOINT_KEY']
GET_ALL_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/all?res=3hourly&key=" + KEY

if os.environ.has_key('HTTP_PROXY'):
    proxy = urllib2.ProxyHandler({'http': os.environ['HTTP_PROXY']})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)


PARAM_INDEXES = {
    "uv":0,
    "temp":1,
    "wind_speed":2,
    "precip_prob":3,
    "humidity":4,
    "wind_gust":5
}

def feels_like_temp_training_set():
    X, Y = [], []
    print "Grabbing 3 hourly weather forecast from Met Office datapoint"
    req = urllib2.Request(url=GET_ALL_URL)
    res = urllib2.urlopen(req)
    data = json.load(res)

    # Grab all the numeric weather parameters to make our feature vector x and put in to the collection X
    # Grab the feels like temp and stick it in our collection Y, this is what we are aiming to guess.
    for i, loc in enumerate(data['SiteRep']['DV']['Location']):
        for period in loc['Period']:
            for rep in period['Rep']:
                X.append([
                    float(rep['U']),
                    float(rep['T']),
                    float(rep['S']),
                    float(rep['Pp']),
                    float(rep['H']),
                    float(rep['G'])
                ])
                Y.append(float(rep['F']))

    return X, Y