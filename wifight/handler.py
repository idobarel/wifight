from subprocess import check_output
from argparse import ArgumentParser 
from os import geteuid
from termcolor import colored
from sys import argv

def isSudo():
    return geteuid() == 0

def getArgs():
    parser = ArgumentParser("wifight")
    subparsers = parser.add_subparsers(help='sub-command help')
    deauth_parser = subparsers.add_parser('deauth', help='Deauth a client from a target network')
    deauth_parser.add_argument("iface", type=str, help="Specify the wireless interface you wish to use")
    deauth_parser.add_argument("-t", "--target", required=True, type=str, help="Specify the target device MAC")
    deauth_parser.add_argument("-b", "--bssid", required=True, type=str, help="Specify the target network MAC")
    scan_parser = subparsers.add_parser('scan', help='Scan for APs')
    scan_parser.add_argument("-c", "--channel", required=False, type=int, default=-1, help="Specify the channel you want to use, channel hooping is enabled by default.")
    scan_parser.add_argument("-e", "--essid", required=False, type=str, default="", help="Specify the ESSID of the target network.")
    scan_parser.add_argument("-b", "--bssid", required=False, type=str, default="", help="Specify the BSSID of the target network.")
    scan_parser.add_argument("-o", "--output", required=False, type=str, default="", help="Specify the name of the output file.")
    scan_parser.add_argument("iface", type=str, help="Specify the wireless interface you wish to use")
    start_parser = subparsers.add_parser('start', help='Start monitor mode')
    start_parser.add_argument("iface", type=str, help="Specify the wireless interface you wish to use")
    stop_parser = subparsers.add_parser('stop', help='Stop monitor mode')
    stop_parser.add_argument("iface", type=str, help="Specify the wireless interface you wish to use")
    crack_parser = subparsers.add_parser('crack', help='Crack captured WPA handshake')
    crack_parser.add_argument("pcapFile", type=str, default="", help="Specify the captured packets file.")
    crack_parser.add_argument("-t", "--target", required=False, default="", type=str, help="Specify the target network ESSID (name) you want to attack (make sure you have a 4 way handshake of it).")
    crack_parser.add_argument("-w", "--wordlist", required=True, type=str, help="Specify the wordlist you wish to use.")
    wjam_parser = subparsers.add_parser("wjam", help="Deauth all nearby clients from their networks")
    wjam_parser.add_argument("iface", type=str, help="Specify the interface you wish to use for the attack")
    wjam_parser.add_argument("-c", "--channel", type=int, default=-1, help="Specify the channel you wish to use.")
    parser.parse_args()
    return parser

def iwconfing():
    raw = check_output(["iwconfig"], shell=True).decode()
    output = raw.split("\n")
    ifaces = []
    for l in output:
        if "no wireless extensions." in l:
            continue 
        ifaces.append(l.split(" ")[0])
    return ifaces

def getIfaces():
    addrs = iwconfing()
    return addrs

def setToMonitorMode(iface:str):
    if not iface in getIfaces():
        raise ValueError(f'{iface} was not found')
    check_output(f"sudo ifconfig {iface} down".split(" "))
    check_output(f"sudo iwconfig {iface} mode monitor".split(" "))
    check_output(f"sudo ifconfig {iface} up".split(" "))

def setToManagedMode(iface:str):
    if not iface in getIfaces():
        raise ValueError(f'{iface} was not found')
    check_output(f"sudo ifconfig {iface} down".split(" "))
    check_output(f"sudo iwconfig {iface} mode managed".split(" "))
    check_output(f"sudo ifconfig {iface} up".split(" "))