# -*- coding: utf-8 -*-
import oauth2 as oauth
import httplib2 as httplib
import urllib

API_KEY = 'ApiKey'
API_SECRET = 'ApiSecret'

ZYNCRO_URL = 'https://my.sandbox.zyncro.com'
REQUEST_TOKEN_URL = ZYNCRO_URL + '/tokenservice/oauth/v1/get_request_token'
NO_BROWSER_AUTHORIZATION_URL = ZYNCRO_URL + '/tokenservice/oauth/v1/NoBrowserAuthorization'
ACCESS_TOKEN_URL = ZYNCRO_URL + '/tokenservice/oauth/v1/get_access_token'


def getRequestToken():
    consumer = oauth.Consumer(key=API_KEY, secret=API_SECRET)
    client = oauth.Client(consumer)
    resp, content = client.request(REQUEST_TOKEN_URL, "POST")
    
    tokens = content.split('&')
    token = tokens[0].split('=')[1]
    secret = tokens[1].split('=')[1]

    return oauth.Token(token, secret)    


def authorizeToken(username, password, requettoken):
    http = httplib.Http()   
    body = {'username': username, 'password': password, 'request_token': requettoken }
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(NO_BROWSER_AUTHORIZATION_URL, 'POST', headers=headers, body=urllib.urlencode(body));


def getAccessToken(requesttoken):
    consumer = oauth.Consumer(key=API_KEY, secret=API_SECRET)
    client = oauth.Client(consumer, requesttoken)
    resp, content = client.request(ACCESS_TOKEN_URL, 'POST')
    
    tokens = content.split('&')
    token = tokens[0].split('=')[1]
    secret = tokens[1].split('=')[1]

    return oauth.Token(token, secret)


def getAccessTokenForUser(username, password):
    requesttoken = getRequestToken()
    authorizeToken(username, password, requesttoken.key)
    return getAccessToken(requesttoken)


def getMainFeed(accesstoken):
    consumer = oauth.Consumer(key=API_KEY, secret=API_SECRET)
    client = oauth.Client(consumer, accesstoken)
    
    parameters = {'itemsPerPage' : '10'}
    resp, content = client.request(ZYNCRO_URL + '/api/v1/rest/wall', 'GET', parameters)
    return content


def publishOnPersonalFeed(accesstoken):
    consumer = oauth.Consumer(key=API_KEY, secret=API_SECRET)
    client = oauth.Client(consumer, accesstoken)
    
    parameters = {'comment' : u'Hello world, Zyncro!'}    
    resp, content = client.request(ZYNCRO_URL + '/api/v1/rest/wall/personalfeed', 'POST', parameters)    
    return content


username = 'Email'
password = 'Password'

# Get an Access token for a user
accesstoken = getAccessTokenForUser(username, password)

# Get the main Microblogging for a user
print 'Main feed: ' + getMainFeed(accesstoken)

# Publish a new message in User's Personal feed
print 'New Event published: ' + publishOnPersonalFeed(accesstoken)