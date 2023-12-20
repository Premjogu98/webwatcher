from docker_monitor.container_management import containerManagement
from dataclasses import dataclass
@dataclass
class Main:
    nothing = ""
    
    def __𝐩𝐨𝐬𝐭_ini𝐭__ (self):
        containerManagement.stopAllContainers()
        containerManagement.startContainers(container_limit=55,batch_size=1300,total_thread=2)