from multiprocessing.dummy import active_children
import sys, socket, datetime, time, random
import ricart_agrawala as ra
from tempfile import tempdir
import threading 
from threading import Thread

# global variables
list_of_processes = []
min_critical_section_timeout = 10
max_critical_section_timeout = 10
min_process_timeout = 5
max_process_timeout = 5
STATES = {0: "WANTED",  1: "HELD",  2: "DO_NOT_WANT"}

class RAThread(Thread):
   
    def __init__(self):
       Thread.__init__(self)

    def run(self):
        while True:
            running()

def list_processes():
    for dic in list_of_processes:
        print(f"P{dic['id']}, {STATES[dic['state']]}")
        
def run(self):
        while True:
            running()
        
def update_max_critical_section_timeout(args):
    #print(int(args))
    global max_critical_section_timeout
    max_critical_section_timeout = int(args)

def update_max_process_timeout(args):
    #print(int(args))
    global max_process_timeout
    max_process_timeout = int(args)

def setup_nodes(number_of_nodes):
    number_of_nodes = int(number_of_nodes)
    ports = random.sample(range(26000, 36000), number_of_nodes*3)
    lh = '127.0.0.1'
    l = {}
    #print(number_of_nodes)
    for i in range(int(number_of_nodes)):
        id,state = ra.CreateProcess((lh, ports[i]), i)
        l = {'id': id, 'state': state }
        list_of_processes.append(l)

def running():
    while(True):
        #print(max_process_timeout)
        #print(max_critical_section_timeout)
        ra.MutexLock(process_id, 'Mutex')
        time_out = random.randint(min_process_timeout,max_process_timeout)
        time.sleep(3)
        # pick a random thread to request 
    
def main(args):
    th = RAThread()
    th.start()
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
                list_processes()
            except:
                print("Error")

        # handle clock
        elif command == "time-cs":
            try:
                update_max_critical_section_timeout(args)
            except:
                print("Error")

        elif command == "time-p":
            try:
                update_max_process_timeout(args)
                #print(args)
            except:
                print("Error")

        # handle unsupported command        
        else:
            print("Unsupported command:", inp)

    print("Program exited")


if __name__ == "__main__":
    main(sys.argv)

