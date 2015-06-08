import requests
import json
import urllib
import pprint
import uuid
import sys
from urlparse import urlparse, parse_qs

# OAuth endpoints given in the Facebook API documentation
random_uuid = str(uuid.uuid4())
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
redirect_uri = 'https://%s.happn.com/' % random_uuid

url = 'https://www.facebook.com/dialog/oauth?'
params = {
  'client_id' : '247294518656661',
  'redirect_uri' : redirect_uri,
  'scope' : 'user_birthday,email,user_likes,user_about_me,user_photos,user_work_history,user_friends',
  'response_type' : 'token'
}

print "Please go to: %s?%s" % ( authorization_base_url, urllib.urlencode(params) )

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')


# Parse the redirect response for the access_token
o = urlparse(redirect_response)

access_token = parse_qs(o.fragment)['access_token'][0]



# client_id and client_secret can be obtained from a decompiled
# happn\smali\com\ftw_and_co\happn\network\services\FacebookService.smali
data = {
  'client_id' :  'FUE-idSEP-f7AqCyuMcPr2K-1iCIU_YlvK-M-im3c',
  'client_secret' :  'brGoHSwZsPjJ-lBk0HqEXVtb3UFu-y5l_JcOjD-Ekv',
  'grant_type' : 'assertion',
  'assertion_type' : 'facebook_access_token',
  'assertion' : access_token,
  'scope' : 'mobile_app'
}

url = 'https://connect.happn.fr/connect/oauth/token'

r = requests.post(url, data=data)

user_info = r.json()


print "Obtained user information: %s" % user_info


query = {
  "types" : "468",
  "limit" : 16,
  "offset" : 0,
  "fields": "id,modification_date,notification_type,nb_times,notifier.fields(id,job,is_accepted,workplace,my_relation,distance,gender,is_charmed,nb_photos,first_name,age,profiles.mode(1).width(360).height(592).fields(width,height,mode,url))"
}

querystring = json.dumps(query)

headers = {
    'Host' : 'api.happn.fr',
    'User-Agent' : 'okhttp/2.3.0',
    'http.useragent' : 'Happn/18.2.0 AndroidSDK/22',
    'Authorization' : 'OAuth="%s"' % user_info['access_token'],
    'Content-Type' : 'application/json'
}

data = {
  'query' : urllib.quote_plus(querystring)
}


url = "https://api.happn.fr/api/users/6799798589/notifications/"

r = requests.get(url, data=data, headers=headers)

notifications = r.json()

for info in notifications['data']:
    #print info['notifier']['first_name'], info['notifier']['last_name']
   
    my_user_id = user_info['user_id']
    target_user_id = info['notifier']['id']
    print "Liking user %s - %s" % (target_user_id, info['notifier']['first_name'])
    url = "https://api.happn.fr/api/users/%s/accepted/%s" % (my_user_id, target_user_id)

    r = requests.post(url, data=data, headers=headers)
    print r.text
