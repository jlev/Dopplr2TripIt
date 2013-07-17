import os
import pickle
import tripit

CREDENTIAL_CACHE = '.credential_cache'

def get_tripit_credentials():
    #application keys
    consumer_key  = '827519bc029183f4cdf42796c0ba46408c4c1b62'
    consumer_secret = '1bf57df390fb985d4c6210d72a9fa90afb025bc7'

    #try to load tokens from cache
    if os.path.exists(CREDENTIAL_CACHE):
        cache = pickle.load(open(CREDENTIAL_CACHE,'r'))
    else:
        cache = {}

    if cache.has_key('access_token'):
        #we have already authorized the app
        access_token = cache['access_token']
    else:
        #get request token
        api_credentials = tripit.OAuthConsumerCredential(consumer_key, consumer_secret)
        t = tripit.TripIt(api_credentials, api_url='https://api.tripit.com')
        request_token = t.get_request_token()

        #open url in browser and authorize
        url = 'https://www.tripit.com/oauth/authorize?oauth_token='+ request_token['oauth_token']+'&oauth_callback=http%3A%2F%2Fwww.tripit.com%2Fhome'
        print "open "+url+" and authorize the app"
        done = raw_input('Hit enter when complete: ')

        #get valid access token from request
        oauth_credential = tripit.OAuthConsumerCredential(consumer_key, consumer_secret,
            request_token['oauth_token'], request_token['oauth_token_secret'])
        t = tripit.TripIt(oauth_credential, api_url='https://api.tripit.com')
        access_token = t.get_access_token()
        
        #save to cache
        print "saving",access_token
        cache['access_token'] = access_token
        pickle.dump(cache, open(CREDENTIAL_CACHE,'w'))
    
    valid_token = tripit.OAuthConsumerCredential(consumer_key, consumer_secret,
        access_token['oauth_token'], access_token['oauth_token_secret'])
    return valid_token

def load_dopplr_file():
    username = raw_input('Dopplr Username: ')
    f = open('export-%s/full_data.json' % username,'r')
    data = json.loads(f.read())
    return data

def post_to_tripit(api,dopplr_trip):
    xml_template = """<Request>
  <Trip>
    <start_date>%s</start_date>
    <end_date>%s</end_date>
    <primary_location>%s</primary_location>
    <PrimaryLocationAddress>
        <city>%s</city>
        <country>%s</country>
        <latitude>%f</latitude>
        <longitude>%f</longitude>
    </PrimaryLocationAddress>
  </Trip>
</Request>"""
    city_name = dopplr_trip['city']['name'].encode('ascii', 'ignore')
    #because TripIt doesn't like unicode

    if dopplr_trip['city'].has_key('region'):
        #probably domestic
        state = dopplr_trip['city']['region']
        location_name = "%s, %s" % (city_name, state)
    else:
        location_name = "%s, %s" % (city_name, dopplr_trip['city']['country'])

    xml_data = xml_template % \
       (dopplr_trip['start'],
        dopplr_trip['finish'],
        location_name,
        city_name,
        dopplr_trip['city']['country_code'],
        dopplr_trip['city']['latitude'],
        dopplr_trip['city']['longitude'])

    response = api.create(xml_data)

    if response.has_error():
        print "ERROR"
        err = response.get_children()[0]
        for att in err.get_attribute_names():
            print att, err.get_attribute_value(att)
        return None
    
    return response

def main():
    credentials = get_tripit_credentials()
    tripit_api = tripit.TripIt(credentials, api_url='https://api.tripit.com')

    d = load_dopplr_file()
    for trip in d['trips']:
        print "loading trip to %s from %s to %s via %s" % \
            (trip['city']['name'],
             trip['start'],trip['finish'],
             trip['outgoing_transport_type'])
        result = post_to_tripit(tripit_api,trip)
        if result:
            print "posted"

if __name__=="__main__":
    main()