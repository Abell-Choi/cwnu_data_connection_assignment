import time
import threading

class th(threading.Thread):
    isRunning = False
    test:list = []
    def __init__(self):
        super().__init__()
    
    def run(self):
        while True:
            print("aaa ")
            time.sleep(1)

    def test(self, msg):
        if self.isRunning:
            self.test.append(msg)
            print("Isrunning -> {0}".format(len(self.test)))
            return
        
        self.isRunning = True
        while self.test != []:
            time.sleep(1)
            print(self.test[0])
            del self.test[0]


t = th()
t.start()
for i in range(0,10):
    t.test(i)