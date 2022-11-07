import json
import os

log_file_dic = os.path.dirname(os.path.abspath(__file__)) +'/logs/'
log_file_name = 'link.txt'

log_table = {
    'start' : lambda update_time : "{0} Link Start //{1} min {2} sec {3} msec\n{0} System Clock Start //{1}, {2}, {3}".format(update_time, update_time.split(':')[0],update_time.split(':')[1],update_time.split(':')[2]),
    'node_connected' : lambda update_time, node_name : "{0} New node connected -> {1}".format(update_time, node_name),
    'node_disconnected' : lambda update_time, node_name : "{0} {1} is disconnected".format(update_time, node_name),
    'add_new_node' : lambda update_time, node_list : "{0} Node List -> {1}".format(update_time, ",".join(node_list)),
    'send_req' : lambda update_time, send_node, receive_node : "{0} {1} Data Send Request TO {2}".format(update_time, send_node, receive_node),
    'accept' : lambda update_time, send_node, receive_node : "{0} Accept : {1} Data Send Request To {2}".format(update_time, send_node, receive_node),
    'reject' : lambda update_time, send_node, receive_node : "{0} Reject : {1} Data Send Request To {2}".format(update_time, send_node, receive_node),
    'send_finished' : lambda update_time, send_node, receive_node : "{0} {1} Data Send Finished To {2}".format(update_time, send_node, receive_node),
    'error' : lambda update_time, error_string, params : "{0} [ERROR] Some error {1} : {2}".format(update_time, params, error_string),
    'stop' : lambda update_time : "{0} System Clock Finished\n{0} Link Finished".format(update_time),
}
log_list = []


def log_function(log_string:str):
    print(log_string)
    log_list.append(log_string)
    return

def log_path_checker():
    if not os.path.exists(log_file_dic):
        try:
            os.mkdir(log_file_dic)
        except Exception as e:
            log_function(log_table['error']("FILE PATH ERROR", e))
            return False

    return True

def log_saver():
    if not log_path_checker():
        return False
    json_string = json.dumps( log_list, indent=4, ensure_ascii=False )
    try:
        f = open(log_file_dic + log_file_name, 'w')
        f.write(json_string)
        f.close()
    except Exception as e:
        log_function(log_table['error']("ERROR", e))
        return False

    return True