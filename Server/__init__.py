from module import log
from module import socket_func as sck
from module import node as node
from module import time_utility

link_state = {
    'state' : -1
}

if __name__ == "__main__":
    # socket listen  실행
    if (socket_obj:= sck.socket_server_init())['res'] == 'err':
        log.log_function(log.log_table['error'](socket_obj['value']))
        quit()
    # 나 시작했어요!
    log.log_function(log.log_table['start'])
    link_state['state'] = 0
    
    # listen
    while link_state['state'] != -1:
        new_node = sck.socket_listen(socket_obj)
        node.add_node(new_node, link_state)
    log.log_saver()