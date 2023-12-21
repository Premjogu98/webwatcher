from docker_monitor.container_management import containerManagement
from dataclasses import dataclass
@dataclass
class DockerMonitor:    
    containerManagement.stopAllContainers()
    containerManagement.monitorContainers()
