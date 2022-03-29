import json
import datetime
import uuid
from websocket import create_connection

'''
credit to https://gist.github.com/manics
'''

base = 'ws://localhost:8888'
url = base + '/api/kernels/'
headers = {'Authorization': 'Token 9dfe0c7f0e56fc00e39b1149f509544ed98624c60587b283'}
kernel_id="10d2f030-00ef-4d22-98c2-5f2e6de32740"

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
                #print("message type "+msg_type)
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
                    break;
                #elif msg_type not in ('execute_input', 'status'):
                #    pass
                
            except json.JSONDecodeError as e:
                print('Error decoding JSON: {}'.format(e))
                raise
        """ if msg_type == 'execute_reply':
            #print(rsp['content'])
            pass """
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

    #ws.close()
    return code_output
#y=execute_code(["print('Hello worl')"])
#print(y)