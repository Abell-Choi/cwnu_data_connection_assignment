import random
import socket
import json

import socket_utility


node_prefix = "Node_"
node_list = []

def get_new_node_name():
    rnd = random.randrange(0,999999999)
    temp_node_name = lambda num : "{0}{1}".format(node_prefix, str(num))
    if len(node_list) == 0:
        return temp_node_name(rnd)
    
    for i in node_list:
        if i['name'] == temp_node_name(rnd):
            return get_new_node_name()

    return temp_node_name(rnd)

def add_node(socekt_connection:socket.socket):
    node_list.append({
        'name' : get_new_node_name(),
        'connection' : socekt_connection
    })
    return True

def find_node_by_name(node_name:str):
    for i in node_list:
        if i['name'] == node_name: return i
    return None

def del_node_by_name(node_name:str):
    for i in node_list:
        if i['name'] == node_name:
            node_list.remove(i)
            return True

    return False

def get_all_node_names():
    node_name_list = []
    for i in node_list:
        node_name_list.append(i['name'])

    return node_name_list


def send_message_from_node_name(node_name:str, message:str):
    if (res:=find_node_by_name(node_name)) == None:
        return False
    
    socket_utility.send_message(res['connection'], )
    
    
