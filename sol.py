import bluetooth
import sys
import select
import lights.lights as lights

from uuid import getnode as get_mac

#Monkey Patching replaces regular python functions with Gevent equivalents that allow for easier concurrency
from gevent import monkey; monkey.patch_all()

connections = []

#Looking for the 
hostMAC = sys.argv[1] # 0 is the name of the script 

if hostMAC == None:
	hostMAC = get_mac()

backlog = 1
size = 1024

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMAC, bluetooth.PORT_ANY))
s.listen(backlog)

port = s.getsockname()[1]
print(s.getsockname())

#random uuid
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

run = True

#Makes this service discoverable after pairing, notwithstanding the RPi's configuration
bluetooth.advertise_service( s, "SampleServer",uuid)
print("Waiting for connection on RFCOMM channel %d" % port)
try:
    client, clientInfo = s.accept()
    while run:
        data = client.recv(size)
        if data:
            lights.test_light(data.decode("utf-8"))
            client.send(data) 
except Exception as err:	
    print("Closing socket: ", err)
    client.close()
    s.close()