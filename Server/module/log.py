import time_utility
log_table = {
    'start' : "00:00:00 Link Start //{1} min {2} sec {3} msec\n00:00:00 System Clock Start //{1} min {2} sec {3} msec\n",
    'error' : lambda error_value:"{0} [ERROR] -> {1}".format(time_utility.get_system_runtime(), error_value)
}
log_list = []


import json
import os

log_file_dic = os.path.dirname(os.path.abspath(__file__)) +'/logs/'
log_file_name = 'link.txt'

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