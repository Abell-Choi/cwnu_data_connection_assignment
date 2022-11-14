import socket
import time
import json
# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '127.0.0.1'  
# 서버에서 지정해 놓은 포트 번호입니다. 
PORT = 3819
# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))


this_node_name = None

while True:
    data = client_socket.recv(1024)
    json_data = data.decode()
    print("()()" +json_data)
    data_dict = json.loads(json_data)
    if data_dict['type'] != 'ping':
        print(data_dict)
    
    if data_dict['type'] == 'set_node_name':
        this_node_name = data_dict['value']
    print(this_node_name)
    data = ''