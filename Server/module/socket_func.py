import socket 
import json
import threading

import log
import command

def socket_server_init():
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # WINERROR 10048 Solution
        socket_obj.bind(("", 3819))
        return {'res' : 'ok', 'value' : socket_obj}
    except Exception as e:
        print(e)
        return {'res' : 'err', 'value' : e}


def socket_listen(socket_obj:socket.socket):
    socket_obj.listen()
    node, addr = socket_obj.accept()
    return node

def socket_send(connection:socket.socket, message:dict):
    connection.sendall(json.dumps(message, indent=4, ensure_ascii=False))

def json_to_dict(sender:str, string_message:str):
    try:
        dict_json = json.loads(string_message)
    except Exception as e:
        return {'type' : 'err', 'value' : e}
    
    return dict_json

def socket_recv(connection:socket.socket, link_state:dict):
    while link_state != -1:
        recv_res = connection.recv(1024)
        dict_res = json_to_dict(recv_res)
        
        # 나중에 따로 처리해줘야함
        if dict_res['type'] == 'err' : 
            continue

        if dict_res['type'] == 'req':
            command.send_req(dict_res, link_state, connection)

def get_socket_recv_th(connection:socket.socket, link_state:dict):
    t = threading.Thread(target=socket_recv, args=(connection, link_state))
    t.start()
    return t