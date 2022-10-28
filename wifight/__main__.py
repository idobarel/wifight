#!/usr/bin/env python3
from wifight.handler import *
from wifight.deauther import Deauther
from wifight.errors import ExitCodes
from wifight.scanner import Scanner
from wifight.cracker import Cracker
from wifight.wjam import Wjam

def main()->int:
    args = getArgs()
    try:
        command = argv[1]  
    except IndexError:
        args.print_help()
        return ExitCodes.ARGS_ERROR
    if not isSudo():
        print("["+colored("-", "red")+"]"+" sudo is required")
        return ExitCodes.PERMISSION_ERROR
    match command:
        case "deauth":
            deauther = Deauther(args.parse_args().__dict__)
            deauther.start()
        case "scan":
            scanner = Scanner(args.parse_args().__dict__)
            scanner.start()
        case "start":
            setToMonitorMode(args.parse_args().iface)
        case "stop":
            setToManagedMode(args.parse_args().iface)
        case "crack":
            Cracker(args.parse_args().__dict__)
        case "wjam":
            Wjam(args.parse_args().__dict__)
        case _:    
            return ExitCodes.ARGS_ERROR
    
if __name__ == '__main__':
    exit(main())
