import random
import socket
from . import time_utility as t
from . import socket_func as s
from . import command as c
from . import log

node_prefix = 'NODE_'
active_node_table = {}
node_style = {
    'create_time' : '',
    'name' : '',
    'connection' : None,
    'recv_th' : None,
}

def get_new_node_name():
    temp_node_name = (lambda: "{0}{1}".format(node_prefix, str(random.randrange(0,999999999))))()
    print(temp_node_name)
    if len(active_node_table.keys()) == 0:
        return temp_node_name
    
    if temp_node_name in active_node_table.keys():
        return get_new_node_name()

    return temp_node_name()

def add_node(socekt_connection:socket.socket, link_state:dict):
    node = node_style.copy()
    node['name'] = get_new_node_name()
    node['create_time'] = t.get_system_runtime()
    node['connection'] = socekt_connection
    node['recv_th'] = s.get_socket_recv_th(socekt_connection, link_state)
    active_node_table[node['name']] = node.copy()
    print("*******************")
    print(active_node_table)
    # 노드 이름 알려줌
    c.send_node_name(node) 
    print(node)

    # 노드 생성됬다고 알려줌
    c.broadcast_node_list(get_all_active_nodes())
    return True

def del_node_by_name(node_name:str):
    if find_node_by_name(node_name) == None:
        return False
    
    del active_node_table[node_name]
    c.broadcast_node_list(get_all_active_nodes())
    log.log_function(log.log_table['node_deleted'](node_name))
    return True

def find_node_by_name(node_name:str):
    print("asdfasdfasfjladjsfkl")
    print(active_node_table.keys())
    print(node_name)
    if node_name in active_node_table.keys():
        return active_node_table[node_name]

    return None

def get_all_active_nodes():
    return active_node_table.keys()

def get_all_active_nodes_count():
    return len(get_all_active_nodes())