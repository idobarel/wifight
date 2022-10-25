from enum import auto, IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    ARGS_ERROR = auto()
    PERMISSION_ERROR = auto()

