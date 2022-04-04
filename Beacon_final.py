from scapy.all import *
import os
import psutil
import signal
from time import * #Importing required modules

netSSID = 'testSSID'       #Network name here
iface = 'wlan0'         #Interface name here
conf.use_pcap = True
monitor = True


dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff',
addr2='22:22:22:22:22:22', addr3='33:33:33:33:33:33')

########################################################################################

######addr1 	Destination MAC address.
######addr2 	Source MAC address of sender.
######addr3 	MAC address of Access Point.

beacon = Dot11Beacon(cap='ESS+privacy')
essid = Dot11Elt(ID='SSID',info=netSSID, len=16)
rsn = Dot11Elt(ID='RSNinfo', info=(
'\x01\x00'                 #RSN Version 1
'\x00\x0f\xac\x02'         #Group Cipher Suite : 00-0f-ac TKIP
'\x02\x00'                 #2 Pairwise Cipher Suites (next two lines)
'\x00\x0f\xac\x04'         #AES Cipher
'\x00\x0f\xac\x02'         #TKIP Cipher
'\x01\x00'                 #1 Authentication Key Managment Suite (line below)
'\x00\x0f\xac\x02'         #Pre-Shared Key
'\x00\x00'))               #RSN Capabilities (no extra capabilities)

frame = RadioTap()/dot11/beacon/essid/rsn

#########################################################################################
#Code in the hashtag line is not my own https://gist.github.com/tintinweb/04c14d1497001e55e6c10ca28f198fbe
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

