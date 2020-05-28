from bs4 import BeautifulSoup
import requests #,socket
import re, string

url, soup ='',''
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
		'Accept': '*/*'}
internal = []
referral = []
hiddenpaths=[]

#region FUNCTIONS
def geturl():
    global url, soup
    url = input("Please enter a URL: ")
    if(not url.startswith(('http://','https://'))):
        url = 'https://'+url
    #print(url)
    try:
        #print(socket.gethostbyaddr(url)) #returns url from ip address #PROBLEM: gets a weird server url instead of hostname that we want
        page = requests.get(url, timeout=3)
        soup = BeautifulSoup(page.content, "html.parser")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the website")
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


def extractLinks(URL):
    for link in soup.findAll('a'):
        if link.get('href') is None:
            continue
        else:
            x = re.search("^/", link.get('href'))
            if x is None:
                referral.append(link.get('href'))
            else:
                internal.append(link.get('href'))

def dirBruteForce(url, wordlist):
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
#endregion

#RUN HERE
wordlist='defaultPathWordlist.txt' #Change this string for different file name or path
geturl()

print("Getting links...")
extractLinks(url)
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

