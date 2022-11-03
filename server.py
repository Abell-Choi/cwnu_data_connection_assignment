import socket
import os
import threading
import datetime
import time

log_table = {
    'start' : lambda : "{0} Link Start //{1}\n{0} Sytem Clock Start //{1}".format("00:00:000", "00 min 00 sec 000 msc"),
    'data_send_request' : lambda update_time, sender, receiver : "{0} {1} Data Send Request To {2}".format(update_time, sender, receiver),
    'accept_link' : lambda update_time, sender, receiver : "{0} Accept: {1} Data Send Request To {2}".format(update_time, sender, receiver),
    'rejcet_link' : lambda update_time, sender, receiver : "{0} Reject: {1} Data Send Request To {2}".format(update_time, sender, receiver),
    'finish' : lambda update_time, sender, receiver : "{0} {1} Data Send Finished To {2}".format(update_time, sender, receiver),
    'eof' : lambda update_time : "{0} System Clock Finished\nLink Finished".format(update_time)
}

# socket server setting
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # WINERROR 10048 Solution
socket_obj.bind(("", 3819))

# server runtime setting
start_time = datetime.datetime.now()
get_system_run_time = lambda : str(datetime.datetime.now() - start_time)[:-3]

# socket proc
def socket_listen():
    socket_obj.listen()
    node, addr = socket_obj.accept()

if __name__ == "__main__":
    quit()