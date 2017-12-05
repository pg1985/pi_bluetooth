import bluetooth
import sys

hostMAC = sys.argv[1] # 0 is the name of the script 
port = 3
backlog = 1
size = 1024

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMAC, bluetooth.PORT_ANY))
s.listen(backlog)

#random uuid
uuid = "905a7ea6-64b0-466d-8081-c88cfaeb564e"

#Makes this service discoverable after pairing
bluetooth.advertise_service( s, "SampleServer", service_id = uuid, service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS], profiles = [bluetooth.SERIAL_PORT_PROFILE])
print("Waiting for connection on RFCOMM channel %d" % port)
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
except:	
    print("Closing socket")
    client.close()
    s.close()



