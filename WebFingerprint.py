import requests, socket
from tld import get_tld
import ssl, OpenSSL

target_headers = [
    'Server', 'method', 
    'uid','id','user','username', 'q', 
    'password', 'pass', 'pin',
    'Via', 'X-Powered-By', 'X-Country-Code', 'cookie', 'set-cookie'
    ]

#region FUNCTIONS
result=dict()
url, req, domain='','',''
def geturl():
    global url, req, domain
    url=input("Url to fingerprint: ")
    domain=url
    if(not url.startswith(('http://','https://'))):
        url = 'http://'+url
    else:
        domain=domain.replace('https://','')
        domain=domain.replace('http://','')

    print("Connecting to",url,"...")
    try:
        req = requests.get(url, timeout=3)
        try:
            res = get_tld(url, as_object=True)
            print('got tld') #PROBLEM: FREEZES ON CERTAIN DOMAINS
            domain = res.domain
            domain= domain +'.'+str(res)
        except Exception as e:
            print(e)
            pass
    
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

def findHttpHeaders(req):
    #print("\nHeaders sent:\n",req.request.headers)
    print("\nHeaders received:\n",req.headers)
    #print("\nTargeted headers found:")
    for header in target_headers:
        try:
            h = req.headers[header]
            result[header]=h #print('%s: %s' % (header, h))
        except:
            pass #print('%s: Not found' % header)

def sslCheck(domain):
    try:
        # cert=ssl.get_server_certificate((target_ip,443))
        # x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        # data = x509.get_notAfter()
        # print(cert,'\n',x509,'\n',data,'\n')
        # #sslversion = ssl.OPENSSL_VERSION #NOTE: version of your OWN openssl
        
        context = ssl.create_default_context()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sslSocket = context.wrap_socket(s, server_hostname = domain)
        sslSocket.connect((domain, 443))
        sslversion=sslSocket.version()
        sslSocket.close()
    except:
        sslversion="NO SSL CERTIFICATE (N/A)"
    result['SSL_version']=sslversion

def Output():
    print("\nResults:")
    for key,value in result.items():
        print('%s: %s' % (key, value))

def WebPrint(req=req,domain=domain):
    sslCheck(domain)
    findHttpHeaders(req)
    Output()

#endregion

#RUN HERE
if __name__ == "__main__":
    geturl()
    sslCheck(domain)
    findHttpHeaders(req)
    Output()
