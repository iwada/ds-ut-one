import sys, time, threading, socket, json
import pickle as pickle

REPLY = 0
REQUEST = 1
WANTED = 0
HELD = 1
DO_NOT_WANT = 2
localInfo ={ 'procPID': None,  'procState': None, 'procTimestamp': None, 'procAddr': None, 'procRemotes': None }
defferedQueue = []  
replyQueue    = []  
msgThread = None
remoteAddresses = { } 
MAXRECV = 4096 

def CreateProcess(localAddr, procPID):

    localInfo['procPID']         = procPID
    localInfo['procState']       = DO_NOT_WANT
    localInfo['procAddr']        = localAddr
    

    #thread forks the messageListener function to run in the background 
    msgThread = threading.Thread(target = MessageListener)
    msgThread.start()
    return localInfo['procPID'] , localInfo['procState']

def ProcessRemoteAddress(remoteAddr):
        #Add the other two processes addresses to a dictionary for access later
    for remote_address in remoteAddr:
        remoteAddresses["remoteName_%d",remote_address] = remote_address

def SendMessage(addr, message):
    sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #print(message)
    sendingSocket.sendto((str(message).encode()), addr)
    sendingSocket.close()
    return True

def MessageListener():
    #print(localInfo['procAddr'])
    listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #listeningSocket.bind(localInfo['procAddr']) #Bind the socket to the local address

    while True:
        MessageHandler(listeningSocket.recv(MAXRECV))

def MessageHandler(message):
    remoteMessage = eval(message) 
    if remoteMessage['type'] == REQUEST: 
        if (remoteMessage['procInfo']['procTimestamp'] < localInfo['procTimestamp'] and localInfo['procState'] == WANTED) or localInfo['procState'] == HELD:
            defferedQueue.append(remoteMessage['procInfo']['procAddr'])
        else:
            message = { 'type': REPLY, 'procInfo': localInfo}
            SendMessage(remoteMessage['procInfo']['procAddr'], message)
    
    if remoteMessage['type'] == REPLY:
        replyQueue.remove(remoteMessage['procInfo']['procAddr'])

def MutexLock(the_mutex):
    localInfo['procState'] = WANTED             #Change state
    localInfo['procTimestamp'] = time.time()    #Generate the timestamp for  message
    requestMessage = { 'type': REQUEST, 'procInfo': localInfo, 'mutex': the_mutex }
    for address in list(remoteAddresses.values()):
        SendMessage(address, requestMessage)
        replyQueue.append(address) 
 
    while len(replyQueue) > 0: pass 
    return True
    
    
def MutexUnlock(the_mutex):
    localInfo['procState'] = DO_NOT_WANT
    replyMessage = { 'type': REPLY, 'procInfo': localInfo, 'mutex': the_mutex }
    for address in replyQueue:
        SendMessage(address, replyMessage)
        defferedQueue.remove(address)
    return True


def MutexExit():
    return True
