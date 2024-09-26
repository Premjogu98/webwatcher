from dataclasses import dataclass, field
import requests_unixsocket
import datetime
from datetime import timedelta, timezone
import time
import random
import docker
import pytz
from main.db_connection import DbConnection
from main.env_handler import EnvHandler
from main.db_connection.query_handler import QueryHandler
from main.logger import console_logger
from typing import List


@dataclass
class ContainerManagement:
    SESSION: requests_unixsocket.Session = requests_unixsocket.Session()
    DOCKER_URL: str = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
    DOCKER_CLIENT: docker.DockerClient = docker.DockerClient(
        base_url="unix://var/run/docker.sock"
    )
    BATCH_SIZE: int = None
    GROUP_ID: str = field(init=False, default="")
    DATA_COUNT: int = field(init=False, default=0)
    LIST_OF_CONTAINERS: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.__getDataCount()

    def __getDataCount(self):
        self.GROUP_ID = datetime.datetime.now().strftime("%Y%m%d%H:%M")
        DATABASE_DETAILS = EnvHandler.DB_CONNECTION
        self.dbconnection = DbConnection(CONNECTION_DETAILS=DATABASE_DETAILS)
        QUERY_HANDLER = QueryHandler(
            connection=self.dbconnection.connection, cur=self.dbconnection.cur
        )
        # query = """
        #         SELECT COUNT(*) AS record_count
        #         FROM dms_wpw_tenderlinks tl
        #         INNER JOIN dms_wpw_tenderlinksdata td ON tl.id = td.tlid
        #         INNER JOIN tbl_region re ON tl.country = re.Country_Short_Code
        #         WHERE tl.process_type = 'Web Watcher' AND tl.added_WPW = 'Y' AND td.entrydone = 'Y' AND (re.Region_Code LIKE '102%' OR re.Region_Code LIKE '104%' OR re.Region_Code LIKE '105%' OR re.Region_Code LIKE '103304%')
        #         ORDER BY tl.id ASC
        #     """

        # query = """
        #         SELECT COUNT(*) AS record_count
        #         FROM dms_wpw_tenderlinks tl
        #         INNER JOIN dms_wpw_tenderlinksdata td ON tl.id = td.tlid
        #         INNER JOIN tbl_region re ON tl.country = re.Country_Short_Code
        #         WHERE tl.process_type = 'Web Watcher' AND tl.added_WPW = 'Y'
        #         ORDER BY tl.id ASC"""

        # query = """
        #         SELECT COUNT(*) AS record_count
        #         FROM dms_wpw_tenderlinks tl
        #         INNER JOIN dms_wpw_tenderlinksdata td ON tl.id = td.tlid
        #         INNER JOIN tbl_region re ON tl.country = re.Country_Short_Code
        #         WHERE tl.process_type = 'Web Watcher' AND tl.added_WPW = 'Y' AND td.entrydone = 'Y' AND (re.Region_Code LIKE '101%' OR re.Region_Code LIKE '102%' OR re.Region_Code LIKE '104%' OR re.Region_Code LIKE '105%' OR re.Region_Code LIKE '103304%')
        #         ORDER BY tl.id ASC
        #     """

        # query = """SELECT COUNT(*) AS record_count FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y';"""

        status, data = QUERY_HANDLER.getQueryAndExecute(
            query="SELECT QUERY FROM `tend_dms`.`dms_wpw_query` LIMIT 1;", fetchone=True
        )
        query = f'SELECT COUNT(*) AS record_count FROM {data["QUERY"].partition("FROM")[2].strip()}'
        console_logger.debug(query)

        status, data = QUERY_HANDLER.getQueryAndExecute(query=query, fetchone=True)
        console_logger.debug(f"TOTAL RECORDS : {data}")
        self.dbconnection.connection.close()
        if not status:
            raise Exception("Failed to get data count from the database")
        self.DATA_COUNT = data["record_count"]
        return

    def __generateRandomNumber(self):
        return "".join(str(random.randint(0, 9)) for _ in range(20))

    def __containerMetaData(self, container_name, offset, limit, threads):
        volumes = [
            "/home/gts/web-watcher/htmldocs:/home/gts/code/htmldocs",
            "/home/gts/web-watcher/main:/home/gts/code/main",
            "/home/gts/web-watcher/logs:/home/gts/code/logs",
            "/home/gts/web-watcher/run.py:/home/gts/code/run.py",
            "/home/gts/web-watcher/.env:/home/gts/code/.env",
            "/etc/localtime:/etc/localtime:ro",
            "/etc/timezone:/etc/timezone:ro",
            "/dev/shm:/dev/shm",
            "/tmp/.X11-unix:/tmp/.X11-unix",
        ]
        envs = [
            f"DB_DATA_LIMIT={limit}",
            f"DB_DATA_OFFSET={offset}",
            f"THREAD={threads}",
            f"GROUP_ID={self.GROUP_ID}",
            f"CONTAINER_NAME={container_name}",
            # f"DISPLAY=localhost:10.0",
        ]
        return {
            "Image": "web-watcher:0.0.3",  # Image": "playwight:0.0.1", #web-watcher:0.0.1 wpw_selenium:0.0.1
            "Cmd": [
                "/bin/bash",
                "-c",
                # "apt-get update && apt-get install -y iputils-ping && pip3 install boto3 pyppeteer async_timeout && python run.py",
                "pip3 install boto3 pyppeteer async_timeout && python run.py",
            ],
            "Env": envs,
            "HostConfig": {
                "Binds": volumes,
                # "Memory": 1073741824,  # 1GB
                # "MemorySwap": 0,
                # "NanoCpus": 900000000, # 90%
                "NetworkMode": "host",
                "Privileged": True,
            },
            "StopTimeout": 30,
        }

    def __startDockerContainer(self, container_name, metadata):
        response = self.SESSION.post(
            f"{self.DOCKER_URL}/containers/create?name={container_name}", json=metadata
        )
        container_id = response.json()["Id"]
        self.SESSION.post(f"{self.DOCKER_URL}/containers/{container_id}/start")
        console_logger.debug(f"{container_name} STARTED")

    def __deployContainer(self, batch_size, container_limit, total_thread):
        self.BATCH_SIZE = batch_size
        container_count = 0
        offset = 0
        while True:
            if container_count != container_limit:
                # if offset <= self.data_count:
                container_name = f"{container_count}-{offset}-{batch_size}"
                self.__startDockerContainer(
                    container_name=container_name,
                    metadata=self.__containerMetaData(
                        container_name, offset, batch_size, total_thread
                    ),
                )
                offset += batch_size
                container_count += 1
                self.LIST_OF_CONTAINERS.append(container_name)
                continue
            else:
                break

    def __deployContainerWithBatch(
        self, batch_size, container_limit, total_thread, offset=0
    ):
        container_count = 0
        while True:
            if container_count != container_limit:
                # if offset <= self.data_count:
                container_name = f"{container_count}-{offset}-{batch_size}"
                self.__startDockerContainer(
                    container_name=container_name,
                    metadata=self.__containerMetaData(
                        container_name, offset, batch_size, total_thread
                    ),
                )
                offset += batch_size
                container_count += 1
                self.LIST_OF_CONTAINERS.append(container_name)
                continue
            else:
                break
        return offset

    def __stopAndRemoveContainers(self):
        console_logger.info("*** DOCKER CONTINER START PRUNING *** ")
        for container in self.DOCKER_CLIENT.containers.list(all=True):
            if (
                "web-watcher-nginx-1" not in container.name
                and "web-watcher-web-watcher-backend-1" not in container.name
                and "web-watcher-web-watcher-frontend-1" not in container.name
            ):
                container_info = container.attrs
                dt_start_time, str_start_time = self.__convertToLocalTime(
                    container_info["State"]["StartedAt"]
                )
                dt_end_time, str_end_time = self.__convertToLocalTime(
                    container_info["State"]["FinishedAt"]
                )
                dif = None
                if dt_end_time and dt_start_time:
                    dif = dt_end_time - dt_start_time
                console_logger.info(
                    f"{container.name} = STARTIME {str_start_time} | ENDTIME : {str_end_time} | TOTAL DIF (MIN) : {dif}"
                )
                self.__stopContainer(container_obj=container)
        console_logger.info("*** ALL DOCKER CONTAINER PRUNED ***\n")

    def __convertToLocalTime(self, utc_time):
        try:
            utc_time = utc_time[:26]
            datetime_obj = datetime.datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f")
            utc_timezone = pytz.timezone("UTC")
            datetime_obj = utc_timezone.localize(datetime_obj)
            local_timezone = pytz.timezone("Asia/Kolkata")
            local_time = datetime_obj.astimezone(local_timezone)
            return local_time, local_time.strftime("%Y-%m-%d %I:%M:%S")
        except:
            return None, None

    def __stopContainer(self, container_name=None, container_obj=None):
        try:
            if not container_obj:
                container_obj = self.DOCKER_CLIENT.containers.get(container_name)
            container_obj.stop()
            container_obj.remove()
            console_logger.info(
                f"Container '{container_obj.name}' stopped and removed successfully."
            )
        except docker.errors.NotFound:
            console_logger.error(f"Container '{container_obj.name}' not found.")

    def startContainers(self, batch_size, container_limit, total_thread):
        # console_logger.info("*** CONTAINER DEPLOYMENT PROCESS START ***")
        self.__deployContainer(batch_size, container_limit, total_thread)
        # console_logger.info("*** ALL CONTAINERS DEPLOYED SUCCESSFULLY ***\n")

    def stopAllContainers(self):
        self.__stopAndRemoveContainers()

    def is_container_frozen(
        self, container, cpu_threshold=0.1, memory_threshold=20, check_duration=10
    ):
        end_time = time.time() + check_duration
        while time.time() < end_time:
            stats = container.stats(stream=False)
            console_logger.debug(stats)
            cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
            system_cpu_usage = stats["cpu_stats"].get("system_cpu_usage", None)
            if not system_cpu_usage:
                return True
            system_cpu_delta = (
                system_cpu_usage - stats["precpu_stats"]["system_cpu_usage"]
            )
            memory_usage = stats["memory_stats"]["usage"]

            cpu_delta = cpu_usage - stats["precpu_stats"]["cpu_usage"]["total_usage"]

            cpu_percent = (
                (cpu_delta / system_cpu_delta)
                * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"])
                * 100.0
            )
            memory_usage_mb = memory_usage / (1024 * 1024)

            if cpu_percent > cpu_threshold or memory_usage_mb > memory_threshold:
                return False
            time.sleep(1)
        return True

    def running_container_status(self):
        for container in self.DOCKER_CLIENT.containers.list(
            filters={"status": "running"}
        ):
            if (
                "web-watcher-nginx-1" not in container.name
                and "web-watcher-web-watcher-backend-1" not in container.name
                and "web-watcher-web-watcher-frontend-1" not in container.name
                and container.name in self.LIST_OF_CONTAINERS
            ):
                start_time = datetime.datetime.strptime(
                    container.attrs["State"]["StartedAt"][:26],
                    "%Y-%m-%dT%H:%M:%S.%f",
                ).replace(tzinfo=timezone.utc)

                running_time = datetime.datetime.now(timezone.utc) - start_time

                if running_time > timedelta(hours=1):
                    self.__stopContainer(container.name)
                    del self.LIST_OF_CONTAINERS[
                        self.LIST_OF_CONTAINERS.index(container.name)
                    ]
                    console_logger.debug(
                        f"Container has been running for {running_time} {container.name}"
                    )
                # else:
                #     console_logger.debug(
                #         f"Container has been running for {running_time}, which is less than 1 hour"
                #     )
                #     return False

    def monitorContainers(self):
        while True:
            batch_size = 500
            offset = 0
            container_count = round(self.DATA_COUNT / batch_size / 2)
            console_logger.info(
                f"TOTAL RECORDS : {self.DATA_COUNT} | CONTAINER COUNT : {container_count * 2}"
            )
            for idx in range(2):
                offset += self.__deployContainerWithBatch(
                    offset=offset,
                    container_limit=container_count,
                    batch_size=batch_size,
                    total_thread=2,
                )
                while len(self.LIST_OF_CONTAINERS) != 0:
                    for container in self.DOCKER_CLIENT.containers.list(
                        filters={"status": "exited"}
                    ):
                        if (
                            "web-watcher-nginx-1" not in container.name
                            and "web-watcher-web-watcher-backend-1"
                            not in container.name
                            and "web-watcher-web-watcher-frontend-1"
                            not in container.name
                            and container.name in self.LIST_OF_CONTAINERS
                        ):
                            self.__stopContainer(container.name)
                            del self.LIST_OF_CONTAINERS[
                                self.LIST_OF_CONTAINERS.index(container.name)
                            ]
                            console_logger.info(
                                f"TOTAL {len(self.LIST_OF_CONTAINERS)} Containers Remaining "
                            )
                    self.running_container_status()

                    # console_logger.info(
                    #     f"continue sleep for 60 sec until container count 0 current count {len(self.LIST_OF_CONTAINERS)}"
                    # )
                    time.sleep(60)

            self.__getDataCount()
            # console_logger.info(f"LATEST TOTAL RECORDS : {self.DATA_COUNT} ")
            # return


containerManagement = ContainerManagement()
