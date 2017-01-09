import urllib2, json

def getTags(url, accesstoken):
    u = urllib2.urlopen("https://api.clarifai.com/v1/tag?url="+url+"&access_token="+accesstoken)
    response = u.read()
    data = json.loads(response)
    return data["results"][0]["result"]["tag"]["classes"]
