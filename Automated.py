import os, platform, subprocess
import requests, socket #, threading, sys
import re #, string
from datetime import datetime
from tld import get_tld
#From custom scripts
from TrafficMaze import useTrafficMaze
from PortScanner import threadScanPorts
from WebFingerprint import WebPrint
from WebPathFinder import WebPaths
from WebInputTest import WebInputs

#region CONFIGURATION_BOOLS
"""Configure the bools below to run the appropriate automated scripts
   True= Run; False= Ignore"""
# Anonymity
_trafficMask=False
# Recon
_portscan=True
_webfingerprint=True
_webPathscan=True
_dirBruteForce=False #WARNING: brute forcing on deployed servers is ILLEGAL and can get you in trouble.
# Exploitation
_webinputTest=True

#endregion

#region Target_info
target_url,target_ip,domain,req='','','',''
def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    num_packets = '-n' if platform.system().lower()=='windows' else '-c' #-n/-c packet number
    size_packets= '-l' if platform.system().lower()=='windows' else '-s' #-l/-s byte size
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', num_packets,'1',size_packets,'1', host]
    
    rstatus, response_ip= subprocess.getstatusoutput(command)     #rstatus= subprocess.call(command)
    response_ip = re.search('Reply from (.*):', response_ip).group(1)
    print(rstatus, response_ip)
    if(rstatus==0 and response_ip==host): #avoid another ip responding with target unreachable
        return True
    else:
        return False    


def getTarget():
    global target_url,target_ip, domain, req
    target_url= input('Enter target IP or Hostname: ')
    #Filtering Target
    target=target_url
    if(target.startswith(('http://','https://'))):
        target=target.replace('https://','')
        target=target.replace('http://','')
    else:
        target_url= 'http://'+target_url
    
    domain=target
    req=target_url

    #Getting target_ip
    try: #get IP from domain
        res = get_tld(target_url, as_object=True)
        domain = res.domain
        temp= domain +'.'+str(res)
        target= socket.gethostbyname(temp)  #needs input without http:// and with only domain
        #print(temp,target)
        target_ip=target
        domain=temp
    except Exception as e:
        print(e)
        print('Domain NOT found\n')

    if(target_ip==''): #Making sure the target_ip was not set
        try: #Get IP directly
            target= socket.gethostbyname(target)
            #CHECK IF HOST IS REACHABLE
            if(ping(target)==False):
                print('Host Not responding')
                return getTarget()
            target_ip= target
        except Exception as e:
            print(e)
            return getTarget()
             
    #Getting request 
    try: 
        req = requests.get(req, timeout=3)
    except:
        try:
            req = requests.get(domain, timeout=3)
        # except requests.exceptions.ConnectionError: #PROBLEM: NEVER RUNS
        #     print("ERROR: Cannot establish connection")
        #     return getTarget()
        except Exception as e:
            print(e)
            print('NO Response received\n')
            req=requests.Response() #NULL response

    #Info Received
    print("Target:  ", target_ip,'at',domain)
    return target_url, target_ip,domain,req

openPorts=''
#endregion

def Automated():
    global openPorts
    if(_portscan):
        try:
            openPorts = threadScanPorts(target_ip, maxthread=32200) #, portRange=range(11,500)
        except Exception as e:
            print("ERROR: Couldn't perform Port Scan\n",e)
    if(_webfingerprint):
        try:
            WebPrint(req, domain)
        except Exception as e:
            print("ERROR: Couldn't perform Web Fingerprinting\n",e)
    if(_webPathscan):
        try:
            WebPaths(target_url,req,_dirBruteForce)
        except Exception as e:
            print("ERROR: Couldn't perform Web Path Finding\n",e)
    if(_webinputTest):
        try:
            WebInputs(target_url,req)
        except Exception as e:
            print("ERROR: Couldn't perform Web Input Testing\n",e)
    

def Report(): #NOTE: Need to also pass params in Output() of each imported function to correctly name text files
    print(openPorts)
    if not os.path.exists(results_dirname):
        print('Results directory NOT found')
        #return
    else:
        print('Done')

#RUN HERE
results_dirname="Results"
print("WARNING: THE USE OF THIS SCRIPT ON SYSTEMS YOU DO NOT OWN IS ILLEGAL AND CAN GET YOU IN TROUBLE!")
if __name__ == "__main__":
    start_time=datetime.now()
    print("Started at",start_time)

    target_url, target_ip,domain,req = getTarget()
    print(target_url, target_ip,domain,req)

    if(_trafficMask):
        useTrafficMaze(Automated)
    else:
        Automated()
    print("Time taken:", datetime.now()-start_time)
    Report()