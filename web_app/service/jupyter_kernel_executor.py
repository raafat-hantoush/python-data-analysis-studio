import json
from  datetime import datetime,timezone
import uuid
import os
from websocket import create_connection
import requests 
import re
'''
credit to https://gist.github.com/manics
'''

path = os.getcwd()
'''
reading from config file 
'''
import configparser
config = configparser.ConfigParser()
config.read(path+ '/config.txt')
#config.read('../config.txt')

'''
get Juypter server params
'''
def get_juypter_server_params():
    result= os.popen("jupyter notebook list").read()
    jupyter_url=""
    
    if "http" in result:
        jupyter_url=re.search("(?P<url>https?://[^\s]+)", result).group("url")
    else:
        pass
        """ os.popen("jupyter notebook")
        result= os.popen("jupyter notebook list").read()
        if "http" in result:
            jupyter_url=re.search("(?P<url>https?://[^\s]+)", result).group("url") """
        
    if len(jupyter_url) > 30 : 
        jupyter_port=jupyter_url[17:21]
        token= jupyter_url[int(jupyter_url.find("token")+6):]
        print("juypter server token is " + token)
        return jupyter_port,token
    else: 
        return "",""

jupyter_port,token= get_juypter_server_params()

#token=config['Jupyter']['Token']
#jupyter_port=config['Jupyter']['Localhost_Port']
##kernel_id=config['Jupyter']['Kernel_id'] ##static kernel id

kernel_id=""
base = 'ws://localhost:'+jupyter_port
http_base= 'http://localhost:' + jupyter_port
url = base + '/api/kernels/'
http_url= '{}/api/kernels'.format(http_base)
headers = {'Authorization': 'Token '+token}

'''
create juypter kernel
'''
def create_kernel():
    data = {}
    kernel_id= ""
    # sending post request and saving response as response object
    r = requests.post(url = http_url,
                    data = data,headers=headers)

    kernel = json.loads(r.text)
    if 'id' in kernel:
        kernel_id = kernel['id']
        print(
            '''Created kernel {0}.'''.format(kernel_id)
        )
    return kernel_id

'''
create Juypter message request 
'''
def send_execute_request(code):
    #print("kernel execute request "+ code)
    msg_type = 'execute_request';
    content = { 'code' : code, 'silent':False }
    hdr = { 'msg_id' : uuid.uuid1().hex, 
        'username': 'test', 
        'session': uuid.uuid1().hex, 
        'data': datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' }
    msg = { 'header': hdr, 'parent_header': hdr, 
        'metadata': {},
        'content': content }
    return msg

'''
execute source code on juypter kernel
'''
def execute_code(code): 
    global kernel_id
    if (kernel_id==""):
        kernel_id = create_kernel()
    # Execution request/reply is done on websockets channels
    ws = create_connection(url+kernel_id+"/channels",
     header=headers)
    code_output=[]
    for i, c in enumerate(code):
        print("kernel execute request "+ c)
        ws.send(json.dumps(send_execute_request(c)))
        execute_reply=False

        while True:
            try:
                rsp = json.loads(ws.recv())
                msg_type = rsp['msg_type']
                print("message type "+msg_type)
                #print(rsp['content'])

                if msg_type in ('error'):
                    break
                if msg_type == 'stream':
                    ##print("stream content "+rsp['content']['text'])
                    code_output.append(rsp["content"]["text"])
                    break;
                elif msg_type=="display_data":
                    #print(rsp["content"]["data"]["image/png"])
                    if 'image/png' in rsp["content"]["data"]:
                        img_src="data:image/png;base64," + rsp["content"]["data"]["image/png"]
                        img_html="<img width='100%' src="+img_src+" >"
                        code_output.append(img_html)
                        break;
                elif msg_type=="execute_result":
                    #print(rsp["content"]["data"]['text/html'])
                    if 'text/html' in rsp["content"]["data"]:
                        code_output.append(rsp["content"]["data"]['text/html'])
                    else:
                        code_output.append(rsp["content"]["data"]['text/plain'])
                    break
                
                elif msg_type=="status":
                    if ("execution_state" in rsp['content']):
                        execution_state=rsp['content']["execution_state"]
                        if (execute_reply):
                            print("no output for this specific command")
                            
                            if len(code)>1: ## meaning if it is run_all_above_command
                                step_index="Step "+str(i) +": "
                            else:
                                step_index=""
                                
                            code_output.append(step_index+"command runs successfully at "+ 
                                               datetime.now(timezone.utc).astimezone().strftime("%H:%M:%S")) ##%d.%m.%Y 
                            break
                              
                elif msg_type=="execute_reply":
                    if ('execution_count' and 'status' in rsp['content']):
                        execute_reply=True;
                        ## only break the loop when the execution finished and the stream returned in case there is stream
                        if execution_state=="idle":
                            pass
                
            except json.JSONDecodeError as e:
                print('Error decoding JSON: {}'.format(e))
                raise

        if msg_type == 'error':
            print("errors are raised ")
            error=""
            error='Failed to execute: {}'.format(rsp["content"]["evalue"])
            if len(code)>1:
                code_output.append("Step: "+str(i)+" "+ error )
            else:
                code_output.append(error )
    
    #ws.close()
    return code_output

#y=execute_code(["print('Hello worl')"])
#print(y)


