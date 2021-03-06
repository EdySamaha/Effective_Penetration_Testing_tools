import socket, threading, sys
import re, string
from datetime import datetime
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from tld import get_tld #needs url with http://

#Default:
portRange=range(0, 65535+1) #(inclusive, exclusive)
timeout=1 #sec
target=""
maxthread=6500

#region FUNCTIONS
openPorts=[]
#NOTE: DO BLEOW IN TRY LOOP COZ 1 SOCKET CAN ONLY CONNECT TO 1 PORT AT A TIME 
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #INET means use IPv4, STREAM means tcp, 
# sock.settimeout(2) #2sec timeout

def ScanPort(target, port, threading=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #INET means use IPv4, STREAM means tcp, 
        sock.settimeout(timeout) #sec timeout
        response= sock.connect_ex((target,port)) #argument is a union
        #print(response)
        if(response==0):
            print("Port",port,"is Open")
            openPorts.append(port)
        sock.close()       #close connection
    except KeyboardInterrupt:
        print("Stopped script with Ctrl+C")
        sock.close()
        if(threading):
            sys.exit(1) #exits script (not just return)
        return 0
    except socket.error:
        print ("Couldn't connect to server")
        sock.close()
        if(threading):
            sys.exit(1)
        return 0
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sock.close()
        if(threading):
            sys.exit(1)
        return 0
    except Exception as e:
        print(e)
        sock.close()
        #continue


def seqScanPorts(target): #sequential scan OUTDATED
    print("Scanning for open ports...")
    for port in portRange:
        if(ScanPort(target,port)==0): #if returned by any major exception
            break

def threadScanPorts(target, maxthread=maxthread, portRange=portRange):
    threads = []        # To run ScanPort concurrently
    threadcount, joinedthread =0,0
    # Spawning threads to scan ports
    for i in portRange:
        t = threading.Thread(target=ScanPort, args=(target, i, True))
        threads.append(t)

    # Starting threads
    for i in portRange:
        threads[i-portRange[0]].start() #-range[0] in case starting from port>0
        threadcount+=1
        if(threadcount>=maxthread):
            # Locking the main thread until all threads complete
            for j in range(i-maxthread+1, i+1):
                threads[j-portRange[0]].join() #waits until selected thread is complete
                joinedthread+=1
            threadcount=0

    #Joining last threads in case threadcount<maxthread at the end
    while((len(threads)-1) >=joinedthread):
        threads[joinedthread].join()
        joinedthread+=1
    
    openPorts.sort()
    return openPorts

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
    global target
    target_url= input('Enter target IP or Hostname: ')
    target=target_url
    if(target.startswith(('http://','https://'))):
        target=target.replace('https://','')
        target=target.replace('http://','')

    try:
        target_ip= socket.gethostbyname(target)
        #CHECK IF HOST IS REACHABLE
        if(ping(target_ip)==False):
            print('Host Not responding')
            getTarget()
            return
        print("Target:  ", target,'at',target_ip)
        target= target_ip
    except:
        try: #get IP from domain
            res = get_tld(target_url, as_object=True)
            domain = res.domain
            temp= domain +'.'+str(res)
            target_ip= socket.gethostbyname(temp)  #needs input without http:// and with only domain
            print(temp,target_ip)
            target=target_ip
            return
        except Exception:# as e:
            pass #print(e)
        print("invalid IP address")
        getTarget()

def getportRange():
    global portRange
    try:
        minp=int(input('Enter First port Number: '))
        maxp=int(input('Enter Last port Number: '))
        if maxp<minp:
            print("Last port must be BIGGER than First port")
            getportRange()
            return
        portRange=range(minp, maxp+1)
    except:
        print("Please enter Integers")
        getportRange()

def ShowResults():
    print("All open ports found:")
    for i in openPorts:
        print("Port",i,"OPEN")
#endregion

#RUN HERE
if __name__ == "__main__":
    getTarget()

    q= input("Scan ALL[1] ports or Range[0]? ")
    q= ''.join(e for e in q if(e not in string.whitespace and e not in string.punctuation))
    if (q=="0"):
        getportRange()

    #Get max thread number
    print("Enter the maximum number of threads to run. NOTE: The higher the number the more load on your device")
    q=input("(default is "+str(maxthread)+") Num: ")
    if (q!=''):     #default chosen
        maxthread=q
    while(type(maxthread)!=int):
        try:
            maxthread=int(maxthread)
        except:
            print("Please enter an integer")
            maxthread=input("Enter the maximum number of threads to run: ")
    #print(maxthread)

    start_time=datetime.now()
    print("Started at",start_time)
    openPorts = threadScanPorts(target,maxthread,portRange)

    print("All Open ports found:\n",openPorts) #ShowResults()

    print("Time taken:", datetime.now()-start_time)
    