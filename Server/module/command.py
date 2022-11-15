from . import node
from . import time_utility as t
from . import socket_func
from . import log
from . import time_utility

import json
import time

'''
command_message_style
{ update_time, sender, type, value, description }
'''
get_message_style = lambda update_time, sender='server', type_string='', value='', description='': {'update_time' : update_time, 'sender' : sender, 'type' : type_string, 'value' : value, 'description' : description}.copy()

def send_node_name(node:dict):              # 노드 이름 할당
    message = get_message_style(t.get_system_runtime(), 'server', 'set_node_name', node['name'], (log.log_table['new_node_created'])(node['name']))
    print(message)
    socket_func.socket_send(node['connection'], message)
    log.log_function(message['description'])

    # 메모리  관리 필수
    del message

def broadcast_node_list(node_lists:list):   # 신규 노드 알림
    message = get_message_style(
        t.get_system_runtime(),
        'server',
        'node_update',
        list(node_lists),
        None
    )
    for i in node_lists:
        message['description'] = log.log_table['new_node_broadcast'](i)
        log.log_function(message['description'])
        node_conn = node.find_node_by_name(i)
        if node_conn != None : node_conn = node_conn['connection']
        socket_func.socket_send(node_conn, message)

    del message

def send_req( dict_message:dict, link_state:dict ):
    '''
    전송 요청에 대한 처리를 담당하는 클래스입니다.\n
    요청을 받을 경우 link_state, target_node_state에 따라 send_condition이 결정되며\n
    send_condition에 따라 결과가 달라집니다\n
    ***\n
    not send_condition == reject\n
    send_condition == accept
    ***\n
    '''

    sender_node = node.find_node_by_name(dict_message['sender'])
    # send log -> sender
    message = get_message_style(
        t.get_system_runtime(),
        'system',
        'log',
        log.log_table['req'](dict_message['sender'], dict_message['value'])
    )
    socket_func.socket_send(sender_node['connection'], message)

    if link_state != 0 or (receiver_connection:=node.find_node_by_name(dict_message['value'])) == None: #reject 
        # reason -> link is busy or receiver_connection_name_is_null
        message['type'] = 'reject'
        message['value'] = None
        message['description'] = log.log_table['reject'](dict_message['sender'], dict_message['value'])
        socket_func.socket_send(sender_node['connection'], message)
        if receiver_connection == None:
            node.del_node_by_name(dict_message['value'])
        
        del message  # 메모리 누수 방지
        return
    
    # real_send_proc
    link_state['state'] = 1
    # send receive mode   value : sender, type : receive_mode
    message['type'] = 'receive_mode'
    message['value'] = dict_message['sender']

    socket_func.socket_send(receiver_connection['connection'], message)
    
    # send sending mode

    message['type'] = 'accept'
    message['value'] = dict_message['value']
    message['description'] = log.log_table['accept'](dict_message['sender'], dict_message['value'])
    socket_func.socket_send(receiver_connection['connection'], message)

    # end of connection
    time.sleep(0.005) # -> 5msc..?
    message['type'] = 'finished_send'
    message['value'] = [dict_message['sender'], dict_message['value']]
    message['description'] = log.log_table['finished_send'](dict_message['sender'], dict_message['value'])
    socket_func.socket_send(receiver_connection['connection'], message)
    socket_func.socket_send(sender_node['connection'], message)
    return