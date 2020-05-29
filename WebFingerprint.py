import requests

target_headers = [
    'Server', 'uid','id','user','username', 'q', 
    'password', 'pin',
    'Via', 'X-Powered-By', 'X-Country-Code'
    ]

#region FUNCTIONS
url, req='',''
def findHttpHeaders(url):
    print("Headers found:\n",req.headers)
    print("\nTargeted headers found:")
    for header in target_headers:
        try:
            result = req.headers[header]
            print('%s: %s' % (header, result))
        except:
            pass #print('%s: Not found' % header)

def geturl():
    global url, req
    url=input("Url to fingerprint: ")
    if(not url.startswith(('http://','https://'))):
        url = 'https://'+url
    print("Connecting to",url,"...")
    try:
        req = requests.get(url, timeout=3)
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to",url)
        geturl()
        return
    except requests.exceptions.Timeout:
        print("Error: Connection timeout")
        exit()
    except:
        print("Please enter a valid url")
        geturl()
        return

#endregion

#RUN HERE
geturl()
findHttpHeaders(url)