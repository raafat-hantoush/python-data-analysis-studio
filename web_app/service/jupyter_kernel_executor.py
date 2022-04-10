import json
import datetime
import uuid
import os
from websocket import create_connection

'''
credit to https://gist.github.com/manics
'''

path = os.getcwd()
'''
reading from config file 
'''
import configparser
config = configparser.ConfigParser()
config.read(path +'/config.txt')
token=config['Jupyter']['Token']
jupyter_port=config['Jupyter']['Localhost_Port']
kernel_id=config['Jupyter']['Kernel_id']

base = 'ws://localhost:'+jupyter_port
url = base + '/api/kernels/'
headers = {'Authorization': 'Token '+token}

def send_execute_request(code):
    #print("kernel execute request "+ code)
    msg_type = 'execute_request';
    content = { 'code' : code, 'silent':False }
    hdr = { 'msg_id' : uuid.uuid1().hex, 
        'username': 'test', 
        'session': uuid.uuid1().hex, 
        'data': datetime.datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' }
    msg = { 'header': hdr, 'parent_header': hdr, 
        'metadata': {},
        'content': content }
    return msg

def execute_code(code): 
    # Execution request/reply is done on websockets channels
    ws = create_connection(url+kernel_id+"/channels",
     header=headers)
    code_output=[]
    for i, c in enumerate(code):
        print("kernel execute request "+ c)
        ws.send(json.dumps(send_execute_request(c)))
        while True:
            try:
                rsp = json.loads(ws.recv())
                msg_type = rsp['msg_type']
                print("message type "+msg_type)
                print(rsp['content'])

                if msg_type in ('error'):
                    break
                if msg_type == 'stream':
                    print("stream content "+rsp['content']['text'])
                    code_output.append(rsp["content"]["text"])
                    break;
                
                elif msg_type=="execute_result":
                    #print(rsp["content"]["data"]['text/plain'])
                    if 'text/html' in rsp["content"]["data"]:
                        code_output.append(rsp["content"]["data"]['text/html'])
                    else:
                        code_output.append(rsp["content"]["data"]['text/plain'])
                    break
                
                elif msg_type=="status":
                    if ("execution_state" in rsp['content']):
                        execution_state=rsp['content']["execution_state"]
                        #print(execution_state)
                              
                elif msg_type=="execute_reply":
                    if ('execution_count' and 'status' in rsp['content']):
                        ## only break the loop when the execution finished and the stream returned in case there is stream
                        if execution_state=="idle":
                            print("no output for this specific command")
                            break
                
            except json.JSONDecodeError as e:
                print('Error decoding JSON: {}'.format(e))
                raise

        if msg_type == 'error':
            print("errors are raised ")
            error=""
            error='Failed to execute: {}'.format(rsp["content"]["evalue"])
            print("length of code is "+ str(len(code)))
            if len(code)>1:
                code_output.append("Step: "+str(i)+" "+ error )
            else:
                code_output.append(error )
            #raise Exception(error)
    print (code_output)
    #ws.close()
    return code_output
#y=execute_code(["print('Hello worl')"])
#print(y)