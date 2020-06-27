from bs4 import BeautifulSoup
import requests
import re, json
from tld import get_tld
from urllib.parse import urljoin

payloadsf = 'WebInput_payloads.txt'

#region FUNCTIONS
url,req='',''
resultForms={}
def geturl():
    global url, req
    url = input("Please enter a URL: ")
    if(not url.startswith(('http://','https://'))):
        url = 'http://'+url
        
    print("Connecting to",url,"...")
    try:
        #print(socket.gethostbyaddr(url)) #returns url from ip address #PROBLEM: gets a weird server url instead of hostname that we want
        req = requests.get(url, timeout=3)
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

def getForms(req):
    soup = BeautifulSoup(req.content, "html.parser")
    forms=soup.find_all("form")
    details={}
    counter=0
    for form in forms:
        action = form.attrs.get("action",'').lower() #second arg is default value
        method = form.attrs.get("method", "get").lower()
        inputs=[]
        for tag in form.find_all("input"):
            input_id = tag.attrs.get("id",'')
            input_type = tag.attrs.get("type", "text")
            input_name = tag.attrs.get("name",'')
            input_value =tag.attrs.get("value", "")

            _input= {"id":input_id, "type": input_type, "name": input_name, "value": input_value}
            inputs.append(_input)
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        resultForms["form"+str(counter)]=details
        counter+=1

def testForms(url, proxy='',headers=''):
    payloadsList=[]
    with open(payloadsf,'r') as f:
        for line in f:#.readlines():
            if line.startswith(('#','\n')): #title
                continue
            line=line.replace('\n','')
            payloadsList.append(line)
    #f.close() # The file is always closed after the with-scope ends.
    
    for k,v in resultForms.items():
        forminp=v["inputs"]     #list
        for inp in forminp:     #dict
            if(inp['type']=='text' or inp['type']=='password' or inp['type']=='url' or inp['type']=='search'):
                data=inp
                #Test Input:
                for p in payloadsList:
                    data['value']=p
                    # print(data)
                    try:
                        urli= urljoin(url, v["action"]) #add form action to url requested
                        if(v['method']=='post'):
                            r=requests.post(urli,data=data, proxies=proxy,headers=headers)
                        else:
                            r=requests.get(urli,data=data, proxies=proxy,headers=headers)

                        if(p in r.content.decode()): #NOT FOR SQL INJECTION SINCE PAGE CHANGES WITHOUT PAYLOAD APPEARING ON PAGE
                            print(k,inp['id'],'is vulnerable to',p)
                    except Exception as e:
                        print("Cannot test form:",e)
                        continue
   
def Output():
    with open("Forms"+".txt", 'w') as f:
        f.write("FORMS:\n")    
        f.write(json.dumps(resultForms))
    #f.close() # The file is always closed after the with-scope ends.

def WebInputs(url,req, proxy='',headers=''): #used in Automated
    getForms(req)
    print(resultForms)
    testForms(url, proxy,headers)
    # Output()
#endregion

#RUN HERE
if __name__ == "__main__":
    geturl()
    getForms(req)
    print(resultForms)
    testForms(url)
    #Output()
