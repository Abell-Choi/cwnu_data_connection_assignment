import datetime

end_time_min = 1

system_start_time = datetime.datetime.now()
get_system_runtime = lambda : str(datetime.datetime.now() - system_start_time)[:-3] # system run time 확인용
check_end_time = lambda : True if int(get_system_runtime().split(':') [:-3])>=end_time_min else False