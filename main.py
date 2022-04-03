import sys, socket, datetime, time, random,ra
import threading 
from threading import Thread

# global variables
list_of_threads = []
default_min_time_out = 10
default_max_time_out = 10

STATES = ["DO-NOT-WANT","HELD","WANTED"]

class RAThread(Thread):
    def __init__(self, id,state):
       Thread.__init__(self)
       self.state = state
       self.id = id
       self.active = []
       self.lock = threading.Lock()

    def run(self):
        while True:
            running()


def list():
    for thread in list_of_threads:
        print(f"P{thread.id},", thread.state)

def time_cs(args):
    print("time_cs")
    print(args)

def update_time(args):
    print(int(args))
    global default_max_time_out
    default_max_time_out = int(args)

def setup_nodes(number_of_nodes):
    #print(number_of_nodes)
    for i in range(int(number_of_nodes)):
        th = RAThread(i+1, STATES[0])
        th.start()
        list_of_threads.append(th)

def running():
    while(True):
        #pass
        time.sleep((default_min_time_out + default_max_time_out) / 2)
        #test_change_states()
        test.acquire()
        time.sleep(self.use_time)
        test.release()


        

def main(args):
    setup_nodes(args[1])

    # start the main loop
    running = True
    

    while running:
        inp = input().lower()
        cmd = inp.split(" ")

        command = cmd[0]

        if len(cmd) == 1:
            command = cmd[0]
        else:
            command = cmd[0]
            args = cmd[1]

        if len(cmd) > 3:
            print("Too many arguments")

        # handle exit
        elif command == "exit":
            running = False

        # handle list
        elif command == "list":
            try:
                list()
            except:
                print("Error")

        # handle clock
        elif command == "time-cs":
            try:
                time_cs(args)
            except:
                print("Error")

        elif command == "time-p":
            try:
                update_time(args)
                #print(args)
            except:
                print("Error")

        # handle unsupported command        
        else:
            print("Unsupported command:", inp)

    print("Program exited")


if __name__ == "__main__":
    main(sys.argv)

