import datetime
import random
from datetime import datetime
from datetime import timedelta
import math

end_time_min = 1

system_start_time = datetime.datetime.now()
get_system_runtime = lambda : str(datetime.datetime.now() - system_start_time)[:-3] # system run time 확인용
check_end_time = lambda : True if int(get_system_runtime().split(':') [:-3])>=end_time_min else False

# 과제 제공물의 BackofTimer를 python으로 변환
def back_of_timer_func(trans_number:int):
    trans_number = trans_number if trans_number<=10 else 10
    time = random.randrange(0,  * math.pow(2, trans_number)-1)
    return time

def update_back_off_time(msec_data:int):    # update back_off_timer
    back_off_timer = datetime.now() + timedelta(milliseconds=msec_data)

def check_back_off_time():
    if back_off_end_time == None: back_off_end_time = update_back_off_time(random.randrange(1,100))
    return False if back_off_end_time > datetime.now() else True
