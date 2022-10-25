# WIFIGHT
## The wifi hacking tool kit
written in python3, WIFIGHT will let you crack a WPA wifi network.

# Usage
## Installation:
### Github:
```bash
git clone https://github.com/idobarel/wifight.git #clone the repo
cd wifight # navigate into the directory
./installer.sh # give execute permissions
./wifight -h # run the app!
```
## Command syntax:
there is a lot in this tool:
the command are (might changed): <br>
### deauth:
#### kick a target from a network.
##### args:
iface       Specify the wireless interface you wish to use<br>
##### flags:
-h, --help                  show the help message and exit<br>
-t TARGET, --target TARGET<br>
                            Specify the target device MAC<br>
-b BSSID, --bssid BSSID
                            Specify the target network MAC<br>
### scan:
#### scan for APs and clients.
##### args:
iface       Specify the wireless interface you wish to use<br>
##### flags:
-h, --help                      show the help message and exit<br>
-c CHANNEL, --channel CHANNEL   Specify the channel you want to use, channel hooping is enabled by default.<br>
-e ESSID, --essid ESSID         Specify the ESSID of the target network.<br>
-b BSSID, --bssid BSSID         Specify the BSSID of the target network.<br>
-o OUTPUT, --output OUTPUT      Specify the name of the output file.<br>
### start: 
#### change the interface to monitor mode
##### args:
iface       Specify the wireless interface you wish to use<br>
##### flags:
-h, --help  show the help message and exit<br>
### stop: 
#### change the interface to managed mode
##### args:
iface       Specify the wireless interface you wish to use<br>
##### flags:
-h, --help  show the help message and exit<br>
### crack: 
#### crack the password from a captured 4 way handshake
##### args:
pcapFile              Specify the captured packets file.<br>
##### flags:
-h, --help                          show the help message and exit<br>
-t TARGET, --target TARGET          Specify the target network ESSID (name) you want to attack (make sure you have a 4 way handshake of it).<br>
-w WORDLIST, --wordlist WORDLIST    Specify the wordlist you wish to use.<br>

# Notice
I do not promote any illigal actions, please do not use this script for malicuse activities!

# _hope yall having a blast_
