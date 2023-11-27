from dataclasses import dataclass

@dataclass
class GlobalVariable:
    path_error:int = 0
    exceptions:int = 0
    timeout_error:int = 0
    success:int = 0
    compared:int = 0
    total_data:int = 0
    nothing_changed:int = 0