import socket
import json
import threading
from datetime import datetime, timedelta
import math
import random



# 로그만을 위한 뭐시기
log_list = []
log_table = {
    'error' : lambda update_time, err_string : "{0} Error -> {1}".format(update_time, err_string),
    'start' : lambda update_time, node_name : "{0} {1} Start // {2} min, {3} sec {4} msec".format(update_time, node_name, update_time.split(':')[0], update_time.split(':')[1], update_time.split(':')[2]),
    'update_node' : lambda update_time, node_list : "{0} Server has been updated node lists -> [{1}]".format(update_time, ', '.join(node_list)),
    'receive_data' : lambda update_time, send_node_name : "{0} Data Receive Start from {1}".format(update_time, send_node_name),
    'r_finished' : lambda update_time, send_node_name  : "{0} Data Receive Finished from {1}".format(update_time, send_node_name),
    'request' : lambda update_time, target_node_name : "{0} Data Send Request To {1}".format(update_time, target_node_name),
    'accept' : lambda update_time : "{0} Data send request Accept from Link".format(update_time),
    'reject' : lambda update_time, back_off_time: "{0} Data Send Request Reject from Link\n{0} Exponential Back-off Time: {1} msec".format(update_time, back_off_time),
    's_finished' : lambda update_time, target_node_name: "{0} Data Send Finished To {1}".format(update_time, target_node_name),
}

func_table = {
    'init' : lambda res_dict : init_func(res_dict),
    'update_node' : lambda res_dict : init_func(res_dict),
    'receive_data' : lambda res_dict : receive_data_func(res_dict),
    'r_finished' : lambda res_dict : r_finished(res_dict),
}

# socket setting
conn_auth = {
    "node_name" : None,
    "HOST" : '127.0.0.1',
    "PORT" : 3819,
}

socket_connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Client Socket
isDisconnected = False
isTransmission = False
back_off_end_time = None
back_off_trans_count = 1
send_target = None
node_list = []

# ================================ umm... idk ==================================== #

def init():
    try:
        socket_connector.connect((conn_auth['HOST'], conn_auth['PORT']))
    except Exception as e:
        print(e)
        log_func(log_table['error']("Client", "Connection Error -> {0}".format(str(e))))
        return False

    recv_fun_list = [recv_func(), recv_func()]
    for i in recv_fun_list:
        if i == False:
            log_func(log_table['error']("Client", "Init Error"))
            return False
    return True


def log_func(log_string:str):
    log_list.append(log_string)
    print(log_string)
    return
    
# 과제 제공물의 BackofTimer를 python으로 변환
def back_of_timer_func(trans_number:int):
    trans_number = trans_number if trans_number<=10 else 10
    time = random.randrange(0,  * math.pow(2, trans_number)-1)
    return time

def update_back_off_time(msec_data:int):    # update back_off_timer
    back_off_timer = datetime.now() + timedelta(milliseconds=msec_data)

def check_back_off_time():
    if back_off_end_time == None: back_off_end_time = update_back_off_time(random.randrange(1,100))
    return False if back_off_end_time > datetime.now() else True

def EOF():
    return False

# ================================ Receive Function Group ================================ #
def init_func(res_dict:dict):
    conn_auth['node_name'] = res_dict['value']
    log_func(log_table['start'](res_dict['update_time'], res_dict['value']))
    return True

def update_func(res_dict:dict):
    node_list.clear()
    for i in res_dict['value']:
        if i == conn_auth['node_name'] : continue
        node_list.append(i)
    log_func(log_table['update_node'](res_dict['update_date'], res_dict['value']))
    return

def receive_data_func(res_dict:dict):
    isTransmission = True
    log_func(log_table['receive_data'](res_dict['update_time'], res_dict['value']))
    return True
    
def r_finished(res_dict:dict):
    isTransmission = False
    log_func(log_table['r_finished'](res_dict['update_time'], res_dict['value']))
    return True


def accept_request(res_dict:dict):
    isTransmission = True
    log_func(log_table['accept'](res_dict['update_time'], res_dict['value']))
    back_off_end_time = None
    back_off_trans_count = 1
    send_target = None
    return True

def reject_request(res_dict:dict):
    back_off_trans_count += 1
    update_back_off_time(back_of_timer_func)
    return True

def s_finished(res_dict:dict):
    log_func(log_table['s_finished'](res_dict['update_time'], res_dict['value']))
    return True
    

def recv_func():
    try:
        recv = socket_connector.recv(1024).decode()
    except Exception as e:
        log_func(log_table['error']("Client Error", "recv error -> {0}".format(e)))
        return False
    
    try:
        print(recv)
        res_dict = json.loads(recv)
    except Exception as e:
        log_func(log_table['error']('Client' , 'json loads error -> {0}'.format(e)))
        return False
    
    return func_table[res_dict['res']](res_dict)

def recv_th_func():
    while not isDisconnected:
        recv_func()

    return False

def end_func():
    return False

# ================================ Send Function Group ================================ #
def send_func():
    if len(node_list) == 0 : return False
    if send_target == None : send_target = node_list[random.randrange(0, len(node_list))]
    if not check_back_off_time() : return False 
    if isTransmission : return False

    json_send_data = json.dumps({
        'req' : 'send',
        'target' : send_target
    }, ensure_ascii=False, indent=4)
    
    try:
        socket_connector.sendall(json_send_data.encode())
    except Exception as e:
        log_func(log_table['error']('Client', 'Send Func Error -> {0}'.format(e)))
        
    return True

    
def send_th_func():
    while not isDisconnected:
        send_func()
    return False



if __name__ == '__main__':
    if not init():
        print(log_list)
        quit()
    
    # 다중 스레드 (전송용 수신용)
    send_th = threading.Thread(target=send_th_func)
    recv_th = threading.Thread(target=recv_th_func)

    send_th.start()
    recv_th.start()

    send_th.join()
    recv_th.join()

