from main.db_connection.query_handler import QueryHandler
from main.logger import console_logger
import requests_unixsocket
import datetime
import time
import json
from typing import List, Dict, Any, Optional

class DockerServiceManagement:
    def __init__(self):
        self.QUERY_HANDLER = QueryHandler()
        self._init_data_count()
        self.session = requests_unixsocket.Session()
        self.docker_api_url = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
        self.volumes = [
            "/home/gts/image-comparison/comparison/:/app/comparison",
            "/home/gts/image-comparison/db_operation/:/app/db_operation",
            "/home/gts/image-comparison/file_handler/:/app/file_handler",
            "/home/gts/image-comparison/htmldocs/:/app/htmldocs",
            "/home/gts/image-comparison/main_operation/:/app/main_operation",
            "/home/gts/image-comparison/.env:/app/.env",
            "/home/gts/image-comparison/run.py:/app/run.py",
            "/home/gts/image-comparison/globalvar.py:/app/globalvar.py",
            "/etc/localtime:/etc/localtime:ro",
            "/etc/timezone:/etc/timezone:ro",
            "/dev/shm:/dev/shm",
            "/home/gts/image-comparison/container.json:/app/container.json",
        ]
        self.batch_size: Optional[int] = None

    def _init_data_count(self) -> None:
        query = """
            SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, 
            data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy,
            data.CompareChangedOn, data.LastCompareChangedOn, links.tender_link 
            FROM dms_wpw_tenderlinksdata AS data 
            JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id 
            WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y';
        """
        status, data = self.QUERY_HANDLER.getQueryAndExecute(query=query, fetchall=True)
        if not status:
            raise Exception("Failed to fetch data")
        self.data_count = len(data)
        console_logger.info(f"DATA COUNT : {self.data_count}")

    def createService(self, offset: int, limit: int, threads: int) -> None:
        service_name = f"{offset}-{limit}"
        spec = self._create_service_spec(service_name, offset, limit, threads)

        response = self.session.post(
            f"{self.docker_api_url}/services/create",
            headers={"content-type": "application/json"},
            data=json.dumps(spec),
        )
        if response.status_code == 201:
            console_logger.debug("Docker service created successfully!")
        else:
            console_logger.debug(f"Failed to create Docker service. Status code: {response.status_code}")
            console_logger.debug(response.text)

    def _create_service_spec(self, service_name: str, offset: int, limit: int, threads: int) -> Dict[str, Any]:
        return {
            "Name": service_name,
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "playwight:0.0.2",
                    "Env": [
                        f"DB_DATA_LIMIT={limit}",
                        f"DB_DATA_OFFSET={offset}",
                        f"THREAD={threads}",
                    ],
                    "Command": ["python", "run.py"],
                    "Mounts": [{"Target": vol.split(":")[1], "Source": vol.split(":")[0], "Type": "bind"} for vol in self.volumes],
                    "Init": False,
                    "StopGracePeriod": 10000000000,
                    "DNSConfig": {},
                    "Isolation": "default",
                    "CapabilityAdd": ["ALL"],
                },
                "Resources": {"Limits": {"MemoryBytes": 524288000}},
                "RestartPolicy": {"Condition": "none"},
                "Placement": {
                    "MaxReplicas": 1,
                    "Platforms": [{"Architecture": "amd64", "OS": "linux"}],
                },
                "ForceUpdate": 0,
                "Runtime": "container",
            },
            "Mode": {"Replicated": {"Replicas": 1}},
        }

    def getAllServiceInfo(self, service_id: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        url = f"{self.docker_api_url}/services/{service_id}" if service_id else f"{self.docker_api_url}/services"
        response = self.session.get(url)

        if response.status_code != 200:
            console_logger.debug(f"Failed to list Docker services. Status code: {response.status_code}")
            return None
        return response.json()

    def stopAllServices(self) -> None:
        services = self.getAllServiceInfo()
        if services:
            for service in services:
                service_id = service["ID"]
                response = self.session.delete(
                    f"{self.docker_api_url}/services/{service_id}",
                    params={"force": "true"},
                )
                if response.status_code == 200:
                    console_logger.debug(f"Service {service_id} forcefully stopped successfully.")
                else:
                    console_logger.debug(f"Failed to forcefully stop service {service_id}. Status code: {response.status_code}")
            console_logger.debug("All Docker services forcefully stopped.")
        else:
            console_logger.error("SERVICE INFO NOT FOUND")

    def inspectService(self, service_id: str) -> None:
        response = self.session.get(f"{self.docker_api_url}/services/{service_id}/tasks")

        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                task_id = task["ID"]
                task_logs_response = self.session.get(
                    f"{self.docker_api_url}/tasks/{task_id}/logs",
                    params={"stdout": "true", "tail": "20"},
                )

                if task_logs_response.status_code == 200:
                    logs = task_logs_response.text
                    console_logger.debug(f"Last 20 lines of logs for task {task_id}:")
                    console_logger.debug(logs)
                else:
                    console_logger.debug(f"Failed to get logs for task {task_id}. Status code: {task_logs_response.status_code}")
        else:
            console_logger.debug(f"Failed to get tasks for service ID {service_id}. Status code: {response.status_code}")

    def run(self, batch_size: int) -> None:
        self.batch_size = batch_size
        container_count = 0
        offset = 0
        while container_count < 3 and offset < min(self.data_count, 40000):
            self.createService(offset=offset, limit=batch_size, threads=5)
            offset += batch_size
            container_count += 1
            time.sleep(2)

if __name__ == "__main__":
    obj = DockerServiceManagement()
    obj.stopAllServices()
    # time.sleep(30)
    # obj.run(batch_size=100)
    # obj.inspectService(service_id="5b58f9134aedcde97468059a72ca187d00bd7b7f8d09ee5756e319d3c4d52448")