import json
import datetime
import uuid
from pprint import pprint
from websocket import create_connection

base = 'ws://localhost:8888'
headers = {'Authorization': 'Token d623ec84f49f54007bec91f0f89b7cc01a43cbec25197f1c'}

url = base + '/api/kernels/'
kernel_id="494b8312-41c6-4023-8d29-beb14b846c7c"

def send_execute_request(code):
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
    
    for c in code:
        ws.send(json.dumps(send_execute_request(c)))

    code_output=[]
    # We ignore all the other messages, we just get the code execution output
    # (this needs to be improved for production to take into account errors, large cell output, images, etc.)
    for i in range(0, len(code)):
        msg_type = ''
        while msg_type != "stream":
            rsp = json.loads(ws.recv())
            msg_type = rsp["msg_type"]
        print(rsp["content"]["text"])
        code_output.append(rsp["content"]["text"])

    ws.close()
    return code_output

y=execute_code(["df=pd.read_csv(\"work_file.csv\")","print df"])
#print(y)