from termcolor import colored
import os
import time

class Cracker():
    def __init__(self, args:dict):
        print('['+colored("-", "yellow")+"]"+
        "The program is using "+ colored("aircrack-ng", "cyan") +" to crack the WPA handshake.")
        self.__dict__.update(args)
        print("Hold On! Proccessing...")
        time.sleep(2)
        self.crack()
    
    def crack(self):
        if self.target != "":
            os.system(f"aircrack-ng {self.pcapFile} -w {self.wordlist} -e {self.target}")
        else:
            os.system(f"aircrack-ng {self.pcapFile} -w {self.wordlist}")

