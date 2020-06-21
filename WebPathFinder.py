from bs4 import BeautifulSoup
import requests ,socket
import re, string, sys
from tld import get_tld #needs url with http://

wordlist='defaultPathWordlist.txt' #Change this string for different file name or path

#region FUNCTIONS
url, req, ip, domain ='','','',''
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
		'Accept': '*/*'}
internal = []
referral = []
hiddenpaths=[]

def geturl():
    global url, req, ip, domain
    url = input("Please enter a URL: ")
    if(not url.startswith(('http://','https://'))):
        url = 'http://'+url
        
    print("Connecting to",url,"...")
    try:
        #print(socket.gethostbyaddr(url)) #returns url from ip address #PROBLEM: gets a weird server url instead of hostname that we want
        req = requests.get(url, timeout=3)
        try: #get domain and IP
            res = get_tld(url, as_object=True)
            domain = res.domain
            temp= domain +'.'+str(res)
            ip= socket.gethostbyname(temp)  #needs input without http:// and with only domain
            print(temp,ip)
        except Exception as e:
            domain="NOT FOUND"
            ip="Result"
            print(e)

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to",url)
        geturl()
        return
        #exit() #quits script but keeps console open
    except requests.exceptions.Timeout:
        print("Error: Connection timeout")
        exit()
    except:
        print("Please enter a valid url")
        geturl()
        return


def extractLinks(req):
    soup = BeautifulSoup(req.content, "html.parser")
    for link in soup.findAll('a'):
        if link.get('href') is None:
            continue
        else:
            x = re.search("^/", link.get('href'))
            if x is None:       # if the link does not start with '/'
                if link.get('href') not in referral: #avoid dups
                    referral.append(link.get('href'))
            else:
                if link.get('href') not in internal:
                    internal.append(link.get('href'))

def dirBruteForce(url, wordlist=wordlist):
    if url[-1]!='/':
        url+='/'
    with open(wordlist, 'r') as f:
        for line in f:
            testurl = url + line.replace('\n', "")
            #print(testurl)
            try:
                testurl = requests.get(testurl, headers=headers, timeout=3)
                if testurl.status_code ==200:
                    hiddenpaths.append(line.replace('\n', ""))
            except:
                continue

def Output():
    f = open(ip+"_paths.txt", "w")
    f.write("Url: "+url+"\nDomain: "+domain+"\nIP: "+ip+'\n')
    f.write("\nInternal links:\n")
    for i in internal:
        f.write(i+'\n')
    f.write("\nReferal links:\n")
    for i in referral:
        f.write(i+'\n')
    f.write("\nHidden paths found:\n")
    for i in hiddenpaths:
        f.write(i+'\n')

    f.close()

def WebPaths(req,dirBruteForce=False):
    extractLinks(req)
    if(dirBruteForce):
        dirBruteForce(url)
    Output()
#endregion

#RUN HERE
if __name__ == "__main__":
    geturl()

    print("Getting links...")
    extractLinks(req)
    print("\nINTERNAL:")
    print(internal)
    print("\nREFERRAL: ")
    print(referral)

    q= input("\nSearch for hidden paths? (NOT Recommended) yes[1]/no[0]: ").lower()
    q= ''.join(e for e in q if(e not in string.whitespace and e not in string.punctuation))
    if (q=="yes" or q=="y" or q=="1"):
        q= input("\nWARNING: Trying to brute force directories and files names on deployed servers is ILLEGAL!\nDo you still wish to continue? (AT YOUR OWN RISK) Yes/No: ").lower()
        q= ''.join(e for e in q if(e not in string.whitespace and e not in string.punctuation))
        if (q=="yes"):
            searchHidden=True
        else:
            searchHidden=False
    else:
        searchHidden=False
    print(searchHidden)

    if(searchHidden):
        dirBruteForce(url, wordlist)
        print(hiddenpaths)

    Output()
