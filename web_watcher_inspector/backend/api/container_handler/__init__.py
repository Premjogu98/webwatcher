import docker
from datetime import datetime, timezone
import requests_unixsocket
from api.logger import console_logger


class ContainerHandler:
    def __init__(self) -> None:
        self.SESSION: requests_unixsocket.Session = requests_unixsocket.Session()
        self.DOCKER_URL: str = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
        self.DOCKER_CLIENT: docker.DockerClient = docker.DockerClient(
            base_url="unix://var/run/docker.sock"
        )

    def format_uptime(self, start_time):
        now = datetime.now(timezone.utc)
        uptime = now - start_time
        total_seconds = int(uptime.total_seconds())
        if total_seconds >= 3600:
            return f"{total_seconds // 3600} hrs"
        elif total_seconds >= 60:
            return f"{total_seconds // 60} min"
        else:
            return f"{total_seconds} sec"

    def get_container_names(self):
        containers = self.DOCKER_CLIENT.containers.list(all=True)
        detail = []
        sr_no = 1
        for container in containers:
            if not container.name.startswith("web-watcher-"):
                try:
                    start_time = datetime.strptime(
                        container.attrs["State"]["StartedAt"][:26],
                        "%Y-%m-%dT%H:%M:%S.%f",
                    ).replace(tzinfo=timezone.utc)
                    uptime = self.format_uptime(start_time)
                except KeyError:
                    uptime = "N/A"
                detail.append(
                    {
                        "sr": sr_no,
                        "container_id": container.short_id,
                        "container_name": container.name,
                        "container_uptime": uptime,
                        "status": container.status,
                    }
                )
                sr_no += 1
        return detail


containerHandler = ContainerHandler()
