import socket 
import json
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # WINERROR 10048 Solution
socket_obj.bind(("", 3819))

# socket server setting
link_switch = True
link_state = 0

def socket_listen():
    socket_obj.listen()
    node, addr = socket_obj.accept()
    return node

def recv_message(socket_connection:socket.socket, node_name:str):
    res_string = socket_connection.recv(1024).decode()
    try:
        res_dict = json.loads(res_string)
    except Exception as e:
        return {'type' : 'ERROR', 'value' : 'e'}

def send_message(socket_connection:socket.socket, message:dict):
    return socket_connection.sendall(json.dumps(dict, ensure_ascii=False, indent=4))