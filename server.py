import json
import socket
import threading
import os
import time
import datetime
import random

# socket server setting
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # WINERROR 10048 Solution
socket_obj.bind(("", 3819))

node_list = []
node_prefix = 'NODE_'

start_time = datetime.datetime.now()
get_system_run_time = lambda : str(datetime.datetime.now() - start_time)[:-3] # system run time 확인용
link_switch = True
link_state = 0

log_table = {
    'start' : lambda update_time : "{0} Link Start //{1} min {2} sec {3} msec\n{0} System Clock Start //{1}, {2}, {3}".format(update_time, update_time.split(':')[0],update_time.split(':')[1],update_time.split(':')[2]),
    'node_connected' : lambda update_time, node_name : "{0} New node connected -> {1}".format(update_time, node_name),
    'node_disconnected' : lambda update_time, node_name : "{0} {1} is disconnected".format(update_time, node_name),
    'add_new_node' : lambda update_time, node_list : "{0} Node List -> {1}".format(update_time, ",".join(node_list)),
    'send_req' : lambda update_time, send_node, receive_node : "{0} {1} Data Send Request TO {2}".format(update_time, send_node, receive_node),
    'accept' : lambda update_time, send_node, receive_node : "{0} Accept : {1} Data Send Request To {2}".format(update_time, send_node, receive_node),
    'reject' : lambda update_time, send_node, receive_node : "{0} Reject : {1} Data Send Request To {2}".format(update_time, send_node, receive_node),
    'send_finished' : lambda update_time, send_node, receive_node : "{0} {1} Data Send Finished To {2}".format(update_time, send_node, receive_node),
    'error' : lambda update_time, error_string : "{0} [ERROR] Some error -> {1}".format(update_time, error_string),
    'stop' : lambda update_time : "{0} System Clock Finished\n{0} Link Finished".format(update_time),
}

command_table = {
    'send_req' : lambda dict_command : send_req_func(dict_command)
}
log_list = []
send_data_list = []

# send json style
get_json_style = lambda updatetime, type, value, description : { 'update_time' : updatetime, 'type' : type, 'value' : value, 'description' : description }

# Log Func
def log_func(log_string:str):
    print(log_string)
    log_list.append(log_string)
    return

# Log Save
def save_log():             # 로그 저장기
    log_string = json.dumps(log_list, ensure_ascii=False, indent=4)
    f = open('./logs/server.txt', 'w')
    f.write(log_string)
    f.close()
    return True

def end_time_checker():     # 종료 시간 검사
    string_min = int(get_system_run_time().split(':')[0])
    if string_min >= 1:
        return True
    return False

def is_exist_node_name(node_name:str):
    if len(node_list) == 0:
        return False
    
    for i in node_list:
        if i['name'] == node_name:
            return True
        
    return False

# 실제 처리를 위한 함수 모음들
# {update_time, sender, type, value, description으로 나뉨}
def send_req_func(dict_command:dict):
    # making log
    log_string = log_table['send_req'](get_system_run_time(), dict_command['sender'], dict_command['value'])
    log_func(log_string)
    runtime = get_system_run_time()

    # link is busy
    if link_state != 0: # link is busy -> reject
        log_string = log_table['reject'](runtime, dict_command['sender'], dict_command['value'])
        res = get_json_style(runtime, 'reject', dict_command['value'], log_string)
        send_data_list.append({"target":dict_command['sender'], "value":res})
        log_func(log_string)
        return
    
    link_state = 1
    log_string = log_table['accept'](runtime, dict_command['sender'], dict_command['value'])
    res = get_json_style(runtime, 'accept', dict_command['value'], log_string)
    send_data_list.append({'target':dict_command['sender'], "value" : res})
    log_func(log_string)

    # 실제 5초 통신 구현할 수 있지만 송수신 데이터가 없어서 5초 딜레이 줌
    time.sleep(0.500)
    runtime = get_system_run_time()
    log_string = log_table['send_finished'](runtime, dict_command['sender'], dict_command['value'])
    res = get_json_style(runtime, 'send_finished', dict_command['value'], log_string)
    send_data_list.append({'target' : dict_command['sender'], 'value' : res})
    link_state = 0
    return

def stop_func (dict_command:dict):
    runtime = get_system_run_time()
    log_string = log_table['stop'](runtime)
    log_func(log_string)
    for i in node_list:
        res = get_json_style(runtime, 'stop', '', log_string)
        send_data_list.append({'target' : i['name'], 'value' : res})

    save_log()

    return
# 옴뇸뇸

def recv(socket_object, node_name:str): # Node 가 요청하는 데이터 수신
    while link_switch and ping(socket_object):
        try:
            recv_data = socket_object.recv(1024)
        except Exception as e:
            continue
        # WIP recv functional Add
        recv_string = recv_data.decode()

        try:
            recv_dict = json.loads(recv_string)
        except Exception as e:
            log_string = log_table['error'](get_system_run_time(), e)
            continue
        
        command_table[recv_dict['type']](recv_dict)

    print('{0} {1} recv thread closed'. format(get_system_run_time(), node_name))
    return False

def send(socket_object:socket.socket, node_name:str): # Node 전송 (데이터든... 뭐든..)
    while link_switch:
        if not ping(socket_object) :
            return delete_node_in_table(node_name)
        if len(send_data_list) == 0 :
            time.sleep(0.1)
            continue
        if send_data_list[0]['target'] != node_name:
            time.sleep(0.1)
        send_data = send_data_list[0]['value']
        socket_object.sendall(json.dumps(send_data, ensure_ascii=False, indent=4).encode())
        del send_data_list[0]
    
    print('{0} {1} send thread closed'.format(get_system_run_time(), node_name))
    return False

def ping(socket_object:socket.socket):
    json_string = json.dumps({
        "update_time" : get_system_run_time(),
        "type" : "ping",
        "value" : '',
        "description" : 'ping'
    }, ensure_ascii=False, indent=4)
    try:
        socket_object.sendall(json_string.encode())
    except Exception as e:
        return False
    return True

# checking exist node
def check_exist_node(node_name:str):
    if len(node_list) == 0:
        return False
    
    for i in node_list:
        if i['name'] == node_name:
            return True
        
    return False



# socket listen func -> 노드 연결 대기
def socket_listen():
    socket_obj.listen()
    node, addr = socket_obj.accept()
    return node

# Making new node -> 노드가 새로 연결이 되었을 때 처리
def addNode(socket_connection_obj):
    # node key -> name, send, receive
    node_name = node_prefix +str(random.randrange(0,10000))
    while check_exist_node(node_name):
        node_name = node_prefix +str(random.randrange(0,10000))

    recv_th = threading.Thread(target=recv, args=(socket_connection_obj, node_name))
    send_th = threading.Thread(target=send, args=(socket_connection_obj, node_name))
    recv_th.start()
    send_th.start()
    node_dict = {
        'name' : node_name,
        'create_time' : get_system_run_time(),
        'send_th' : send_th,
        'recv_th' : recv_th,
    }

    node_list.append(node_dict)

    # log func
    log_string = log_table['node_connected'](get_system_run_time(), node_name)
    log_func(log_string)
    res = get_json_style(get_system_run_time(), 'node_connected', node_name, log_string)
    send_data_list.append({'target' : node_name, 'value' : res})
    return True


def delete_node_in_table(node_name:str):
    for i in node_list:
        if i['name'] == node_name:
            node_list.remove(i)
            break
    log_string = log_table['node_disconnected'](get_system_run_time(), node_name)
    print(log_string)
    log_list.append(log_string)

def init():
    log_string = log_table['start']("00:00:00") # 실제 실행 후 작동시키면 시스템 클릭에 딜레이가 발생
    log_func(log_string)
    return True

if __name__ == "__main__":
    print('socket_on')
    while link_switch == True:
        new_node = socket_listen()
        addNode(new_node)
