from module import log_table
from module import node
from module import socket_controller
from module import time_utility

# socket server setting
link_switch = True
link_state = 0

# Log Func
if __name__ == "__main__":
    print('socket_on')
    while link_switch == True:
        new_node = socket_controller.socket_listen()
        node.add_node(new_node)