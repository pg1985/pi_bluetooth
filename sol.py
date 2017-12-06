import bluetooth
import sys
import select
import lights.lights as lights
from thread import *

from uuid import getnode as get_mac

#Monkey Patching replaces regular python functions with Gevent equivalents that allow for easier concurrency
from gevent import monkey; monkey.patch_all()

connections = []

#Looking for the 
hostMAC = sys.argv[1] # 0 is the name of the script 

if hostMAC == None:
    hostMAC = get_mac()

backlog = 1

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMAC, bluetooth.PORT_ANY))
s.listen(backlog)

port = s.getsockname()[1]
print(s.getsockname())

#random uuid
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
print("Waiting for connection on RFCOMM channel %d" % port)
run = True

#Makes this service discoverable after pairing, notwithstanding the RPi's configuration
bluetooth.advertise_service( s, "SampleServer",uuid)

def connect(conn):
    while True:
        connClient = conn[0]
        data = connClient.recv(1024)
        if not data:
            break
        else:
            lights.test_light(data.decode("utf-8"))
            connClient.send(data) 

while 1:
    client, clientInfo = s.accept()
    print('New connection with: ' + addr[0] + ':' + str(addr[1]))

    #New thread: First argument is the function name, 2nd is tuple of the arguments
    start_new_thread(connect ,(conn,))