from scapy.all import Dot11Beacon, Dot11, Dot11Elt, Packet, sniff, wrpcap
from tabulate import tabulate
import os
import time
from threading import Thread
from dataclasses import dataclass

@dataclass
class NetworkData():
    bssid:str
    power:str
    channel:str
    crypto:str
    ssid:str

    @property
    def data(self):
        return list(self.__dict__.values())

@dataclass
class ClientData():
    src_addr:str
    ap_addr:str
    channel:str

    @property
    def data(self):
        return list(self.__dict__.values())

class Scanner():
    def __init__(self, args:dict) -> None:
        self.__dict__.update(args)
        self.networks:list[NetworkData] = []
        self.clients:list[ClientData] = []
        self.done = False
        self.mapping = {}

    def changeChannel(self):
        if self.channel == -1:
            ch = 1
            while True:
                if self.done == True:
                    return
                os.system(f"iwconfig {self.iface} channel {ch}")
                self.channel = ch
                ch = ch % 14 + 1
                time.sleep(0.2)
        else:
            os.system(f"iwconfig {self.iface} channel {self.channel}")

    def callback(self, packet:Packet):
        if packet.haslayer(Dot11) and not packet.haslayer(Dot11Beacon):
            if packet.type in [1, 2]:
                doesExistsCD = False
                cd = ClientData(packet.addr1, str(packet.addr2), self.channel)
                if cd.ap_addr == "00:00:00:00:00:00":
                    return
                if self.essid != "":
                    if cd.ap_addr == "None":
                        return
                    try:
                        self.bssid = self.mapping[self.essid]
                    except:
                        pass
                if self.bssid != "":
                    if cd.ap_addr != self.bssid:
                        return
                if not cd in self.clients:
                    for i, ne in enumerate(self.networks):
                        if ne.bssid == cd.src_addr or cd.src_addr == "ff:ff:ff:ff:ff:ff":
                            doesExistsCD = True
                    if not doesExistsCD:
                        self.clients.append(cd)
        if packet.haslayer(Dot11Beacon):
            doesExistsNE = False
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()
            if ssid == "":
                return
            try:
                power = str(packet.dBm_AntSignal)
            except:
                power = "N/A"
            stats = packet[Dot11Beacon].network_stats()
            channel = stats.get("channel")
            crypto = stats.get("crypto")
            if self.bssid != "":
                    if bssid != self.bssid:
                        return
            if self.essid != "":
                if ssid != self.essid:
                    return
                self.mapping = {ssid:bssid}
            for i, ne in enumerate(self.networks):
                if ne.bssid == bssid:
                    self.networks[i].power = power
                    doesExistsNE = True
                    break
            if not doesExistsNE:
                ne = NetworkData(bssid, power, channel, crypto, ssid)
                if not ne in self.networks:
                    self.networks.append(ne)
        

    def printer(self):
        try:
            while True:
                if self.done:
                    return
                dataNE = [ne.data for ne in self.networks]
                dataCD = [cd.data for cd in self.clients]
                headersNE = ["BSSID","PWR", "CH", "CIPHER", "ESSID"]
                headersCD = ["ADDRS", "AP", "CH"]
                print(f"[channel => {self.channel}], [output => {self.output}]\n")
                print("APs:")
                print(tabulate(dataNE, headers=headersNE, tablefmt="fancy_grid"))
                print("Clients:")
                print(tabulate(dataCD, headers=headersCD, tablefmt="fancy_grid"))
                time.sleep(0.2)
                os.system("clear")
        except :
            pass


    def start(self):
        cChanger = Thread(target=self.changeChannel)
        cChanger.daemon = True
        cChanger.start()
        printer = Thread(target=self.printer)
        printer.start()
        try:
            x = sniff(iface=self.iface, prn=self.callback)
            if self.output != "":
                wrpcap(self.output, x)
        except KeyboardInterrupt:
            if self.output != "":
                wrpcap(self.output, x)
            self.done = True
            os.system("clear")
            exit()

