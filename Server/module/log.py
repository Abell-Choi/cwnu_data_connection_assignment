from . import time_utility

log_table = {
    'start' : "00:00:00 Link Start //00 min 00 sec 00 msec\n00:00:00 System Clock Start //00 min 00 sec 00 msec\n",
    'error' : lambda error_value:"{0} [ERROR] -> {1}".format(time_utility.get_system_runtime(), error_value),
    'new_node_created' : lambda target_node_name : "{0} new node created -> {1}".format(time_utility.get_system_runtime(), target_node_name),
    'new_node_broadcast' : lambda target_node_name : "{0} broadcast node list to {1}".format(time_utility.get_system_runtime(), target_node_name),
    'node_deleted' : lambda target_node_name : "{0} {1} node is deleted!".format(time_utility.get_system_runtime(), target_node_name),
    'req' : lambda sender_node_name, target_node_name : "{0} {1} Data Send Request To {2}".format(time_utility.get_system_runtime(), sender_node_name, target_node_name),
    'accept' : lambda sender_node_name, target_node_name : "{0} Accept : {1} Data Send Request To {2}".format(time_utility.get_system_runtime(), sender_node_name, target_node_name),
    'reject' : lambda sender_node_name, target_node_name : "{0} Reject : {1} Data Send Request To {2}".format(time_utility.get_system_runtime(), sender_node_name, target_node_name),
    'finished_send' : lambda sender_node_name, target_node_name : "{0} {1} Data Send Finished To {2}".format(time_utility.get_system_runtime(), sender_node_name, target_node_name),
    
}
log_list = []


import json
import os

log_file_dic = os.path.dirname(os.path.abspath(__file__)) +'/logs/'
log_file_name = 'link.txt'

def log_function(log_string:str):
    '''
    로그 string을 출력하고 로그를 캐시(메모리)에 저장합니다,\n
    해당 로그의 인자 값은 log_table 에 의해서 처리를 하도록 권장드립니다.
    '''
    print(log_string)
    log_list.append(log_string)
    return

def log_path_checker():
    '''
    캐시(메모리) 에 저장된 로그값들을 저장하기 위해\n
    디스크의 주소에 파일이 저장 가능한지 여부를 확인합니다.\n
    변경사항이 없다면 실행 스크립트 폴더/logs/log_file_name 으로 저장됩니다.
    '''
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