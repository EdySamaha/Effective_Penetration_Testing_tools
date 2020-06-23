#NOTE: THIS SCRIPT IS ONLY USEFUL IN ACCORDANCE WITH OTHER SCRIPTS
from bs4 import BeautifulSoup
import requests, random, string, time
from itertools import cycle #cycles through a set infinitely

#region FUNCTIONS
proxyPool= set() #set only keeps unique inputs, and is unordered

accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}
useragent=[
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/5'
]

def getProxyPool():
    url = 'https://www.sslproxies.org/'    
    try:
        #with requests.Session() as res: #'with' is used here in order to automatically close the session when done
        proxies_page = requests.get(url)
        
        soup = BeautifulSoup(proxies_page.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
  
        for row in proxies_table.tbody.find_all('tr'):
            proxyPool.add('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string)) #(IP:port)
        return
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print("Error: can't get Proxy Pool\n",e)
        q= input("\nRetry: yes[1]/no[0]: ").lower()
        q= ''.join(e for e in q if(e not in string.whitespace and e not in string.punctuation))
        if (q=="yes" or q=="y" or q=="1"):
            getProxyPool()
            return


def getRandom_Headers():
    rand_useragent= random.choice(useragent)
    # #It's important to match between the user-agent and the accept headers
    valid_accept = accepts['Firefox'] if rand_useragent.find('Firefox') > 0 else accepts['Safari, Chrome']
    headers = {"User-Agent": rand_useragent,
            "Accept": valid_accept}
    return headers


def hide_local(proxy,headers): #obfuscates your packets inside network
    return

def useTrafficMaze(function, args=(), kwargs={}, delay=0, stopiter=10):
    getProxyPool()
    itercounter=0
    for i in cycle(proxyPool):
        headers=getRandom_Headers()
        itercounter+=1
        try:
            execute = function(*args,**kwargs, proxy=i,headers=headers)
        except:
            print("WARNING: Proxy unable to reach target. Using random headers only.")
            execute = function(*args,**kwargs, proxy='',headers=headers)
        # print(i,'\n',headers)
        if (itercounter>=stopiter):
            break
        time.sleep(delay)

#endregion

#RUN HERE
if __name__ == "__main__":
    useTrafficMaze(hide_local)
