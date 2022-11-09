import node
import time_utility as t
import socket_func
import log


command_style = {
    'update_time' : '',
    'sender' : 'server',
    'type' : '',
    'value' : '',
    'description' : ''
}

def send_node_name(node:dict):              # 노드 이름 할당
    message = command_style.copy()
    message['update_time'] = t.get_system_runtime()
    message['type'] = "set_node_name"
    message['value'] = node['name']
    message['description'] = log.log_table['new_node_created'](node['name'])

    socket_func.socket_send(node['connection'], message)
    log.log_function(message['description'])

def broadcast_node_list(node_lists:list):   # 신규 노드 알림
    message = command_style.copy()
    message['update_time'] : t.get_system_runtime()
    message['type'] = 'node_update'
    message['value'] = node_lists

    for i in node_lists:
        message['description'] = log.log_table['new_node_broadcast'](node_lists['name'])
        log.log_function(message['description'])
        socket_func.socket_send(i['connection'], message)

def send_req(dict_message:dict, link_state:dict, ):
    # 로그 먼저 보내고
    message = command_style.copy()
    message['update_time'] = t.get_system_runtime()
    message['type'] = 'log'
    message['value'] = log.log_table['req'](dict_message['sender'], dict_message['value'])
    socket_func.socket_send(node.find_node_by_name(dict_message['sender'])['connection'], message)

    if link_state != 0 or (target_node:=node.find_node_by_name(dict_message['value'])) == None: #reject
        message['type'] = 'reject'
        message['value'] = None
        message['description'] = log.log_table['reject'](dict_message['sender'], dict_message['value'])
        socket_func.socket_send(node.find_node_by_name(dict_message['sender'])['connection'], message)
        if target_node == None:
            node.del_node_by_name(dict_message['value'])
        return

    # accept

