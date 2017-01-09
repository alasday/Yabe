import urllib, urllib2, json, base64, time, hashlib, StringIO

def uploadPic (path, key, secret):
    #encode image
    with open(path, "rb") as image:
        encoded_image = base64.b64encode(image.read())
    utime = int(time.time())
    encoder = hashlib.sha1()
    encoder.update("timestamp=" + str(utime) + secret)
    datadict = {"file": "data:image/jpg;base64," + encoded_image,
                "api_key": "246477329826533",
                "timestamp": str(utime),
                "signature": encoder.hexdigest()
                }
    encodeddata = urllib.urlencode(datadict)
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = urllib2.Request("https://api.cloudinary.com/v1_1/dv5y12rxk/image/upload", encodeddata, headers)
    
    u = urllib2.urlopen(req)
    response = u.read()
    data = json.loads(response)
    return data["url"]
