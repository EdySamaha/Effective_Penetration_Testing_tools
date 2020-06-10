#NOTE: THIS SCRIPT IS ONLY USEFUL IN ACCORDANCE WITH OTHER SCRIPTS
from bs4 import BeautifulSoup
import requests, random, string, time
from itertools import cycle #cycles through a set infinitely

#region FUNCTIONS
proxyPool= {"a",'b',1,'1',"1",2,2,"2",'2'} #set only keeps unique inputs, and is unordered
headerPool= set()

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


# def getRandom_Headers():
#     accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                 "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}
#     user-agent={}
    
#     try: 
#         # Getting a user agent using the fake_useragent package
#         ua = UserAgent()
#         if random.random() > 0.5:
#             random_user_agent = ua.chrome
#         else:
#             random_user_agent = ua.firefox
    
#             user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]  # Just for case user agents are not extracted from fake-useragent package
#         random_user_agent = random.choice(user_agents)
    
#     #It's important to match between the user-agent and the accept headers
#         valid_accept = accepts['Firefox'] if random_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
#         headers = {"User-Agent": random_user_agent,
#                 "Accept": valid_accept}
#         return headers

def generatePools():
    return

def hide_local(): #obfuscates your packets inside network
    return

def useTrafficMaze(function, delay=0, stopiter=10):
    itercounter=0
    for i in cycle(proxyPool):
        itercounter+=1
        execute = function()
        print(i)
        if (itercounter>=stopiter):
            break
        time.sleep(delay)

#endregion

#RUN HERE
if __name__ == "__main__":
    # getProxyPool()
    print(proxyPool)

    def ahmad():
        print('walaa')
    useTrafficMaze(ahmad, 1)
