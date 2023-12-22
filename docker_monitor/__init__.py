from docker_monitor.container_management import containerManagement
from dataclasses import dataclass
@dataclass
class DockerMonitor:    
    containerManagement.stopAllContainers()
    containerManagement.startContainers(container_limit=65,batch_size=1000,total_thread=3)
    # containerManagement.monitorContainers()
