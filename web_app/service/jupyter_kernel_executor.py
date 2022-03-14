import json
import datetime
import uuid
from websocket import create_connection

'''
credit to https://gist.github.com/manics
'''

base = 'ws://localhost:8888'
url = base + '/api/kernels/'
headers = {'Authorization': 'Token d623ec84f49f54007bec91f0f89b7cc01a43cbec25197f1c'}
kernel_id="494b8312-41c6-4023-8d29-beb14b846c7c"

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
                if msg_type in ('error', 'execute_reply'):
                    break
                if msg_type == 'stream':
                    print("stream content "+rsp['content']['text'])
                    code_output.append(rsp["content"]["text"])
                
                elif msg_type=="execute_result":
                    #print(rsp["content"]["data"]['text/plain'])
                    if 'text/html' in rsp["content"]["data"]:
                        code_output.append(rsp["content"]["data"]['text/html'])
                    else:
                        code_output.append(rsp["content"]["data"]['text/plain'])
                elif msg_type not in ('execute_input', 'status'):
                    pass
                
            except json.JSONDecodeError as e:
                print('Error decoding JSON: {}'.format(e))
                raise
        if msg_type == 'execute_reply':
            #print(rsp['content'])
            pass
        if msg_type == 'error':
            print("erros are raised ")
            error=""
            error='Failed to execute: {}'.format(rsp["content"]["evalue"])
            print("length of code is"+ str(len(code)))
            if len(code)>1:
                code_output.append("Step: "+str(i)+" "+ error )
            else:
                code_output.append(error )
            #raise Exception(error)

    #ws.close()
    return True,code_output
##y=execute_code(["df=pd.read_csv(\"work_file.csv\")","print df"])
#print(y)