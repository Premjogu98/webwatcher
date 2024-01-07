from dataclasses import dataclass,field
import requests_unixsocket,datetime,time,string,random,docker,pytz
from main.db_connection import DbConnection
from main.env_handler import EnvHandler
from main.db_connection.query_handler import QueryHandler
from main.logger import console_logger
from typing import List

@dataclass
class ContainerManagement:
    SESSION = requests_unixsocket.Session()
    DOCKER_URL = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
    DOCKER_CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock')
    BATCH_SIZE = None
    GROUP_ID = 0
    DATA_COUNT = 0
    LIST_OF_CONTAINERS:List[str] = field(default_factory=list) 

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        self.GROUP_ID = self.__generateRandomNumber()
        self.DATA_COUNT = self.__getDataCount()

    def __getDataCount(self):
        DATABASE_DETAILS = EnvHandler.DB_CONNECTION
        self.dbconnection = DbConnection(CONNECTION_DETAILS=DATABASE_DETAILS)
        QUERY_HANDLER = QueryHandler(
            connection=self.dbconnection.connection, cur=self.dbconnection.cur
        )
        query = """
                SELECT COUNT(*) AS record_count
                FROM dms_wpw_tenderlinks tl 
                INNER JOIN dms_wpw_tenderlinksdata td ON tl.id = td.tlid
                INNER JOIN tbl_region re ON tl.country = re.Country_Short_Code
                WHERE tl.process_type = 'Web Watcher' AND tl.added_WPW = 'Y' AND td.entrydone = 'N' AND (re.Region_Code LIKE '102%' OR re.Region_Code LIKE '104%' OR re.Region_Code LIKE '105%' OR re.Region_Code LIKE '103304%')
                ORDER BY tl.id ASC
            """
        # query = """SELECT COUNT(*) AS record_count FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y';"""
        status, data = QUERY_HANDLER.getQueryAndExecute(query=query, fetchone=True)
        console_logger.debug(f"TOTAL RECORDS : {data}")
        if not status:
            raise Exception
        return data["record_count"]
    
    def __generateRandomNumber(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(20))
    
    def __containerMetaData(self,container_name,offset,limit,threads):
        volumes = [
            "/home/gts/web-watcher/htmldocs:/home/gts/code/htmldocs",
            "/home/gts/web-watcher/main:/home/gts/code/main",
            "/home/gts/web-watcher/logs:/home/gts/code/logs",
            "/home/gts/web-watcher/run.py:/home/gts/code/run.py",
            "/etc/localtime:/etc/localtime:ro",
            "/etc/timezone:/etc/timezone:ro",
            "/dev/shm:/dev/shm"
        ]
        envs = [
            f"DB_DATA_LIMIT={limit}",
            f"DB_DATA_OFFSET={offset}",
            f"THREAD={threads}",
            f"GROUP_ID={self.GROUP_ID}",
            f"CONTAINER_NAME={container_name}"
        ]
        container_create_data = {
            "Image": "web-watcher:0.0.1", # Image": "playwight:0.0.1", #web-watcher:0.0.1
            "Cmd": ["/bin/bash", "-c", "pip3 install cdifflib && python run.py"],
            "Env": envs,
            "HostConfig": {
                "Binds": volumes,
                "Memory": 1073741824,  # 1GB
                # "MemorySwap": 0,
                # "NanoCpus": 900000000, # 90%
                "NetworkMode":"host"
            },
        }
        return container_create_data
    
    def __startDockerContainer(self,container_name,metadata:dict):
        response = self.SESSION.post(f"{self.DOCKER_URL}/containers/create?name={container_name}", json=metadata)
        container_id = response.json()["Id"]
        self.SESSION.post(f"{self.DOCKER_URL}/containers/{container_id}/start")
        console_logger.debug(f"{container_name} STARTED")

    def __deployContainer(self,batch_size,container_limit,total_thread):
        self.BATCH_SIZE = batch_size
        container_count = 0
        offset = 0
        while True:
            if container_count != container_limit:
            # if offset <= self.data_count:
                container_name = f"{container_count}-{offset}-{batch_size}"
                self.__startDockerContainer(container_name=container_name,metadata=self.__containerMetaData(container_name,offset,batch_size,total_thread))
                offset += batch_size
                container_count += 1
                self.LIST_OF_CONTAINERS.append(container_name)
                continue
            else:
                break

    def __deployContainerWithBatch(self,batch_size,container_limit,total_thread,offset=0):
        container_count = 0
        while True:
            if container_count != container_limit:
            # if offset <= self.data_count:
                container_name = f"{container_count}-{offset}-{batch_size}"
                self.__startDockerContainer(container_name=container_name,metadata=self.__containerMetaData(container_name,offset,batch_size,total_thread))
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
            if "web-watcher-nginx-1" not in container.name:
                container_info = container.attrs
                dt_start_time,str_start_time = self.__convertToLocalTime(container_info['State']['StartedAt'])
                dt_end_time,str_end_time = self.__convertToLocalTime(container_info['State']['FinishedAt'])
                dif = None
                if dt_end_time and dt_start_time:
                    dif = dt_end_time - dt_start_time
                console_logger.info(f"{container.name} = STARTIME {str_start_time} | ENDTIME : {str_end_time} | TOTAL DIF (MIN) : {dif}")
                self.__stopContainer(container_obj=container)

        console_logger.info("*** ALL DOCKER CONTAINER PRUNED ***\n")

    def __convertToLocalTime(self, utc_time):
        try:
            utc_time = utc_time[:26]
            datetime_obj = datetime.datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S.%f')

            # Convert to UTC timezone
            utc_timezone = pytz.timezone('UTC')
            datetime_obj = utc_timezone.localize(datetime_obj)

            # Convert to local timezone
            local_timezone = pytz.timezone('Asia/Kolkata')
            local_time = datetime_obj.astimezone(local_timezone)
            return local_time , local_time.strftime('%Y-%m-%d %I:%M:%S')
        except:
            return None,None
        
    def __stopContainer(self,container_name=None, container_obj=None):
        try:
            if not container_obj:
                container_obj = self.DOCKER_CLIENT.containers.get(container_name)
            container_obj.stop()
            container_obj.remove()
            console_logger.info(f"Container '{container_obj.name}' stopped and removed successfully.")
        except docker.errors.NotFound:
            console_logger.error(f"Container '{container_obj.name}' not found.")

    def startContainers(self,batch_size,container_limit,total_thread):
        console_logger.info("*** CONTAINER DEPLOYMENT PROCESS START ***")
        self.__deployContainer(batch_size=batch_size,container_limit=container_limit,total_thread=total_thread)
        console_logger.info("*** ALL CONTAINER DEPLOYMED SUCESSFULLY ***\n")

    def stopAllContainers(self):
        self.__stopAndRemoveContainers()

    def monitorContainers(self):
        while True:
            batch_size = 500
            offset = 0
            container_count = round(round(self.DATA_COUNT / batch_size) / 1)
            console_logger.info(f"TOTAL RECORDS : {self.DATA_COUNT} | CONTAINER COUNT : {container_count * 1} ")
            for idx in range(1):
                console_logger.debug(idx)
                offset += self.__deployContainerWithBatch(offset=offset,container_limit=container_count ,batch_size=batch_size,total_thread=1)
                while len(self.LIST_OF_CONTAINERS) != 0:
                    for container in self.DOCKER_CLIENT.containers.list(filters={"status": "exited"}):
                        if "web-watcher-nginx-1" not in container.name and container.name in self.LIST_OF_CONTAINERS:
                            self.__stopContainer(container.name)
                            del self.LIST_OF_CONTAINERS[self.LIST_OF_CONTAINERS.index(container.name)]
                            console_logger.info(f"TOTAL {len(self.LIST_OF_CONTAINERS)} Containers Remaining ")
                    console_logger.info(f"continue sleep for 30 sec until container count 0 current count {len(self.LIST_OF_CONTAINERS)}")
                    time.sleep(30)
            

containerManagement = ContainerManagement()