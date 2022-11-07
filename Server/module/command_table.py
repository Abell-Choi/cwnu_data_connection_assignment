import log_table
command = {
    'start' : lambda update_time : start(update_time),

}

def start(update_time):
    log_string = log_table.log_table['start'](update_time)
    log_table.log_function(log_string)
    return
